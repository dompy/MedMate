# main.py
from db_operations import create_database, add_patient, add_consultation, add_diagnosis, add_diabetes_details, add_cv_risk_factors
from gen_data_main import generate_all_data
from gen_cv_risk_factors import generate_cvrisk_factors

def main():
    create_database()
    num_patients = 500
    patients_data, consultations_data, primary_diagnoses_data, secondary_diagnoses_data, diabetes_diagnosis_details_data, all_acute_complications, all_late_complications, complication_score = generate_all_data(num_patients)
    for patient, consultation_date, primary_diagnosis_dict, sec_diagnoses_list, diabetes_detail in zip(patients_data, consultations_data, primary_diagnoses_data, secondary_diagnoses_data, diabetes_diagnosis_details_data):
        patient_id = add_patient(patient)

        consultation_id = add_consultation(patient_id, consultation_date)
        add_diagnosis(consultation_id, primary_diagnosis_dict['name'], primary_diagnosis_dict['date'], primary_diagnosis_dict['type'])

        for sec_diagnosis_dict in sec_diagnoses_list:
            if isinstance(sec_diagnosis_dict, dict):
                add_diagnosis(consultation_id, sec_diagnosis_dict['name'], sec_diagnosis_dict['date'], sec_diagnosis_dict['type'])

        if diabetes_detail:
            # Pass all required details to add_diagnosis_details
            add_diabetes_details(
                consultation_id,
                diabetes_detail['therapy'],
                diabetes_detail['antibodies_status'],
                diabetes_detail['hcl_system_details'],
                diabetes_detail['insulin_details'],
                diabetes_detail['oral_medication_details'],
                diabetes_detail['non_insulin_injection_details'],
                diabetes_detail['complications_score'],
                diabetes_detail['spätkomplikationen'],
                diabetes_detail['hba1c_current'],
                diabetes_detail['hba1c_previous'],
                diabetes_detail['hba1c_previous_date'],
                diabetes_detail['akutkomplikationen']
            )

        cvrisk_data = generate_cvrisk_factors(patient_id)
        if cvrisk_data:
            add_cv_risk_factors(consultation_id, cvrisk_data)

if __name__ == "__main__":
    main()
