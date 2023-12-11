import os
import sqlite3
import json

def fetch_patient_info(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT first_name, last_name, dob, sex, street_name, building_number, postcode, city_name, phone_number, email
            FROM patients
            WHERE patient_id = ?
            """, (patient_id,))
        patient_info = cursor.fetchone()
        return patient_info
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def fetch_latest_consultation(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        # Query to get the latest consultation ID and date for the given patient
        cursor.execute("""
            SELECT consultation_id, consultation_date 
            FROM consultations 
            WHERE patient_id = ? 
            ORDER BY consultation_date DESC 
            LIMIT 1
        """, (patient_id,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]  # consultation_id and consultation_date
        return None, None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None
    finally:
        conn.close()

def fetch_diagnoses(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT d.diagnosis_name, d.diagnosis_date, d.diagnosis_type
            FROM diagnoses d
            JOIN consultations c ON d.consultation_id = c.consultation_id
            WHERE c.patient_id = ?
            ORDER BY d.diagnosis_type DESC  -- Ensure that primary diagnoses come first
            """, (patient_id,))
        fetched_diagnoses = cursor.fetchall()
        
        # Separate primary and secondary diagnoses
        primary_diagnosis = next((diag for diag in fetched_diagnoses if diag[2] == 'Primary'), None)
        secondary_diagnoses = [diag for diag in fetched_diagnoses if diag[2] == 'Secondary']
        
        return primary_diagnosis, secondary_diagnoses
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None
    finally:
        conn.close()

def fetch_diabetes_details(consultation_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT therapy, hcl_system_details, hba1c_current, 
            hba1c_previous, hba1c_previous_date, akutkomplikationen, spätkomplikationen, 
            complications_score, antibodies_status, insulin_details, oral_medication_details, 
            non_insulin_injection_details
            FROM diabetes_details
            WHERE consultation_id = ?
            """, (consultation_id,))
        details = cursor.fetchone()
        if details:
            # Assuming all details are stored in JSON format in the database
            # Decode JSON fields to dictionaries
            diabetes_details = {
                'therapy': json.loads(details[0]) if details[0] else None,
                'hcl_system_details': json.loads(details[1]) if details[1] else None,
                'hba1c_current': details[2],
                'hba1c_previous': details[3],
                'hba1c_previous_date': details[4],
                'acute_complications': json.loads(details[5]) if details[5] else None,
                'late_complications': json.loads(details[6]) if details[6] else None,
                'complications_score': details[7],
                'antibodies_status': json.loads(details[8]) if details[8] else None,
                'insulin_details': json.loads(details[9]) if details[9] else None,
                'oral_medication_details': json.loads(details[10]) if details[10] else None,
                'non_insulin_injection_details': json.loads(details[11]) if details[11] else None,
            }
            print("Fetched Insulin details:", diabetes_details['insulin_details'])
            return diabetes_details
        else:
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def fetch_cv_risk_factors(consultation_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT art_hypertension, dyslipidemia, obesity_grade, 
            bmi, smoking_status, family_history
            FROM cv_risk_factors
            WHERE consultation_id = ?
            """, (consultation_id,))
        details = cursor.fetchone()
        if details:
            # Assuming that all details except 'bmi' are stored as JSON strings
            cvrf_details = {
                'art_hypertension': details[0],
                'dyslipidemia': details[1],
                'obesity_grade': details[2],
                'bmi': details[3],
                'smoking_status': json.loads(details[4]) if details[4] else None,
                'family_history': json.loads(details[5]) if details[5] else None,
            }
            return cvrf_details
        else:
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def create_report(patient_id):
    # Fetch Data
    patient_info = fetch_patient_info(patient_id)
    if not patient_info:
        print(f"Patient info not found for patient_id: {patient_id}")
        return

    latest_consultation_id, current_consultation_date_long = fetch_latest_consultation(patient_id)

    # Convert consultation date to mm/yyyy format
    current_consultation_date_short = None
    if current_consultation_date_long:
        date_parts = current_consultation_date_long.split('.')
        if len(date_parts) == 3:
            current_consultation_date_short = f"{date_parts[1]}/{date_parts[2]}"

    primary_diagnosis, secondary_diagnoses = fetch_diagnoses(patient_id)
    diabetes_details = fetch_diabetes_details(latest_consultation_id) if latest_consultation_id else None
    cvrf_details = fetch_cv_risk_factors(latest_consultation_id) if latest_consultation_id else None

    # Patient Details
    patient_details = f"{patient_info[0]} {patient_info[1]}, {patient_info[2]}\n"
    patient_details += f"{patient_info[3]} {patient_info[4]}, {patient_info[5]}, {patient_info[6]}, {patient_info[7]}\n\n"

    # Constructing Other Report Sections
    diagnosis_section, therapy_section, acute_complications_section, cv_risk_factors_section, late_complications_section = construct_report_sections(diabetes_details, primary_diagnosis, secondary_diagnoses, current_consultation_date_short, cvrf_details)

    # Combine all sections into the final report
    report = patient_details + diagnosis_section + therapy_section + acute_complications_section + cv_risk_factors_section + late_complications_section

    # Save Report to File
    save_report_to_file(report, patient_id)

def save_report_to_file(report, patient_id):
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    report_filename = os.path.join(reports_dir, f'report_patient_{patient_id}.txt')
    with open(report_filename, 'w') as file:
        file.write(report)
    
    print(f"Report for patient_id {patient_id} created as {report_filename}")

def construct_report_sections(diabetes_details, primary_diagnosis, secondary_diagnoses, current_consultation_date_short, cvrf_details):
    # Diagnosis Section
    diagnosis_section = "Diagnosen\n"
    if primary_diagnosis:
        diagnosis_section += f"1. {primary_diagnosis[0]} (ED {primary_diagnosis[1]})\n"
        # Add additional details from diabetes_details if available
        if diabetes_details:
            if diabetes_details['antibodies_status']:
                antibodies_pos = '-, '.join(diabetes_details['antibodies_status'].get('positive', []))
                antibodies_neg = '-, '.join(diabetes_details['antibodies_status'].get('negative', []))
                diagnosis_section += f"- {antibodies_pos}-Autoantikörper positiv; {antibodies_neg}-Autoantikörper negativ\n"

            # Therapy Section
            therapy_section = "Therapie\n"
            if diabetes_details['therapy']:
                therapy_section += f"- {diabetes_details['therapy']}"

            # Add hcl_system details if present
            if diabetes_details['hcl_system_details']:
                therapy_section += f" ({diabetes_details['hcl_system_details']['system']}, Insulin {diabetes_details['hcl_system_details']['insulin']}, seit {diabetes_details['hcl_system_details']['start_year']})"

            # Add insulin details if present
            if diabetes_details['insulin_details']:
                print("Insulin details:", diabetes_details['insulin_details'])
                insulin_str = '; '.join([f"{insulin['type']} {insulin['insulin']} seit {insulin['start_year']}" 
                                        for insulin in diabetes_details['insulin_details']])
                therapy_section += f" ({insulin_str})"

            # Add oral medication details if present
            if diabetes_details['oral_medication_details']:
                therapy_section += f" ({diabetes_details['oral_medication_details']})"

            # Add non_insulin_injection details if present
            if diabetes_details['non_insulin_injection_details']:
                therapy_section += f" ({diabetes_details['non_insulin_injection_details']})"

            # Add current and previous HbA1c values
            therapy_section += f"\n- HbA1c {diabetes_details['hba1c_current']} % {current_consultation_date_short} ({diabetes_details['hba1c_previous']} % {diabetes_details['hba1c_previous_date']})\n"

        therapy_section += "\n"


    # Acute Complications
    acute_complications_section = "Akutkomplikationen\n"
    if diabetes_details and diabetes_details.get('acute_complications'):
        acute_complications_list = diabetes_details['acute_complications']

        # Group the complications by type
        grouped_complications = {}
        for complication in acute_complications_list:
            comp_type = complication['type']
            comp_date = complication['date']
            # Convert date format from dd.mm.yyyy to mm/yyyy
            if comp_date:
                date_parts = comp_date.split('.')
                if len(date_parts) == 3:
                    comp_date = f"{date_parts[1]}/{date_parts[2]}"

            grouped_complications.setdefault(comp_type, []).append(comp_date)

        # Format each group of complications
        for comp_type, dates in grouped_complications.items():
            sorted_dates = sorted(dates, reverse=True)
            dates_str = ', '.join(sorted_dates)
            acute_complications_section += f"- {comp_type} (zuletzt {dates_str})\n"

    else:
        acute_complications_section += "- Keine\n"

    # Cardiovascular Risk Factors
    cv_risk_factors_section = "Weitere kardiovaskuläre Risikofaktoren\n"
    if cvrf_details:
        cv_risk_factors_parts = []
        for factor, value in cvrf_details.items():
            if value is not None:
                if factor == 'bmi':
                    cv_risk_factors_parts.append(f"{factor}: {value:.1f}")  # Format BMI with one decimal place
                else:
                    cv_risk_factors_parts.append(f"{factor}: {value}")

        if cv_risk_factors_parts:
            cv_risk_factors_section += "- " + ', '.join(cv_risk_factors_parts) + "\n"
        else:
            cv_risk_factors_section += "- Keine\n"
    else:
        cv_risk_factors_section += "- Keine\n"

    # Late Complications
    late_complications_section = "Spätkomplikationen\n"
    if diabetes_details and diabetes_details['late_complications']:
        for complication in diabetes_details['late_complications']:
            late_complications_section += f"- {complication['name']} ({complication['date']})\n"
    else:
        late_complications_section += "- Keine\n"

    return diagnosis_section, therapy_section, acute_complications_section, cv_risk_factors_section, late_complications_section

def generate_reports_for_range(start_id, end_id):
    for patient_id in range(start_id, end_id + 1):
        create_report(patient_id)

# call to generate reports for patient IDs x through y
generate_reports_for_range(2, 2)