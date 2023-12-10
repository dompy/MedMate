# gen_cv_risk_factors.py

import random
import sqlite3
from datetime import datetime
from calc_bmis import calc_bmi

def get_all_patient_ids():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT patient_id FROM patients")
        patient_ids = [row[0] for row in cursor.fetchall()]
        return patient_ids
    finally:
        conn.close()

def get_patient_age(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age FROM patients WHERE patient_id = ?", (patient_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()

def generate_smoking_status(patient_id, pat_age):
    """
    Generate smoking history based on patient's age, with updated formatting for database insertion.
    Returns a dictionary with smoking status details.
    """
    if pat_age is None:
        print("Unable to generate smoking status due to missing age")
        return None
    current_year = datetime.now().year
    
    # Assume a person can start smoking from the age of 15
    max_smoking_years = pat_age - 15
    start_smoking_year = current_year - max_smoking_years
    
    smoking_status = {
        'start_smoking_year': None,
        'stop_smoking_year': None,
        'packs_per_day': None,
        'pack_years': None,
        'current_status': None
    }

    # If age is less than 15, they haven't smoked
    if max_smoking_years <= 0:
        smoking_status['current_status'] = "Non-smoker"
        return smoking_status
    
    # Randomly decide if the patient has stopped smoking
    has_stopped_smoking = random.choice([True, False])

    smoking_status['start_smoking_year'] = start_smoking_year

    if has_stopped_smoking:
        # Randomly decide the year they stopped smoking
        stop_year = random.randint(start_smoking_year, current_year)
        smoking_status['stop_smoking_year'] = stop_year
        
        # Calculate smoking years up to stopping year
        smoking_years = stop_year - start_smoking_year
        
        # Randomly decide packs per day
        packs_per_day = random.uniform(0.2, 3)
        smoking_status['packs_per_day'] = round(packs_per_day, 2)
        
        # Calculate pack years
        pack_years = round(packs_per_day * smoking_years)
        smoking_status['pack_years'] = pack_years
        smoking_status['current_status'] = "Ex-smoker"
    
    else:
        # Calculate smoking pack years
        smoking_years = max_smoking_years
        packs_per_day = random.uniform(0.5, 2)
        smoking_status['packs_per_day'] = round(packs_per_day, 2)

        pack_years = round(packs_per_day * smoking_years)
        smoking_status['pack_years'] = pack_years
        smoking_status['current_status'] = "Current smoker"

    return smoking_status

def generate_obesity():
    obesity = {
        'bmi': None,
        'grade': None,
        'weight': None,
        'height': None,
    }
    
    # Call calc_bmi() and directly get the three values it returns
    weight, height, bmi = calc_bmi()
    obesity['bmi'] = bmi
    obesity['weight'] = weight
    obesity['height'] = height
    
    # Determine the obesity grade based on BMI
    if bmi < 18.5:
        obesity['grade'] = "Untergewicht"
    elif 18.5 <= bmi <= 24.9:
        obesity['grade'] = "Normalgewicht"
    elif 25 <= bmi <= 29.9:
        obesity['grade'] = "Übergewicht"
    elif 30 <= bmi <= 34.9:
        obesity['grade'] = "Adipositas Grad I"
    elif 35 <= bmi <= 39.9:
        obesity['grade'] = "Adipositas Grad II"
    else:
        obesity['grade'] = "Adipositas Grad III"
    
    return obesity

def generate_cvrisk_factors(patient_id):
    pat_age = get_patient_age(patient_id)
    if pat_age is None:
        return None  # If no age found, return None

    smoking_status = generate_smoking_status(patient_id, pat_age)
    obesity = generate_obesity()

    cvrisk_factors = {
        'art_hypertension': random.choice([True, False]),
        'dyslipidemia': random.choice([True, False]),
        'obesity': obesity,
        'smoking_status': smoking_status,
        'family_history': None
    }

    # Familienanamnese
    if random.choice([True, False]):
        events = ["Myokardinfarkt", "Schlaganfall", "zerebrovaskulärer Insult"]
        relatives = ["Vater", "Mutter", "Bruder", "Schwester"]
        event = random.choice(events)
        relative = random.choice(relatives)
        age = random.randint(40, 70)

        # Keep family history as a dictionary
        family_history_dict = {
            'event': event,
            'relative': relative,
            'age': age
        }

        # Assign the dictionary directly to cvrisk_factors
        cvrisk_factors['family_history'] = family_history_dict

    return cvrisk_factors

if __name__ == "__main__":
    patient_ids = get_all_patient_ids()
    for patient_id in patient_ids:

        cvrisk_data = generate_cvrisk_factors(patient_id)
        if cvrisk_data:
            print(f"CV Risk Factors for patient_id {patient_id}: {cvrisk_data}")
        else:
            print(f"No CV Risk Factors data for patient_id {patient_id}")
