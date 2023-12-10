#gen_prim_dg_details.py
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from gen_cv_risk_factors import generate_cvrisk_factors
from gen_akutkomplikationen import generate_hypo_awareness, generate_ketoacidosis
from gen_spaetkomplikationen import generate_spätkomplikationen
from helper_functions import generate_short_random_date_within_1_3_years, generate_long_random_date_within_1_3_years

def generate_common_details():
    # Generate and return details common to all diabetes diagnoses
    prim_diagnosis_year = random.randint(1975, 2022)
    prim_diagnosis_month = random.randint(1, 12)
    # HbA1c values
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate current hba1c
    previous_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate previous hba1c
    previous_hba1c_date = generate_previous_hba1c_date(previous_hba1c, current_month, current_year)
    return prim_diagnosis_year, prim_diagnosis_month, current_month, current_year, current_hba1c, previous_hba1c, previous_hba1c_date
    
def generate_previous_hba1c_date(prev_hba1c, current_month, current_year):
    # Determine the interval and unit (weeks/months) based on the previous HbA1c
    if prev_hba1c > 12:
        interval = random.randint(2, 4)
        unit = "Wochen"
    elif 10 <= prev_hba1c <= 12:
        interval = random.randint(4, 6)
        unit = "Wochen"
    elif 8 <= prev_hba1c < 10:
        interval = random.randint(6, 8)
        unit = "Wochen"
    elif 7 <= prev_hba1c < 8:
        interval = random.randint(2, 3)
        unit = "Monaten"
    elif 6 <= prev_hba1c < 7:
        interval = random.randint(3, 4)
        unit = "Monaten"
    else:
        interval = random.randint(4, 6)
        unit = "Monaten"

    # Calculate the date for the previous HbA1c based on the interval and unit
    if unit == "Wochen":
        prev_hba1c_date = datetime(current_year, current_month, 1) - timedelta(weeks=interval)
    else:
        prev_hba1c_date = datetime(current_year, current_month, 1) - relativedelta(months=interval)

    return prev_hba1c_date.strftime('%m/%Y')

def get_diagnosis_options():
    diagnosis_options = {
        "Diabetes Mellitus Typ 1": {
            "antibodies": ["GAD", "IA2", "Pankreas-Inselzell", "Zinktransporter-8"],
            "type1_therapies": ["Hybrid-Closed-Loop System", "Basis-Bolus-Therapie"],
            "hcl_systems": ["Minimed Medtronic 780G", "Mylife CamAPS Fx mit Ypsopump", "Diabeloop Accu-Chek insight"],
            "hcl_insulins": ["Lyumjev", "NovoRapid", "Fiasp", "Humalog"]
        },
        "Diabetes Mellitus Typ 2": {
            "type2_therapies": ["Orale Antidiabetika", "Basis-Insulin", "Basis-Bolus-Therapie", "GLP-1-Analogon"],
            "oral_medications": ["Metformin", "Sulfonylharnstoff", "DPP-4-Inhibitor", "SGLT-2-Inhibitor"],
            "non_insulin_injections": ["Ozempic", "Wegovy", "Munjaro"]
        },
        "common_diabetes_options": {        
            "basal_insulins": ["Tresiba", "Toujeo", "Lantus", "Levemir"],
            "bolus_insulins": ["Lyumjev", "NovoRapid", "Fiasp", "Humalog"]
        }
    }
    return diagnosis_options 

def process_type1_diabetes_details(diagnosis_details, all_diagnosis_options, diagnosis_year):
    diagnosis_options_spec = all_diagnosis_options.get("Diabetes Mellitus Typ 1", {})
    diagnosis_options_common = all_diagnosis_options.get("common_diabetes_options", {})

    # Antibodies status
    antibodies = diagnosis_options_spec["antibodies"]
    positive_antibodies = random.sample(antibodies, random.randint(1, len(antibodies)))
    diagnosis_details['antibodies_status'] = {
        'positive': positive_antibodies,
        'negative': [ab for ab in antibodies if ab not in positive_antibodies]
    }
    # Therapy details
    therapy = random.choice(diagnosis_options_spec["type1_therapies"])
    diagnosis_details['therapy'] = therapy
    start_year = random.randint(diagnosis_year, datetime.now().year)
    if therapy == "Hybrid-Closed-Loop System":
        hcl_system = random.choice(diagnosis_options_spec["hcl_systems"])
        hcl_insulin = random.choice(diagnosis_options_spec["hcl_insulins"])
        diagnosis_details['hcl_system_details'] = {
            'system': hcl_system,
            'insulin': hcl_insulin,
            'start_year': start_year
        }
    elif therapy == "Basis-Bolus-Therapie":
        basal_insulin = random.choice(diagnosis_options_common["basal_insulins"])
        bolus_insulin = random.choice(diagnosis_options_common["bolus_insulins"])
        diagnosis_details['insulin_details'] = [
            {'type': 'Basal', 'insulin': basal_insulin, 'start_year': start_year},
            {'type': 'Bolus', 'insulin': bolus_insulin, 'start_year': start_year}
        ]
def process_type2_diabetes_details(diagnosis_details, all_diagnosis_options, diagnosis_year):
    diagnosis_options_spec = all_diagnosis_options.get("Diabetes Mellitus Typ 2", {})
    diagnosis_options_common = all_diagnosis_options.get("common_diabetes_options", {})

    # Therapy details
    type2_therapies = diagnosis_options_spec.get("type2_therapies", [])
    selected_therapies = random.sample(type2_therapies, random.randint(1, len(type2_therapies))) if type2_therapies else []
    diagnosis_details['therapy'] = '; '.join(selected_therapies)
    all_oral_medications = []
    for selected_therapy in selected_therapies:
        start_year = random.randint(diagnosis_year, datetime.now().year)
        if selected_therapy == "Orale Antidiabetika":
            oral_medications_options = diagnosis_options_spec.get("oral_medications", [])
            selected_oad = random.sample(oral_medications_options, random.randint(1, len(oral_medications_options))) if oral_medications_options else []
            diagnosis_details['oral_medication_details'] = '; '.join([f"{oad}, Start Year: {start_year}" for oad in selected_oad])
            all_oral_medications.extend(selected_oad)
        elif selected_therapy == "Basis-Insulin" and "Basis-Bolus-Therapie" not in selected_therapies:
            basal_insulin_option = random.choice(diagnosis_options_common["basal_insulins"])
            diagnosis_details['insulin_details'] = f"Basal: {basal_insulin_option}, Start Year: {start_year}"
        elif selected_therapy == "Basis-Bolus-Therapie" and "Basis-Insulin" not in selected_therapies:
            basal_insulin_option = random.choice(diagnosis_options_common["basal_insulins"])
            bolus_insulin_option = random.choice(diagnosis_options_common["bolus_insulins"])
            diagnosis_details['insulin_details'] = f"Basal: {basal_insulin_option}, Bolus: {bolus_insulin_option}, Start Year: {start_year}"
        elif selected_therapy == "GLP-1-Analogon":
            non_insulin_option = random.choice(diagnosis_options_spec["non_insulin_injections"])
            diagnosis_details['non_insulin_injection_details'] = f"{non_insulin_option}, Start Year: {start_year}"


def generate_details_based_on_diagnosis(primary_diagnosis, pat_age, current_month, current_year):
    # Generate common details
    prim_diagnosis_year, prim_diagnosis_month, _, _, current_hba1c, previous_hba1c, previous_hba1c_date = generate_common_details()

    # Initialize diagnosis details dictionary
    diagnosis_details = {
        'therapy': [],
        'antibodies_status': {},
        'hcl_system_details': {},
        'insulin_details': [],
        'oral_medication_details': [],
        'non_insulin_injection_details': [],
        'akutkomplikationen': [],
        'spätkomplikationen': [],
        'hba1c_current': current_hba1c,
        'hba1c_previous': previous_hba1c,
        'previous_hba1c_date': previous_hba1c_date,
        'cvrisk_factors': generate_cvrisk_factors(pat_age)  # Moved CV risk factors generation here
    }

    # Fetch options for the specified primary diagnosis
    all_diagnosis_options = get_diagnosis_options()

    # Process details based on primary diagnosis
    if primary_diagnosis == "Diabetes Mellitus Typ 1":
        process_type1_diabetes_details(diagnosis_details, all_diagnosis_options, prim_diagnosis_year)
    elif primary_diagnosis == "Diabetes Mellitus Typ 2":
        process_type2_diabetes_details(diagnosis_details, all_diagnosis_options, prim_diagnosis_year)

    # Generate complications and add them to the dictionary
    complications_score, spätkomplikationen = generate_spätkomplikationen(current_hba1c, pat_age, diagnosis_details['cvrisk_factors'])
    akutkomplikationen = generate_hypo_awareness(prim_diagnosis_year) + generate_ketoacidosis(prim_diagnosis_year)

    diagnosis_details.update({
        'complications_score': complications_score,
        'spätkomplikationen': spätkomplikationen,
        'akutkomplikationen': akutkomplikationen
    })

    return diagnosis_details

  
if __name__ == '__main__':
    cvrisk_factors = {'art_hypertension': True, 'dyslipidemia': True, 'obesity': {'bmi': 55.3, 'grade': 'Adipositas Grad III', 'weight': 134.3, 'height': 155.8}, 'smoking_status': {'start_smoking_year': None, 'stop_smoking_year': None, 'packs_per_day': None, 'pack_years': None, 'current_status': 'Non-smoker'}, 'family_history': None}
    bmi = 35
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate current hba1c
    previous_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate previous hba1c
    complications_score = random.uniform(1-12, 1)
    spätkomplikationen = None
    primary_diagnosis = "Diabetes Mellitus Typ 1"
    prim_diagnosis_year = 1999
    prim_diagnosis_month = 6
    pat_age = 33
    previous_hba1c_date = generate_previous_hba1c_date(previous_hba1c, current_month, current_year)   
    generate_details_based_on_diagnosis(primary_diagnosis, 50, 1990, 5, current_month, current_year, current_hba1c, previous_hba1c, previous_hba1c_date)
    #print("generate_prim_diagnosis_details: ", generate_prim_diagnosis_details(primary_diagnosis, prim_diagnosis_year, prim_diagnosis_month, pat_age, current_month, current_year, current_hba1c, previous_hba1c, previous_hba1c_date))