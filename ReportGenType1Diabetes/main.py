import random
import sys
import subprocess
import json
import pint
import datetime
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta
from qrisk3male import cvd_male_raw
from qrisk3female import cvd_female_raw
ureg = pint.UnitRegistry()
def load_patient_data():
# Provided patient data lists
    first_names = {
        "m": [
            "Liam", "Noah", "Harper", "Ethan", "William", "Benjamin", "Lucas", "Henry", 
            "Alexander", "Sebastian", "Oliver", "Daniel", "Matthew", "Jack", "Aiden", 
            "Owen", "Samuel", "Joseph", "John", "David", "Wyatt", "Carter", "Jayden", 
            "Levi", "Gabriel", "Julian", "Max", "Adrian", "Tristan", "Xavier"
        ],
        "w": [
            "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", 
            "Evelyn", "Simbuala", "Aleksandra", "Lily", "Zoe", "Chloe", "Madison", 
            "Ella", "Avery", "Scarlett", "Grace", "Layla", "Riley", "Zoey", "Nora", 
            "Elizabeth", "Luna", "Sofia", "Aubrey", "Camila", "Aria", "Leah"
        ]
    }
    # Last names
    last_names = ["Müller", "Meier", "Schmid", "Fischer", "Meyer", "Widmer", "Schneider", "Schwarz", "Huber", "Hoffmann", "Zürcher", "Bumwadba", "Kirosczekci"]

    # Phone numbers
    phone_numbers = [f"+41 {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}" for _ in range(11)]

    # Patient streets
    streets = ["Bahnhofstrasse", "Rütistrasse", "Schulweg", "Dorfplatz", "Bergweg", "Hauptstrasse", "Wiesenweg", "Sonnhalde", "Alpenblick", "Birkenweg", "Talstrasse"]
    street_numbers = ["13", "5a", "663", "51c-d", "16", "104", "993", "22", "7", "12", "1B"]

    # Patient Postal codes and cities
    postal_codes = [f"{random.randint(1000, 9999)}" for _ in range(11)]
    cities = ["Zürichberg", "Luganolake", "Genevaville", "Bernside", "Lucernpoint", "Baselbay", "Lausannepark", "Fribourgpeak", "Neuchâtelview", "St.Gallenshore", "Bellinzonagate"]

    # Patient Social security numbers
    ahv_numbers = [f"756.{random.randint(1000, 9999)}.{random.randint(1000, 9999)}.{random.randint(10, 99)}" for _ in range(11)]

    return first_names, last_names, phone_numbers, streets, street_numbers, postal_codes, cities, ahv_numbers

def generate_name(first_names, last_names):
    pat_gender = random.choice(["m", "w"])
    if pat_gender == "m":
        pat_gender_long = "Herr"
    else:
        pat_gender_long = "Frau"
    first_name = random.choice(first_names[pat_gender])
    last_name = random.choice(last_names)

    return first_name, last_name, pat_gender

def generate_address(streets, street_numbers, postal_codes, cities):
    """Generate patient address."""
    pat_street = random.choice(streets)
    pat_street_number = random.choice(street_numbers)
    pat_postal_code = random.choice(postal_codes)
    pat_city = random.choice(cities)
    return pat_street, pat_street_number, pat_postal_code, pat_city

def generate_phone_number(phone_numbers):
    """Generate patient phone number."""
    pat_phone_number = random.choice(phone_numbers)
    return pat_phone_number

def generate_ahv_number(ahv_numbers):
    """Generate patient ahv-number."""
    pat_ahv_number = random.choice(ahv_numbers)
    return pat_ahv_number

def generate_pat_birth_date():
    """
    Generate a random birth date in dd.mm.yyyy format.
    """
    current_year = datetime.datetime.now().year
    
    # Define a reasonable age range for patients
    pat_min_age = 17
    pat_max_age = 95
    
    # Randomly select an age and compute the birth year
    pat_age = random.randint(pat_min_age, pat_max_age)
    pat_birth_year = current_year - pat_age
    
    # Randomly select a month and day
    pat_birth_month = random.randint(1, 12)
    
    # Adjust the day range based on the month (e.g., February can have 28/29 days)
    if pat_birth_month in [4, 6, 9, 11]:
        birth_day = random.randint(1, 30)
    elif pat_birth_month == 2:
        if (pat_birth_year % 4 == 0 and pat_birth_year % 100 != 0) or (pat_birth_year % 400 == 0):  # Leap year
            birth_day = random.randint(1, 29)
        else:
            birth_day = random.randint(1, 28)
    else:
        birth_day = random.randint(1, 31)
    
    # Format the date
    pat_birth_date = f"{birth_day:02d}.{pat_birth_month:02d}.{pat_birth_year}"
    
    return pat_birth_date, pat_age

def generate_patient_header(first_names, last_names, streets, street_numbers, postal_codes, cities, phone_numbers, ahv_numbers):
    """Generate patient report."""
    first_name, last_name, pat_gender = generate_name(first_names, last_names)
    pat_street, pat_street_number, pat_postal_code, pat_city = generate_address(streets, street_numbers, postal_codes, cities)
    pat_birth_date, pat_age = generate_pat_birth_date()
    pat_ahv_number = generate_ahv_number(ahv_numbers)
    pat_phone_number = generate_phone_number(phone_numbers)
    
    clinic_name = "\033[1;35mFantasie Kliniken Bern\033[0m"
    consultation_date = (datetime.datetime.now() - timedelta(days=random.randint(0, (datetime.datetime.now() - datetime.datetime.strptime(pat_birth_date, "%d.%m.%Y")).days))).strftime("%d.%m.%Y")
    
    report = f"\n{clinic_name}\n"
    report += f"\nFiktive Sprechstunde für Diabetologie vom {consultation_date}\n\n"
    report += f"{first_name} {last_name}, {pat_birth_date}, {pat_gender}\n"
    report += f"{pat_street} {pat_street_number}, {pat_postal_code} {pat_city}, {pat_ahv_number}, {pat_phone_number}\n"
    report += "\n\033[1;34mDiagnosen\033[0m"
    return report, pat_age, pat_gender

#type-1-diagnose helper functions
def generate_akutkomplikationen(prim_diagnosis_year):
    """
    Generate details for acute complications with formatted date. If a complication didn't occur, return None.
    """
    # Randomly decide if reduced hypo awareness is present
    clark_score = random.randint(0,7)

    if (random.choice([True, False]) and clark_score >= 4):
        clark_score_date = generate_random_date_within_1_3_years() # Randomly pick date within the past 3 years for the last clark-score calculation 
        clark_score_output = f"Reduzierte Hypoglykämiewahrnehmung (Clark-Score {clark_score} Punkte {clark_score_date})"
    else:
        clark_score_output =""

    # Hypoglykemia (Hypoglykämie)
    hypoglykemia_grades = ["II", "III"]
    hypoglykemia_details = []

    if random.choice([True, False]):  # Randomly decide if Hypoglykämie occurred

        num_events = random.randint(1, 3)  # decide the number of events
        events_dates = []  # to store the dates for sorting later
        
        for _ in range(num_events):
            random.shuffle(hypoglykemia_grades)
            hypoglykemia_grade = hypoglykemia_grades[_ % len(hypoglykemia_grades)]

            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            current_day = datetime.datetime.now().day
            
            hypoglykemia_year = random.randint(prim_diagnosis_year, current_year) 
            if hypoglykemia_year == current_year:
                hypoglykemia_month = random.randint(1, current_month) 
            else:
                hypoglykemia_month = random.randint(1, 12)

            # Adjust the day range based on the month
            if hypoglykemia_month in [4, 6, 9, 11]:
                hypoglykemia_day = random.randint(1, 30)
            elif hypoglykemia_month == 2:
                if (hypoglykemia_year % 4 == 0 and hypoglykemia_year % 100 != 0) or (hypoglykemia_year % 400 == 0):  # Leap year
                    hypoglykemia_day = random.randint(1, 29)
                else:
                    hypoglykemia_day = random.randint(1, 28)
            else:
                hypoglykemia_day = random.randint(1, 31)

            hypoglykemia_date = datetime.datetime(hypoglykemia_year, hypoglykemia_month, hypoglykemia_day)
            events_dates.append((hypoglykemia_date, hypoglykemia_grade))
            
        # Sort the dates in descending order
        events_dates.sort(reverse=True)

        for idx, (date, grade) in enumerate(events_dates):
            # Determine if hypoglykemia_date is within the last 8 weeks
            eight_weeks_ago = datetime.datetime.now() - timedelta(weeks=8)
            
            if date > eight_weeks_ago:
                hypoglykemia_display_date = date.strftime('%d.%m.%Y')
            else:
                hypoglykemia_display_date = f"{date.month:02d}/{date.year}"

            # If it's the first (most recent) in the list and there's more than 1 event, add "zuletzt"
            prefix = "zuletzt " if idx == 0 and len(events_dates) > 1 else ""
            hypoglykemia_details.append(f"Grad {grade} {prefix}{hypoglykemia_display_date}")

    if len(hypoglykemia_details) > 1:
        hypo_output = f"Rezidivierende Hypoglykämien ({', '.join(hypoglykemia_details)})"
    elif hypoglykemia_details:
        hypo_output = f"Hypoglykämie {hypoglykemia_details[0].split()[1]} (zuletzt {hypoglykemia_details[0].split()[2]})"
    else:
        hypo_output = ""
        
    # Diabetic ketoacidosis (Diabetische Ketoazidose)
    ketoacidosis_details = []

    if random.choice([True, False]):  # Randomly decide if Diabetische Ketoazidose occurred
        
        num_events = random.randint(1, 3)  # decide the number of events
        events_dates = []  # to store the dates for sorting later

        for _ in range(num_events):
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            current_day = datetime.datetime.now().day

            ketoacidosis_year = random.randint(prim_diagnosis_year, current_year)
            if ketoacidosis_year == current_year:
                ketoacidosis_month = random.randint(1, current_month)
            else:
                ketoacidosis_month = random.randint(1, 12)
            
            # Adjust the day range based on the month
            if ketoacidosis_month in [4, 6, 9, 11]:
                ketoacidosis_day = random.randint(1, 30)
            elif ketoacidosis_month == 2:
                if (ketoacidosis_year % 4 == 0 and ketoacidosis_year % 100 != 0) or (ketoacidosis_year % 400 == 0):  # Leap year
                    ketoacidosis_day = random.randint(1, 29)
                else:
                    ketoacidosis_day = random.randint(1, 28)
            else:
                ketoacidosis_day = random.randint(1, 31)

            ketoacidosis_date = datetime.datetime(ketoacidosis_year, ketoacidosis_month, ketoacidosis_day)
            events_dates.append(ketoacidosis_date)
            
        # Sort the dates in descending order
        events_dates.sort(reverse=True)

        for idx, date in enumerate(events_dates):
            # Determine if ketoacidosis_date is within the last 8 weeks
            eight_weeks_ago = datetime.datetime.now() - timedelta(weeks=8)
            
            if date > eight_weeks_ago:
                ketoacidosis_display_date = date.strftime('%d.%m.%Y')
            else:
                ketoacidosis_display_date = f"{date.month:02d}/{date.year}"

            # If it's the first (most recent) in the list and there's more than 1 event, add "zuletzt"
            prefix = "zuletzt " if idx == 0 and len(events_dates) > 1 else ""
            ketoacidosis_details.append(f"{prefix}{ketoacidosis_display_date}")

    if len(ketoacidosis_details) == 1:
        keto_output = f"Diabetische Ketoazidose (zuletzt {ketoacidosis_details[0]})"
    elif len(ketoacidosis_details) > 1:
        keto_output = f"Rezidivierende diabetische Ketoazidosen ({', '.join(ketoacidosis_details)})"
    else:
        keto_output = ""

    return hypo_output, keto_output, clark_score_output

def generate_smoking_status(pat_age):
    """
    Generate smoking history based on patient's age, with updated formatting.
    """
    current_year = datetime.datetime.now().year
    
    # Assume a person can start smoking from the age of 15
    max_smoking_years = pat_age - 15
    start_smoking_year = current_year - max_smoking_years
    
    # If age is less than 15, they haven't smoked
    if max_smoking_years <= 0:
        return "Nieraucher"
    
    # Randomly decide if the patient has stopped smoking
    has_stopped_smoking = random.choice([True, False])
    
    if has_stopped_smoking:
        # Randomly decide the year they stopped smoking
        stop_year = random.randint(start_smoking_year, current_year)
        
        # Calculate smoking years up to stopping year
        smoking_years = stop_year - start_smoking_year
        
        # Randomly decide packs per day (1 pack = 20 cigarettes, so between 0.5 to 2 packs per day)
        packs_per_day = random.uniform(0.2, 3)
        
        # Calculate pack years
        pack_years = int(round(packs_per_day * smoking_years))
        
        return f"St. n. Nikotinabusus ({pack_years} pack years, sistiert {stop_year})"
    
    else:
        # Calculate smoking pack years as before
        smoking_years = max_smoking_years
        packs_per_day = random.uniform(0.5, 2)
        pack_years = int(round(packs_per_day * smoking_years))
        
        return f"Nikotinabusus ({pack_years} pack years {current_year})"

def generate_cvrisk_factors(pat_age):
    """
    Generate details for additional cardiovascular risk factors.
    """
    cvrisk_factors_details = []
    
    # Arterielle Hypertonie
    if random.choice([True, False]):
        cvrisk_factors_details.append("Arterielle Hypertonie")
    
    # Dyslipidämie with LDL target
    if random.choice([True, False]):
        cvrisk_factors_details.append("Dyslipidämie")
    

    # Adipositas with BMI and date
    adipositas_grades = ["Grad I", "Grad II", "Grad III"]
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    bmi = round(random.uniform(20, 24), 1)  # Random BMI value
    if random.choice([True, False]):
        grade = random.choice(adipositas_grades)
        bmi = round(random.uniform(25, 40), 1)  # Random BMI value
        cvrisk_factors_details.append(f"Adipositas {grade} (BMI {bmi} kg/m² {current_month}/{current_year})")
    
    # Nikotinabusus with pack years and date or smoking history if they've stopped
    smoking_status = generate_smoking_status(pat_age)
    cvrisk_factors_details.append(smoking_status)
    
    # Positive Familienanamnese with event and relative's age
    events = ["Myokardinfarkt", "Schlaganfall", "zerebrovaskulärer Insult"]
    relatives = ["Vater", "Mutter", "Bruder", "Schwester"]
    if random.choice([True, False]):
        event = random.choice(events)
        relative = random.choice(relatives)
        age = random.randint(40, 70)  # Random age for the relative's event
        cvrisk_factors_details.append(f"positive Familienanamnese ({event} bei {relative} im Alter von {age} Jahren)")
    
    return ", ".join(cvrisk_factors_details), bmi

def generate_qrisk3_score_m(pat_age, weitere_diagnosen, primary_diagnosis, bmi, systolic, ldl_cholesterol, is_smoker, has_smoking_history, cvrisk_factors):
    # Boolean indicators from weitere_diagnosen
    b_AF = int("Vorhofflimmern" in weitere_diagnosen)
    b_atypicalantipsy = int("Antipsychotika" in weitere_diagnosen)
    b_corticosteroids = int("Dauersteroidtherapie" in weitere_diagnosen)
    b_impotence2 = int("Erektile Dysfunktion" in weitere_diagnosen)
    b_migraine = int("Migräne" in weitere_diagnosen)
    b_ra = int("Rheumatoide Arthritis" in weitere_diagnosen)
    b_renal = 0  # Default value, assuming no renal disease
    b_sle = int("Lupus" in weitere_diagnosen)
    b_semi = random.choice([1, 0])
    b_treatedhyp = int("Arterielle Hypertonie" in cvrisk_factors)
    b_type1 = int("Typ 1" in primary_diagnosis)
    b_type2 = int("Typ 2" in primary_diagnosis)
    ethrisk = random.choice([1, 0])  # Ethrisk value can be refined further
    fh_cvd = int("positive Familienanamnese" in cvrisk_factors)
    
    # Additional parameters for QRISK3
    rati = ldl_cholesterol / random.uniform(1.2, 2.2)  # Ratio calculation
    sbps5 = random.randint(2, 20)  # Systolic blood pressure standard deviation
    smoke_cat = 3 if is_smoker else (1 if has_smoking_history else 0)
    surv = 10  # Survival rate (can be adjusted if needed)
    town = 0   # Town value (can be refined further)

    # Call QRISK3 function with these parameters
    qrisk3_score = cvd_male_raw(pat_age, b_AF, b_atypicalantipsy, b_corticosteroids, b_impotence2, b_migraine, b_ra, b_renal, b_semi, b_sle, b_treatedhyp, b_type1, b_type2, bmi, ethrisk, fh_cvd, rati, systolic, sbps5, smoke_cat, surv, town)
    
    return qrisk3_score

def generate_qrisk3_score_w(pat_age, weitere_diagnosen, primary_diagnosis, bmi, systolic, ldl_cholesterol, is_smoker, has_smoking_history, cvrisk_factors):
    # Boolean indicators from weitere_diagnosen
    b_AF = int("Vorhofflimmern" in weitere_diagnosen)
    b_atypicalantipsy = int("Antipsychotika" in weitere_diagnosen)
    b_corticosteroids = int("Dauersteroidtherapie" in weitere_diagnosen)
    b_migraine = int("Migräne" in weitere_diagnosen)
    b_ra = int("Rheumatoide Arthritis" in weitere_diagnosen)
    b_renal = 0  # Default value, assuming no renal disease
    b_sle = int("Lupus" in weitere_diagnosen)
    b_semi = random.choice([1, 0])
    b_treatedhyp = int("Arterielle Hypertonie" in cvrisk_factors)
    b_type1 = int("Typ 1" in primary_diagnosis)
    b_type2 = int("Typ 2" in primary_diagnosis)
    ethrisk = random.choice([1, 0])  # Ethrisk value can be refined further
    fh_cvd = int("positive Familienanamnese" in cvrisk_factors)
    
    # Additional parameters for QRISK3
    rati = ldl_cholesterol / random.uniform(1.2, 2.2)  # Ratio calculation
    sbps5 = random.randint(2, 20)  # Systolic blood pressure standard deviation
    smoke_cat = 3 if is_smoker else (1 if has_smoking_history else 0)
    surv = 10  # Survival rate (can be adjusted if needed)
    town = 0   # Town value (can be refined further)

    # Call QRISK3 function with these parameters
    qrisk3_score_w = cvd_female_raw(pat_age, b_AF, b_atypicalantipsy, b_corticosteroids, b_migraine, b_ra, b_renal, b_semi, b_sle, b_treatedhyp, b_type1, b_type2, bmi, ethrisk, fh_cvd, rati, systolic, sbps5, smoke_cat, surv, town)
    
    return qrisk3_score_w

def generate_agla_category(pat_age, prim_diagnosis_year, has_diabetes, hba1c_score, complications_score, spätkomplikationen, fh_status):
    # Constants for AGLA categories
    AGLA_CATEGORIES = {
        "good_control_less_10_years_no_endorganschaden_no_main_risk": "AGLA-Score: moderates Risiko",
        "good_control_less_10_years_no_endorganschaden_one_main_risk": "AGLA-Score: hohes Risiko",
        "good_control_less_10_years_no_endorganschaden_multiple_main_risks": "AGLA-Score: sehr hohes Risiko",
        "not_optimal_or_longer_10_years_no_main_risk": "AGLA-Score: hohes Risiko",
        "not_optimal_or_longer_10_years_with_main_risk": "AGLA-Score: sehr hohes Risiko",
        "with_ASCVD_or_severe_endorganschaden": "AGLA-Score: sehr hohes Risiko"
    }

    current_year = datetime.datetime.now().year
    years_since_diagnosis = current_year - prim_diagnosis_year

    if pat_age > 40 and has_diabetes:
        has_endorganschaden = complications_score > 3
        has_ASCVD = "Koronare Herzkrankheit" in spätkomplikationen

        # Check for presence of ASCVD or severe end-organ damage
        if has_endorganschaden or has_ASCVD:
            return AGLA_CATEGORIES["with_ASCVD_or_severe_endorganschaden"]

        # Determine if well-controlled diabetes for less than 10 years
        if years_since_diagnosis < 10 and hba1c_score in [1, 2]:
            if fh_status == 'None':
                return AGLA_CATEGORIES["good_control_less_10_years_no_endorganschaden_no_main_risk"]
            elif fh_status in ['HeFH', 'HoFH']:
                return AGLA_CATEGORIES["good_control_less_10_years_no_endorganschaden_one_main_risk"]
            else:
                return AGLA_CATEGORIES["good_control_less_10_years_no_endorganschaden_multiple_main_risks"]

        # Determine if not optimal control or longer duration
        elif years_since_diagnosis >= 10 or hba1c_score > 2:
            if fh_status == 'None':
                return AGLA_CATEGORIES["not_optimal_or_longer_10_years_no_main_risk"]
            else:
                return AGLA_CATEGORIES["not_optimal_or_longer_10_years_with_main_risk"]

    return ""


    
def generate_blood_pressure(pat_age, pat_gender, has_diabetes, has_obesity, has_smoking_history):
    """
    Generates a realistic blood pressure reading based on patient's age, gender, diabetes, and obesity status.
    Blood pressure is represented as a tuple (systolic, diastolic).

    Args:
    age (int): The age of the patient.
    gender (str): The gender of the patient ('m' for male, 'w' for female).
    has_diabetes (bool): Whether the patient has diabetes.
    has_obesity (bool): Whether the patient is obese.

    Returns:
    tuple: A tuple representing systolic and diastolic blood pressure (mmHg).
    """
    # Base blood pressure range (systolic, diastolic)
    bp_range = {
        "normal": (90, 120),
        "high": (121, 140)
    }
    # Select 'high' range for approximately 1 in 15 patients
    bp_key = "high" if random.randint(1, 15) == 1 else "normal"
    # Adjustments for age, gender, diabetes, and obesity
    age_adjustment = (pat_age - 30) // 10 * 5 if pat_age > 30 else 0
    gender_adjustment = 5 if pat_gender == "m" and pat_age < 60 else -5 if pat_gender == "w" and pat_age > 60 else 0
    diabetes_adjustment = 10 if has_diabetes else 0
    obesity_adjustment = 10 if has_obesity else 0
    smoking_adjustment = 5 if has_smoking_history else 0
    # Calculate blood pressure
    systolic = random.randint(*bp_range[bp_key]) + age_adjustment + gender_adjustment + diabetes_adjustment + obesity_adjustment + smoking_adjustment
    diastolic = random.randint(60, 80) + age_adjustment // 2

    # Ensure systolic is greater than diastolic
    systolic = max(systolic, diastolic + 10)

    return systolic, diastolic, bp_key

def def_familial_hypercholesterolemia():
    """
    Randomly determines if a patient has a family history of Familial Hypercholesterolemia (FH).

    Returns:
    str: 'HeFH' for Heterozygous FH, 'HoFH' for Homozygous FH, or 'None' for no FH.
    """
    # Probabilities based on prevalence
    probability_HeFH = 1 / 225  # Average of 1 in 200 and 1 in 250
    probability_HoFH = 1 / 230000  # Average of 1 in 160,000 and 1 in 300,000

    # Randomly determine if patient has FH
    if random.random() < probability_HoFH:
        return 'HoFH'
    elif random.random() < probability_HeFH:
        return 'HeFH'
    else:
        return 'None'

def generate_ldl_cholesterol(pat_age, pat_gender, has_obesity, is_smoker, has_diabetes, family_history):
    # Base LDL range in mmol/L
    base_ldl = random.uniform(1.3, 3.4)  # Roughly equivalent to 50-130 mg/dL

    # Modifiable risk factor adjustments
    diet_adjustment = random.uniform(0, 0.52)  # Assumes diet impact
    obesity_adjustment = 0.26 if has_obesity else 0  # Assumes obesity impact
    smoking_adjustment = 0.13 if is_smoker else 0  # Assumes smoking impact
    alcohol_adjustment = random.uniform(0, 0.26)  # Assumes alcohol impact
    diabetes_adjustment = 0.26 if has_diabetes else 0 # Assumes alcohol impact

    # Non-modifiable risk factor adjustments
    age_gender_adjustment = ((pat_age - 20) // 10 * 0.13) if pat_age > 20 else 0  # Equivalent to 0.13 mmol/l per decade
    age_gender_adjustment += -0.26 if pat_gender == "w" and pat_age < 50 else 0.26  # Adjusts for menopause in women

    # Familial Hypercholesterolemia adjustments
    if family_history == 'HeFH':
        # LDL levels for Heterozygous FH (HeFH)
        base_ldl = random.uniform(4.9, 8.0)
    elif family_history == 'HoFH':
        # LDL levels for Homozygous FH (HoFH)
        base_ldl = random.uniform(13.0, 20.0)

    # Calculate total LDL in mmol/L
    total_ldl = round(base_ldl + diet_adjustment + obesity_adjustment + smoking_adjustment + alcohol_adjustment + diabetes_adjustment + age_gender_adjustment, 1)

    return round(total_ldl, 2)

def calculate_target_ldl(qrisk3):
    if qrisk3 < 10:
        target_ldl = 2.4  # Target LDL for low risk
        risiko = "niedriges Risiko"
    elif 10 <= qrisk3 <= 20:
        target_ldl = 1.8  # Target LDL for moderate risk
        risiko = "hohes Risiko"
    else:
        target_ldl = 1.4  # Target LDL for high risk
        risiko = "sehr hohes Risiko"
    return target_ldl, risiko

def generate_random_date_within_1_3_years(): #random date generation for last complication screening
    """
    Generate a random date within the last 1-3 years in the format MM/YYYY.
    """
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    # Randomly select a month within the past 36 months
    months_ago = random.randint(1, 36)
    random_month = current_month - months_ago
    random_year = current_year

    # Adjust the month and year if necessary
    while random_month <= 0:
        random_month += 12
        random_year -= 1
    
    return f"{random_month:02}/{random_year}"

def generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors_details):
    """
    Generate details for late complications.
    """
    complications_details = []
    cv_risk_factors = cvrisk_factors_details.split(", ")
    complications_score = 0
    # Check for dyslipidemia and add KHK if criteria are met
    has_dyslipidemia = "Dyslipidämie" in cv_risk_factors
    if len(cv_risk_factors) >= 2 and pat_age >= 55:
        if not has_dyslipidemia:
            cv_risk_factors.append("Dyslipidämie")
        complications_details.append("Koronare Herzkrankheit")
        complications_score = complications_score + 1

    # Update the cvrisk_factors_details string
    cvrisk_factors_details = ", ".join(cv_risk_factors)

    # Nephropathie with CKD stage and date
    last_screening_date_nephro = generate_random_date_within_1_3_years()
    last_screening_date_retino = generate_random_date_within_1_3_years()
    last_screening_date_füsse = generate_random_date_within_1_3_years()
    ckd_stages = ["G1A1", "G2A1", "G3aA1", "G3bA1", "G4A2", "G5A3"]
    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        stage = random.choice(ckd_stages)
        if "G2" in stage:
                complications_score = complications_score + 1
        elif "G3a" in stage:
                complications_score = complications_score + 2
        elif "G3b" in stage:
                complications_score = complications_score + 3
        elif "G4" in stage:
            complications_score = complications_score + 4 
        elif "G5" in stage:
            complications_score = complications_score + 5              
        complications_details.append(f"Nephropathie (CKD-Stadium {stage} zuletzt {last_screening_date_nephro})")
    else:
        complications_details.append(f"Keine Nephropathie (zuletzt {last_screening_date_nephro})")

    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        complications_details.append(f"Retinopathie (zuletzt {last_screening_date_retino})")
        complications_score = complications_score + 3
    else:
        complications_details.append(f"Keine Retinopathie (zuletzt {last_screening_date_retino})")
    
    # Periphere Polyneuropathie with foot examination date
    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        complications_details.append(f"Periphere Polyneuropathie (Fussuntersuchung zuletzt {last_screening_date_füsse})")
        complications_score = complications_score + 3
    else:
        complications_details.append(f"Keine periphere Polyneuropathie (Fussuntersuchung zuletzt {last_screening_date_füsse})")

    return complications_score, "\n- ".join(complications_details)

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
        prev_hba1c_date = datetime.datetime(current_year, current_month, 1) - timedelta(weeks=interval)
    else:
        prev_hba1c_date = dt(current_year, current_month, 1) - relativedelta(months=interval)

    return prev_hba1c_date.strftime('%m/%Y')

def generate_details_typ1(pat_age, primary_diagnosis):
    details_dict = {
        "diagnosis": None,
        "antibodies": None,
        "therapy": None,
        "hba1c": {
            "current": None,
            "previous": None
        },
        "akutkomplikationen": [],
        "cvrisk_factors": None,
        "spätkomplikationen": None
    }

    # Type-1 diagnose details
    prim_diagnosis_year = random.randint(1975, 2022)
    prim_diagnosis_month = random.randint(1, 12)

    # Antibodies
    antibodies = ["GAD", "IA2", "Pankreas-Inselzell", "Zinktransporter-8"]
    positive_antibodies = random.sample(antibodies, random.randint(1, len(antibodies)))
    negative_antibodies = [ab for ab in antibodies if ab not in positive_antibodies]

    # Therapy details
    type1_therapies = ["Hybrid-Closed-Loop System"]
    hcl_systems = ["Minimed Medtronic 780G", "Mylife CamAPS Fx mit Ypsopump", "Diabeloop Accu-Chek insight"]
    hcl_insulins = ["Lyumjev", "NovoRapid", "Fiasp", "Humalog"]
    hcl_system = random.choice(hcl_systems)
    hcl_insulin = random.choice(hcl_insulins)
    hcl_start_year = random.randint(prim_diagnosis_year, 2022)

    # AGP-Details of HCL-System 
    
    # HbA1c values
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    current_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate current hba1c
    previous_hba1c = round(random.uniform(4.5, 12.9), 1)  # Generate previous hba1c
    previous_hba1c_date = generate_previous_hba1c_date(previous_hba1c, current_month, current_year)

   # Populate the hba1c nested dictionary
    details_dict["hba1c"]["current"] = {
        "value": current_hba1c,
        "date": f"{current_month:02d}/{current_year}"
    }
    details_dict["hba1c"]["previous"] = {
        "value": previous_hba1c,
        "date": previous_hba1c_date
    }

    details_dict["diagnosis"] = f"1. {primary_diagnosis} (ED {prim_diagnosis_month:02d}/{prim_diagnosis_year})"
    details_dict["antibodies"] = f"- {'-, '.join(positive_antibodies)}-Autoantikörper positiv {prim_diagnosis_year}"
    if negative_antibodies:
        details_dict["antibodies"] += f", {'-, '.join(negative_antibodies)}-Autoantikörper negativ {prim_diagnosis_year}"
    details_dict["therapy"] = f"Therapie\n- {random.choice(type1_therapies)} ({hcl_system}) seit {hcl_start_year}, Insulin {hcl_insulin}"

    # Generate Akutkomplikationen
    hypo_output, keto_output, clark_score_output = generate_akutkomplikationen(prim_diagnosis_year)

    if clark_score_output:
        details_dict["akutkomplikationen"].append(clark_score_output)
    if hypo_output:
        details_dict["akutkomplikationen"].append(hypo_output)
    if keto_output:
        details_dict["akutkomplikationen"].append(keto_output)
    
    cvrisk_factors, bmi = generate_cvrisk_factors(pat_age)
    details_dict["cvrisk_factors"] = cvrisk_factors
    

    complications_score, spätkomplikationen = generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors)
    details_dict["spätkomplikationen"] = spätkomplikationen

    return details_dict, current_hba1c, cvrisk_factors, bmi, complications_score, spätkomplikationen, prim_diagnosis_year

def assemble_details(details_dict):
    assembled_details = []
    
    if details_dict["diagnosis"]:
        assembled_details.append(details_dict["diagnosis"])
    if details_dict["antibodies"]:
        assembled_details.append(details_dict["antibodies"])
    if details_dict["therapy"]:
        assembled_details.append(details_dict["therapy"])

    if details_dict["hba1c"]["current"] and details_dict["hba1c"]["previous"]:
        hba1c_current = details_dict["hba1c"]["current"]
        hba1c_previous = details_dict["hba1c"]["previous"]
        assembled_details.append(f"- HbA1c {hba1c_current['value']} % {hba1c_current['date']} ({hba1c_previous['value']} % {hba1c_previous['date']})")

    # Add Akutkomplikationen only if they exist
    if details_dict["akutkomplikationen"]:
        akut_details = "Akutkomplikationen\n" + "\n".join([f"- {ak}" for ak in details_dict["akutkomplikationen"]])
        assembled_details.append(akut_details)
    
    if details_dict["cvrisk_factors"]:
        assembled_details.append("Weitere kardiovaskuläre Risikofaktoren\n- " + details_dict["cvrisk_factors"])
    if details_dict["spätkomplikationen"]:
        assembled_details.append("Spätkomplikationen\n- " + details_dict["spätkomplikationen"])
    return "\n".join(assembled_details)

def select_primary_diagnosis(possible_primary_diagnoses):
    """
    Randomly select a primary diagnosis from the list of possible diagnoses.
    """
    return random.choice(possible_primary_diagnoses)

def generate_details_based_on_diagnosis(diagnosis, pat_age):
    """
    Generate details based on the selected primary diagnosis.
    """
    if diagnosis == "Diabetes Mellitus Typ 1":
        details_dict, current_hba1c, cvrisk_factors, bmi, complications_score, spätkomplikationen, prim_diagnosis_year = generate_details_typ1(pat_age, diagnosis)
        return details_dict, current_hba1c, cvrisk_factors, bmi, complications_score, spätkomplikationen, prim_diagnosis_year
    else:
        return {}, None, None, None, None, None


def generate_weitere_diagnosen():
    weitere_diagnosen = []
    
    b_AF = random.randint(0, 15) # Atrial fibrillation status
    b_corticosteroids = random.randint(0, 15)  # Corticosteroids usage
    b_impotence2 = random.randint(0, 12)
    b_ra = random.randint(0, 80)
    b_sle = random.randint(0, 150)
    b_atypicalantipsy = random.randint(0, 15)
    b_migraine = random.randint(0, 15)
    # Add 'Vorhofflimmern' to weitere_diagnosen if atrial fibrillation is true
    if b_AF == 1:
        weitere_diagnosen.append("Vorhofflimmern")
    if b_corticosteroids == 1:
        weitere_diagnosen.append("Dauersteroidtherapie")
    if b_impotence2 == 1:
        weitere_diagnosen.append("Erektile Dysfunktion")      
    if b_ra == 1:
        weitere_diagnosen.append("Rheumatoide Arthritis")       
    if b_sle == 1:
        weitere_diagnosen.append("Systemischer Lupus Erythematodes")    
    if b_atypicalantipsy == 1:
        weitere_diagnosen.append("Psychiatrische Erkrankung (unter atypischen Antipsychotika)")    
    if b_migraine == 1:
        weitere_diagnosen.append("Migräne")
    # Here, you can add more conditions to include other diagnoses as needed

    return weitere_diagnosen

def assemble_weitere_diagnosen(weitere_diagnosen):
    """
    Assembles a list of additional diagnoses into a formatted string.

    Args:
        weitere_diagnosen (list): A list of additional diagnoses.

    Returns:
        str: A formatted string of additional diagnoses.
    """
    if weitere_diagnosen:
        formatted_diagnoses = "\n".join([f"- {diagnose}" for diagnose in weitere_diagnosen])
        return f"\n\nWeitere Diagnosen\n{formatted_diagnoses}"
    else:
        return ""
    
def determine_hba1c_score(current_hba1c_value, previous_hba1c_value, hba1c_improvement_category):
    # Initial values
    hba1c_score = 0
    hba1c_wording = ""

    if 4.5 <= current_hba1c_value <= 5.9:
        hba1c_score = 1
        hba1c_wording = "sehr gut"
        if previous_hba1c_value < 6 and current_hba1c_value < 6:
            if hba1c_improvement_category in ["verbessert", "deutlich verbessert"]:
                hba1c_wording = "weiterhin sehr gut"
    elif 5.9 < current_hba1c_value <= 6.9:
        hba1c_score = 2
        hba1c_wording = "gut"
        if previous_hba1c_value < 7 and current_hba1c_value < 7:
            if hba1c_improvement_category in ["verbessert", "deutlich verbessert"]:
                hba1c_wording = "weiterhin gut"        
    elif 6.9 < current_hba1c_value <= 7.9:
        hba1c_score = 3
        hba1c_wording = "zufriedenstellend"
        if previous_hba1c_value < 8 and current_hba1c_value < 8:
            if hba1c_improvement_category in ["verbessert", "deutlich verbessert"]:
                hba1c_wording = "weiterhin zufriedenstellend"          
    elif current_hba1c_value > 7.9:
        hba1c_score = 4
        hba1c_wording = "optimierungsfähig"
        if previous_hba1c_value > 8 and current_hba1c_value > 8:
            if hba1c_improvement_category in ["verbessert", "deutlich verbessert"]:
                hba1c_wording = "weiterhin optimierungsfähig"   
    return hba1c_score, hba1c_wording

def determine_hba1c_improvement(previous_hba1c_value, current_hba1c_value):
    # Define the threshold for a significant improvement
    significant_improvement_threshold = 2.0  # Adjust the threshold as needed
    significant_weakening_threshold = - 2.0
    # Calculate the difference
    hba1c_improvement = previous_hba1c_value - current_hba1c_value
    # Determine the improvement category
    if hba1c_improvement >= significant_improvement_threshold:
        hba1c_improvement_category = "deutlich verbessert"
        return hba1c_improvement_category
    elif 0 < hba1c_improvement < significant_improvement_threshold:
        hba1c_improvement_category = "verbessert"
        return hba1c_improvement_category
    elif -0.5 <= hba1c_improvement <= 0.5:
        hba1c_improvement_category = "stabil gehalten"
        return hba1c_improvement_category
    elif significant_weakening_threshold < hba1c_improvement < -0.5:
        hba1c_improvement_category = "verschlechtert"
        return hba1c_improvement_category
    else:
        hba1c_improvement_category = "deutlich verschlechtert"
        return hba1c_improvement_category

def create_beurteilung(previous_hba1c_value, current_hba1c_value):
    """
    Generates a clinical assessment based on HbA1c values.

    This function takes previous and current HbA1c values, determines the improvement or decline in HbA1c, runs a subprocess to generate a sentence based on the HbA1c category, and returns the assessment and category along with the generated sentence.

    Args:
        previous_hba1c_value (float): The previous HbA1c value.
        current_hba1c_value (float): The current HbA1c value.

    Returns:
        tuple: A tuple containing:
            - hba1c_improvement_wording (str): A description of the HbA1c change.
            - hba1c_improvement_category (str): The category of HbA1c change.
            - second_sentence (str): A sentence generated based on the HbA1c category.
    """
    hba1c_improvement_category = determine_hba1c_improvement(
        previous_hba1c_value,
        current_hba1c_value
    )
    
    # Convert float values to strings
    prev_hba1c_str = str(previous_hba1c_value)
    curr_hba1c_str = str(current_hba1c_value)

    spacy_output = subprocess.run(
        ['python3', 'sentence2.py', hba1c_improvement_category, prev_hba1c_str, curr_hba1c_str],
        capture_output=True,
        text=True,
        check=False
    )
    sentence2 = spacy_output.stdout.strip()

    return hba1c_improvement_category, sentence2

# Generate entrance sentence depending on previous hba1c date (represents previous consultation date)
# "Verlaufskontrolle nach x Wochen/Monaten"
def generate_verlaufskontrolle_entrance(previous_hba1c_date):
    """
    Generates an entrance sentence for a medical report based on the time elapsed since 
    the previous HbA1c test date.

    This function takes the date of the previous HbA1c test, 
    calculates the time interval in weeks or months from the current date, 
    and generates an entrance sentence indicating the time elapsed since the last test.

    Args:
        previous_hba1c_date (str): The date of the previous HbA1c test in 
        '%m/%Y' format (e.g., '04/2021').

    Returns:
        str: An entrance sentence for the medical report, 
        indicating the interval since the last HbA1c test in weeks or months.
    """
    # Convert string date to datetime object assuming format '%m/%Y'
    previous_date = dt.strptime(previous_hba1c_date, '%m/%Y')
    current_date = datetime.datetime.now()

    # Calculate the difference in weeks
    difference = current_date - previous_date
    weeks_difference = difference.days // 7

    # Determine the appropriate unit and interval
    if weeks_difference <= 7:
        interval = weeks_difference
        unit = "Wochen" if interval > 1 else "Woche"
    else:
        # Convert weeks to months for intervals longer than 7 weeks
        months_difference = weeks_difference // 4
        interval = months_difference
        unit = "Monaten" if interval > 1 else "Monat"

    # Create the entrance sentence
    entrance_sentence = f"\n\033[1;34mBeurteilung\033[0m\nVerlaufskontrolle nach {interval} {unit}."

    return entrance_sentence

def main():
    """
    Main function to generate a medical report for a patient.

    This function performs several steps to create a comprehensive medical report:
    1. Loads patient data.
    2. Generates the patient header including age.
    3. Selects a primary diagnosis from a list of possible diagnoses.
    4. Generates details based on the selected primary diagnosis and patient's age.
    5. Assembles these details into a structured report.
    6. Generates an entrance sentence for the report based on the previous HbA1c date.
    7. Creates a sentence assessing the patient's HbA1c improvement.
    8. Combines all elements into the final report and prints it.
    """
    # Load patient data
    (
        pat_first_names,
        pat_last_names,
        pat_phone_numbers,
        pat_streets,
        pat_street_numbers,
        pat_postal_codes,
        pat_cities,
        pat_ahv_numbers
    ) = load_patient_data()

    # Generate the patient header
    header, pat_age, pat_gender = generate_patient_header(
        pat_first_names,
        pat_last_names,
        pat_streets,
        pat_street_numbers,
        pat_postal_codes,
        pat_cities,
        pat_phone_numbers,
        pat_ahv_numbers
    )

    # List of possible primary diagnoses
    possible_primary_diagnoses = ["Diabetes Mellitus Typ 1"]

    # Select a primary diagnosis
    primary_diagnosis = select_primary_diagnosis(possible_primary_diagnoses)

    # Generate details based on the selected primary diagnosis
    diagnosis_details_dict, current_hba1c, cvrisk_factors, bmi, complications_score, spätkomplikationen, prim_diagnosis_year = generate_details_based_on_diagnosis(primary_diagnosis, pat_age)
    # Assemble the diagnosis details
    assembled_diagnosis_details = assemble_details(diagnosis_details_dict)
    
    weitere_diagnosen = generate_weitere_diagnosen()    
    assembled_weitere_diagnosen = assemble_weitere_diagnosen(weitere_diagnosen)
    # Determine diabetes and obesity status
    has_diabetes = "Diabetes" in primary_diagnosis # Adjust this based on your diagnosis logic
    has_obesity = "Adipositas" in cvrisk_factors  # Adjust this based on your risk factor logic
    has_smoking_history = "Nikotinabusus" in cvrisk_factors or "Nikotin" in cvrisk_factors  # Adjust based on smoking history
    is_smoker = "St. n. Nikotinabusus" not in cvrisk_factors # Adjust based on if current smoker
    systolic, diastolic, bp_key = generate_blood_pressure(pat_age, pat_gender, has_diabetes, has_obesity, has_smoking_history)

    # Include a sentence about high blood pressure if applicable
    if bp_key == "high":
        blood_pressure = f"Der Blutdruck ({systolic}/{diastolic} mmHg) ist deutlich erhöht."
    else:
        blood_pressure = f"Der heutige Blutdruck liegt bei {systolic}/{diastolic} mmHg."

    # Determine familial hypercholesterolemia status
    fh_status = def_familial_hypercholesterolemia()
    # Generate LDL cholesterol
    ldl_cholesterol = generate_ldl_cholesterol(pat_age, pat_gender, has_obesity, is_smoker, has_diabetes, fh_status)

    # LDL Cholesterol Text Output
    if fh_status == 'HoFH':
        ldl_text = f"Der LDL-Cholesterinspiegel ist deutlich zu hoch ({ldl_cholesterol} mmol/L), womit eine homozygote familiäre Hypercholesterinämie überprüft werden sollte "
    elif fh_status == 'HeFH':
        ldl_text = f"Der LDL-Cholesterinspiegel ist sehr hoch ({ldl_cholesterol} mmol/L) und lässt differentialdiagnostisch an eine heterozygote familiäre Hypercholesterinämie denken "
    elif ldl_cholesterol > 4.9:
        ldl_text = f"Der LDL-Cholesterinspiegel ist erhöht ({ldl_cholesterol} mmol/L) "
    else:
        ldl_text = f"Der LDL-Cholesterinspiegel liegt bei {ldl_cholesterol} mmol/L "

    # Call generate_qrisk3_score male
    if pat_gender == "m":
        qrisk3_score = generate_qrisk3_score_m(
            pat_age, weitere_diagnosen, primary_diagnosis, bmi, systolic, 
            ldl_cholesterol, is_smoker, has_smoking_history, cvrisk_factors
        )  
        # Call generate_qrisk3_score female
    if pat_gender == "w":
        qrisk3_score = generate_qrisk3_score_w(
            pat_age, weitere_diagnosen, primary_diagnosis, bmi, systolic, 
            ldl_cholesterol, is_smoker, has_smoking_history, cvrisk_factors
        )  
    

    target_ldl, risiko = calculate_target_ldl(qrisk3_score)
    # Assuming cvrisk_factors is a string containing the risk factors
    if "Dyslipidämie" in cvrisk_factors:
        # Replace existing 'Dyslipidämie' with updated info
        cvrisk_factors = cvrisk_factors.replace("Dyslipidämie", f"Dyslipidämie (Ziel-LDL < {target_ldl} mmol/l)")
    else:
        # Append new 'Dyslipidämie' info if it doesn't exist
        if cvrisk_factors:  # if cvrisk_factors is not empty
            cvrisk_factors += f", Dyslipidämie (Ziel-LDL < {target_ldl} mmol/l)"
        else:
            cvrisk_factors = f"Dyslipidämie (Ziel-LDL < {target_ldl} mmol/l)"

    # Update the details_dict with the modified cvrisk_factors
    diagnosis_details_dict["cvrisk_factors"] = cvrisk_factors

    # Now, reassemble the details with the updated cvrisk_factors
    assembled_diagnosis_details = assemble_details(diagnosis_details_dict)

    target_ldl_text = (f"Ziel-LDL < {target_ldl} mmol/l")
    qrisk3_text = (f"QRISK3-Score: {qrisk3_score:.0f}%, {risiko}")
    # Call previous HbA1c date for entrance sentence "Verlaufskontrolle nach x Wochen/Monaten"
    current_hba1c_value = diagnosis_details_dict['hba1c']['current']['value']
    previous_hba1c_value = diagnosis_details_dict['hba1c']['previous']['value']
    previous_hba1c_date = diagnosis_details_dict['hba1c']['previous']['date']  

    # Call determine_hba1c_score to calculate the score and wording
    hba1c_improvement_category, sentence2 = create_beurteilung(previous_hba1c_value, current_hba1c_value)
    hba1c_score, hba1c_wording = determine_hba1c_score(current_hba1c_value, previous_hba1c_value, hba1c_improvement_category)
    agla_score = generate_agla_category(pat_age, prim_diagnosis_year, has_diabetes, hba1c_score, complications_score, spätkomplikationen, fh_status)
    agla_text = agla_score
    # Check the hba1c_wording
    if hba1c_wording == "weiterhin optimierungsfähig":
        # Define the list of possible improvement wordings
        bereits_dict = ["bereits ", "jedoch bereits ", "bereits schon ", "schon ", "allerdings schon ", "allerdings "]
        bereits = random.choice(bereits_dict)          
        improvement_wordings = [
        "deutlich verbessert", "stark verbessert", "signifikant verbessert", 
        "relevant verbessert", "merklich verbessert", "verbessert", 
        "etwas verbessert", "diskret verbessert", "etwas optimiert"
        ]
      
        # Check and prepend "bereits" to the improvement wording in the sentence
        for wording in improvement_wordings:
            if wording in sentence2:
                sentence2 = sentence2.replace(wording, bereits + wording)
                break  # Assuming only one improvement wording appears in the sentence


    ist_dict = ["ist", "zeigt sich"]
    ist = random.choice(ist_dict)
    hba1c_sentence = f"Die Blutzuckereinstellung {ist} {hba1c_wording}."
    if agla_score != "":
        cv_risk_bracket = f"({qrisk3_text}; {agla_text}, {target_ldl_text}). "
    else:
        cv_risk_bracket = f"({qrisk3_text}, {target_ldl_text}). "

    entrance_sentence = generate_verlaufskontrolle_entrance(previous_hba1c_date)

    final_output = (
    f"{header}\n"
    f"{assembled_diagnosis_details}"
    f"{assembled_weitere_diagnosen}\n"
    f"{entrance_sentence} "
    f"{hba1c_sentence} "
    f"{sentence2}\n"
    f"{ldl_text}"
    f"{cv_risk_bracket}"
    f"{blood_pressure} "
    )

    print(final_output)

main()