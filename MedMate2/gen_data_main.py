# gen_data_main.py
from gen_pat_data import generate_patient_data
from gen_prim_diagnosis import generate_primary_diagnosis
from gen_weitere_diagnosen import generate_weitere_diagnosen
from gen_prim_dg_details import generate_common_details, generate_details_based_on_diagnosis
from gen_spaetkomplikationen import generate_spätkomplikationen
from gen_akutkomplikationen import generate_hypo_awareness, generate_ketoacidosis
from helper_functions import generate_long_random_date_within_1_3_years
from datetime import datetime

def generate_all_data(num_patients):
    patients_data = generate_patient_data(num_patients)
    consultations_data = []
    primary_diagnoses_data = []
    secondary_diagnoses_data = []  # This will now be a list of lists
    diabetes_diagnosis_details_data = []
    all_acute_complications = []
    all_late_complications = []

    for patient in patients_data:
        pat_age = patient[3]  # Ensure this correctly fetches the patient's age
        consultation_date = generate_long_random_date_within_1_3_years()
        consultations_data.append(consultation_date)

        primary_diagnosis, diagnosis_year, diagnosis_month = generate_primary_diagnosis()
        primary_diagnosis_data = {'name': primary_diagnosis, 'date': f"{diagnosis_month:02d}/{diagnosis_year}", 'type': 'Primary'}
        primary_diagnoses_data.append(primary_diagnosis_data)

        sec_diagnoses_list = generate_weitere_diagnosen()
        secondary_diagnoses_data.append(sec_diagnoses_list) 

        # Ensure diabetes diagnosis details are generated correctly
        diabetes_diagnosis_details = generate_details_based_on_diagnosis(primary_diagnosis, pat_age, datetime.now().month, datetime.now().year)
        diabetes_diagnosis_details_data.append(diabetes_diagnosis_details)

        # Ensure acute complications are generated correctly
        patient_acute_complications = generate_hypo_awareness(diagnosis_year) + generate_ketoacidosis(diagnosis_year)
        all_acute_complications.append(patient_acute_complications)

        # Ensure late complications are generated correctly
        cvrisk_factors = {}  # Replace with actual data if available
        complications_score, patient_late_complications = generate_spätkomplikationen(diabetes_diagnosis_details['hba1c_current'], pat_age, cvrisk_factors)
        all_late_complications.append(patient_late_complications)

    return patients_data, consultations_data, primary_diagnoses_data, secondary_diagnoses_data, diabetes_diagnosis_details_data, all_acute_complications, all_late_complications, complications_score

def main():
    num_patients = 2
    patients, consultations, primary_diagnoses, secondary_diagnoses, diabetes_details, acute_complications, late_complications = generate_all_data(num_patients)
    print(f"Generated data for {num_patients} patients.")
    print("Acute Complications:", acute_complications)
    print("Late Complications:", late_complications)

if __name__ == "__main__":
    main()