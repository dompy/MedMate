#db_operations.py

from dateutil.relativedelta import relativedelta
from datetime import datetime
import sqlite3
import json

# Database management functions
def create_database():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS patients')
    cursor.execute('DROP TABLE IF EXISTS consultations')
    cursor.execute('DROP TABLE IF EXISTS diagnoses')
    cursor.execute('DROP TABLE IF EXISTS diabetes_details')
    cursor.execute('DROP TABLE IF EXISTS complications')
    cursor.execute('DROP TABLE IF EXISTS cv_risk_factors')
    cursor.execute('DROP TABLE IF EXISTS findings')
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute('DROP TABLE IF EXISTS medications')
    
    # Create patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        dob TEXT NOT NULL,  
        age INTEGER,
        sex TEXT,
        street_name TEXT,
        building_number TEXT,
        postcode TEXT,
        city_name TEXT,
        canton_name TEXT,
        canton_code TEXT,          
        phone_number INTEGER,
        ahv_number INTEGER,
        email TEXT
    )
    ''')

    # Create consultations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS consultations (
        consultation_id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        consultation_date TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    ''')

    # Create primary diagnosis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diagnoses (
        diagnosis_id INTEGER PRIMARY KEY,
        consultation_id INTEGER NOT NULL,
        diagnosis_name TEXT NOT NULL,
        diagnosis_date TEXT,
        diagnosis_type TEXT, 
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id)
    )
    ''')
    
    # Create primary diagnosis details table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diabetes_details (
        detail_id INTEGER PRIMARY KEY,
        consultation_id INTEGER NOT NULL,
        therapy TEXT, 
        hcl_system_details TEXT,
        hba1c_current REAL,
        hba1c_previous REAL,
        akutkomplikationen TEXT, 
        spätkomplikationen TEXT,
        complications_score INTEGER,
        antibodies_status TEXT,
        insulin_details TEXT, 
        oral_medication_details TEXT, 
        non_insulin_injection_details TEXT, 
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id)
    )
    ''')


    # Create cv risk factors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cv_risk_factors (
        risk_factor_id INTEGER PRIMARY KEY,
        consultation_id INTEGER NOT NULL,
        art_hypertension BOOLEAN,
        dyslipidemia TEXT,
        obesity_grade TEXT,
        bmi REAL,
        smoking_status TEXT,
        family_history TEXT,
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id)
    )
    ''')
    
    # Create findings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS findings (
        finding_id INTEGER PRIMARY KEY,
        consultation_id INTEGER,
        measurement_type TEXT NOT NULL,
        value REAL,
        date_recorded TEXT,
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id)
    )
    ''')
    
    # Create medictions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        medication_id INTEGER PRIMARY KEY,
        consultation_id INTEGER,
        medication_name TEXT NOT NULL,
        dosage_morning INTEGER, 
        dosage_midday INTEGER,
        dosage_evening INTEGER,
        dosage_night INTEGER,
        notes TEXT,
        FOREIGN KEY(consultation_id) REFERENCES consultations(consultation_id)
    )
    ''')
    
    # Create scores table for calculated scores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        score_id INTEGER PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        score_type TEXT NOT NULL,
        score_value REAL,
        date_assessed TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    ''')


def add_patient(patient):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO patients (first_name, last_name, dob, age, sex, street_name, building_number, postcode, city_name, canton_name, canton_code, phone_number, ahv_number, email) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patient)

    patient_id = cursor.lastrowid  # Get the ID of the newly added patient

    conn.commit()
    conn.close()

    return patient_id

def add_consultation(patient_id, consultation_date):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO consultations (patient_id, consultation_date)
    VALUES (?, ?)
    ''', (patient_id, consultation_date))

    consultation_id = cursor.lastrowid  # Get the last inserted row ID

    conn.commit()
    conn.close()

    return consultation_id

def add_diagnosis(consultation_id, diagnosis_name, diagnosis_date, diagnosis_type):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    try:
        # If the diagnosis_date is an empty string, you might want to insert NULL or a default date
        date_to_insert = diagnosis_date if diagnosis_date else "[]"
        cursor.execute('''
        INSERT INTO diagnoses (consultation_id, diagnosis_name, diagnosis_date, diagnosis_type)
        VALUES (?, ?, ?, ?)
        ''', (consultation_id, diagnosis_name, date_to_insert, diagnosis_type))

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred(1): {e}")

    finally:
        conn.close()


def add_diabetes_details(consultation_id, therapy, antibodies_status, hcl_system_details, insulin_details, 
                         oral_medication_details, non_insulin_injection_details, 
                         complications_score, spätkomplikationen, hba1c_current, 
                         hba1c_previous, akutkomplikationen):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    try:
        # Convert dictionary details and lists to JSON string for storage
        therapy_str = json.dumps(therapy) if therapy else None
        antibodies_status_str = json.dumps(antibodies_status) if antibodies_status else None
        hcl_system_details_str = json.dumps(hcl_system_details) if hcl_system_details else None
        insulin_details_str = json.dumps(insulin_details) if insulin_details else None
        oral_medication_details_str = json.dumps(oral_medication_details) if oral_medication_details else None
        non_insulin_injection_details_str = json.dumps(non_insulin_injection_details) if non_insulin_injection_details else None
        spätkomplikationen_str = json.dumps(spätkomplikationen) if spätkomplikationen else None
        akutkomplikationen_str = json.dumps(akutkomplikationen) if akutkomplikationen else None
        
        cursor.execute('''
        INSERT INTO diabetes_details (consultation_id, therapy, hcl_system_details, hba1c_current, 
                                      hba1c_previous, akutkomplikationen, spätkomplikationen, 
                                      complications_score, antibodies_status, insulin_details, oral_medication_details, 
                                      non_insulin_injection_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (consultation_id, therapy_str, hcl_system_details_str, hba1c_current, hba1c_previous, akutkomplikationen_str, 
              spätkomplikationen_str, complications_score, antibodies_status_str, 
              insulin_details_str, oral_medication_details_str, non_insulin_injection_details_str))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while adding diabetes details: {e}")
    finally:
        conn.close()

def add_cv_risk_factors(consultation_id, cvrisk_data):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    # Handle potential None values in cvrisk_data
    if cvrisk_data['obesity'] is not None:
        obesity_grade = cvrisk_data['obesity']['grade']
        bmi = json.dumps(cvrisk_data['obesity']['bmi']) if cvrisk_data['obesity']['bmi'] is not None else '[]'
    else:
        obesity_grade = '[]'
        bmi = 0  # or use some default value like 'Unknown'

    smoking_status_json = json.dumps(cvrisk_data['smoking_status']['current_status']) if cvrisk_data['smoking_status'] is not None else '[]'

    # Convert the family history dictionary to a JSON string
    family_history_json = json.dumps(cvrisk_data['family_history']) if cvrisk_data['family_history'] else '[]'

    try:
        cursor.execute('''
            INSERT INTO cv_risk_factors (consultation_id, art_hypertension, dyslipidemia, 
            obesity_grade, bmi, smoking_status, family_history) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (consultation_id, bool(cvrisk_data['art_hypertension']), cvrisk_data['dyslipidemia'], obesity_grade, bmi, smoking_status_json, family_history_json))

        conn.commit()
    except Exception as e:
        print(f"Error adding CV risk factors: {e}")
    finally:
        conn.close()


def add_findings(medication_id, consultation_id, medication_name, dosage_morning, 
dosage_midday, dosage_evening, dosage_night, notes):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO medications (consultation_id, medication_name, dosage_morning, 
        dosage_midday, dosage_evening, dosage_night, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (medication_id, consultation_id, medication_name, 
              dosage_morning, dosage_midday, dosage_evening, 
              dosage_night, notes))

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred(3): {e}")

    finally:
        conn.close()
        
def add_scores(medication_id, consultation_id, medication_name, dosage_morning, 
dosage_midday, dosage_evening, dosage_night, notes):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO scores (patient_id, score_type, score_value, date_assessed)
        VALUES (?, ?, ?, ?)
        ''', (patient_id, score_type, score_value, date_assessed))

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred (4): {e}")

    finally:
        conn.close()

def get_all_patients():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM patients')
    fetched_patients = cursor.fetchall()

    conn.close()
    return fetched_patients

# Main execution
def main():
    create_database()  # Create the database and table

    # Retrieving and displaying all patients
    patients = get_all_patients()
    for patient in patients:
        print(patient)
        
if __name__ == "__main__":
    main()