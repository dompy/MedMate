import random
import sys
import subprocess
import json
import pint
import datetime
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta


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
    pat_birth_date, age = generate_pat_birth_date()
    pat_ahv_number = generate_ahv_number(ahv_numbers)
    pat_phone_number = generate_phone_number(phone_numbers)
    
    clinic_name = "\033[1;35mFantasie Kliniken Bern\033[0m"
    consultation_date = (datetime.datetime.now() - timedelta(days=random.randint(0, (datetime.datetime.now() - datetime.datetime.strptime(pat_birth_date, "%d.%m.%Y")).days))).strftime("%d.%m.%Y")
    
    report = f"\n{clinic_name}\n"
    report += f"\nFiktive Sprechstunde für Diabetologie vom {consultation_date}\n\n"
    report += f"{first_name} {last_name}, {pat_birth_date}, {pat_gender}\n"
    report += f"{pat_street} {pat_street_number}, {pat_postal_code} {pat_city}, {pat_ahv_number}, {pat_phone_number}\n"
    report += "\n\033[1;34mDiagnosen\033[0m"
    return report, age

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
    ldl_targets = ["< 1.4 mmol/l", "< 1.8 mmol/l", "< 2.4 mmol/l"]
    if random.choice([True, False]):
        ldl_target = random.choice(ldl_targets)
        cvrisk_factors_details.append(f"Dyslipidämie (Ziel-LDL {ldl_target})")
    
    # Adipositas with BMI and date
    adipositas_grades = ["Grad I", "Grad II", "Grad III"]
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if random.choice([True, False]):
        grade = random.choice(adipositas_grades)
        bmi = round(random.uniform(25, 40), 1)  # Random BMI value
        cvrisk_factors_details.append(f"Adipositas {grade} (BMI {bmi} kg/m2 {current_month}/{current_year})")
    
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
    
    return ", ".join(cvrisk_factors_details)

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
    
    # Add "Koronare Herzkrankheit" if there are 2 or more CV risk factors and patient is 50 or older
    if len(cvrisk_factors_details.split(", ")) >= 2 and pat_age >= 50:
        complications_details.append("Koronare Herzkrankheit")

    # Nephropathie with CKD stage and date
    last_screening_date_nephro = generate_random_date_within_1_3_years()
    last_screening_date_retino = generate_random_date_within_1_3_years()
    last_screening_date_füsse = generate_random_date_within_1_3_years()
    ckd_stages = ["G1A1", "G2A1", "G3aA1", "G3bA1", "G4A2", "G5A3"]
    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        stage = random.choice(ckd_stages)
        complications_details.append(f"Nephropathie (CKD-Stadium {stage} zuletzt {last_screening_date_nephro})")
    else:
        complications_details.append(f"Keine Nephropathie (zuletzt {last_screening_date_nephro})")

    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        complications_details.append(f"Retinopathie (zuletzt {last_screening_date_retino})")
    else:
        complications_details.append(f"Keine Retinopathie (zuletzt {last_screening_date_retino})")
    
    # Periphere Polyneuropathie with foot examination date
    if current_hba1c > 7.0 and random.choice([True, False]):  # Higher chance with poor glycemic control
        complications_details.append(f"Periphere Polyneuropathie (Fussuntersuchung zuletzt {last_screening_date_füsse})")
    else:
        complications_details.append(f"Keine periphere Polyneuropathie (Fussuntersuchung zuletzt {last_screening_date_füsse})")

    return "\n- ".join(complications_details)

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
    current_hba1c = round(random.uniform(5.0, 12.9), 1)  # Generate current hba1c
    previous_hba1c = round(random.uniform(5.0, 12.9), 1)  # Generate previous hba1c
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
    
    cvrisk_factors = generate_cvrisk_factors(pat_age)
    details_dict["cvrisk_factors"] = cvrisk_factors

    spätkomplikationen = generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors)
    details_dict["spätkomplikationen"] = spätkomplikationen

    return details_dict

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
        return generate_details_typ1(pat_age, diagnosis)
    # Here you can add other diagnoses and their respective detail generation in the future.
    else:
        return {}

def determine_hba1c_improvement(previous_hba1c_value, current_hba1c_value):
    # Define the threshold for a significant improvement
    significant_improvement_threshold = 2.0  # Adjust the threshold as needed
    significant_weakening_threshold = - 2.0
    # Calculate the difference
    hba1c_improvement = previous_hba1c_value - current_hba1c_value
    # Determine the improvement category
    if hba1c_improvement >= significant_improvement_threshold:
        hba1c_category = "deutlich verbessert"
        hba1c_improvement_wording = random.choice(["deutlich verbessert", "stark verbessert", "signifikant verbessert", "relevant verbessert", "merklich verbessert"])
        return hba1c_improvement_wording, hba1c_category
    elif 0 < hba1c_improvement < significant_improvement_threshold:
        hba1c_category = "verbessert"
        hba1c_improvement_wording = random.choice(["verbessert", "leicht verbessert", "etwas verbessert", "diskret verbessert"])
        return hba1c_improvement_wording, hba1c_category
    elif -0.5 <= hba1c_improvement <= 0.5:
        hba1c_category = "stabil gehalten"
        hba1c_improvement_wording = random.choice(["stabil gehalten", "stabilisiert"])
        return hba1c_improvement_wording, hba1c_category
    elif significant_weakening_threshold < hba1c_improvement < -0.5:
        hba1c_category = "verschlechtert"
        hba1c_improvement_wording = random.choice(["verschlechtert", "etwas verschlechtert", "leicht verschlechtert", "diskret verschlechtert"])
        return hba1c_improvement_wording, hba1c_category
    else:
        hba1c_category = "deutlich verschlechtert"
        hba1c_improvement_wording = random.choice(["deutlich verschlechtert", "stark verschlechtert", "signifikant verschlechtert", "relevant verschlechtert", "merklich verschlechtert"])
        return hba1c_improvement_wording, hba1c_category

def create_beurteilung(previous_hba1c_value, current_hba1c_value):
    hba1c_improvement_wording, hba1c_category = determine_hba1c_improvement(previous_hba1c_value, current_hba1c_value)
    spacy_output = subprocess.run(['python3', '/Users/nomantscho/PycharmProjects/Berichte_Gen/include_spacy6.py', hba1c_category], capture_output=True, text=True)
    # Debugging: print raw outputs
    #print("STDOUT:", spacy_output.stdout)
    #print("STDERR:", spacy_output.stderr)
    second_sentence = spacy_output.stdout.strip()  # Use strip() to remove any leading/trailing whitespaces
    return hba1c_improvement_wording, hba1c_category, second_sentence

# Generate entrance sentence depending on previous hba1c date (represents previous consultation date) "Verlaufskontrolle nach x Wochen/Monaten"
def generate_verlaufskontrolle_entrance(previous_hba1c_date):
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
    # Load patient data
    pat_first_names, pat_last_names, pat_phone_numbers, pat_streets, pat_street_numbers, pat_postal_codes, pat_cities, pat_ahv_numbers = load_patient_data()

    # Generate the patient header
    header, pat_age = generate_patient_header(pat_first_names, pat_last_names, pat_streets, pat_street_numbers, pat_postal_codes, pat_cities, pat_phone_numbers, pat_ahv_numbers)

    # List of possible primary diagnoses
    possible_primary_diagnoses = ["Diabetes Mellitus Typ 1"]

    # Select a primary diagnosis
    primary_diagnosis = select_primary_diagnosis(possible_primary_diagnoses)
    
    # Generate details based on the selected primary diagnosis
    diagnosis_details_dict = generate_details_based_on_diagnosis(primary_diagnosis, pat_age)

    # Assemble the diagnosis details
    assembled_diagnosis_details = assemble_details(diagnosis_details_dict)

    # Call previous HbA1c date for entrance sentence "Verlaufskontrolle nach x Wochen/Monaten"
    current_hba1c_value = diagnosis_details_dict['hba1c']['current']['value']
    previous_hba1c_value = diagnosis_details_dict['hba1c']['previous']['value']
    previous_hba1c_date = diagnosis_details_dict['hba1c']['previous']['date']  

    verlaufskontrolle_sentence = generate_verlaufskontrolle_entrance(previous_hba1c_date)
    hba1c_improvement_wording, hba1c_category, second_sentence = create_beurteilung(previous_hba1c_value, current_hba1c_value)
    # Debugging: print individual components
    # print("Verlaufskontrolle Sentence:", verlaufskontrolle_sentence)
    # print("Second Sentence:", second_sentence)
    # print("HbA1c Category:", hba1c_category)
    # Print the results
    # print(header)
    # print(assembled_diagnosis_details)
    final_output = f"{header}\n{assembled_diagnosis_details}\n{verlaufskontrolle_sentence} {second_sentence} {hba1c_improvement_wording}. "
    print(final_output)

runtimes = 15
for i in range(runtimes):
    main()

