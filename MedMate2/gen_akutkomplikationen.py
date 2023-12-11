import random
from helper_functions import generate_long_random_date_within_1_3_years

def generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors):
    late_complications = ""
    complications_score = 0
    if cvrisk_factors is None:
        cvrisk_factors = {} 

    # Helper function to format complication details as a string
    def format_complication(type, category, date, severity=None, stage=None):
        details = f"{type} ({category})"
        if severity:
            details += f", Severity: {severity}"
        if stage:
            details += f", Stage: {stage}"
        return f"{details}, Date: {date}"

    # Check for dyslipidemia and add KHK if criteria are met
    has_dyslipidemia = cvrisk_factors.get("dyslipidemia", False)
    if has_dyslipidemia and pat_age >= 55 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        late_complications += format_complication("Koronare Herzkrankheit", "macrovascular", date) + "; "
        complications_score += 2

    # Check for dyslipidemia and add pAVK if criteria are met
    is_smoker = cvrisk_factors.get("smoking_status", False)
    if is_smoker and pat_age >= 65 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        late_complications += format_complication("pAVK", "macrovascular", date) + "; "
        complications_score += 2

    # Nephropathy
    if current_hba1c > 7.0 and random.choice([True, False]): 
        stage = random.choice(["G2A1", "G3aA1", "G3bA1", "G4A2", "G5A3"])
        date = generate_long_random_date_within_1_3_years()
        late_complications += format_complication("Nephropathie", "microvascular", date, stage=f"CKD-Stadium {stage}") + "; "
        complications_score += {"G2A1": 1, "G3aA1": 2, "G3bA1": 3, "G4A2": 4, "G5A3": 5}.get(stage, 0)

    # Retinopathy
    if current_hba1c > 7.0 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        severity = random.choice(["milde", "schwere"])  # Randomly select between "mild" and "severe"
        late_complications += format_complication("Retinopathie", "microvascular", date, severity=severity) + "; "
        # Adjust the complications_score based on the severity
        if severity == "milde":
            complications_score += 2
        elif severity == "schwere":
            complications_score += 3

    # Peripheral polyneuropathy
    if current_hba1c > 7.0 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        severity = random.choice(["leichte", "schwere"])
        late_complications += format_complication("periphere Polyneuropathie", "microvascular", date, severity=severity) + "; "
        complications_score += 3

    # Trim the trailing "; " if late_complications is not empty
    if late_complications:
        late_complications = late_complications[:-2]

    return complications_score, late_complications

def generate_hypo_awareness(prim_diagnosis_year):
    acute_complications = []
    clark_score = random.randint(0, 7)

    if random.choice([True, False]) and clark_score >= 4:
        date = generate_long_random_date_within_1_3_years()
        acute_complications.append({
            'type': f"Reduzierte Hypoglykämiewahrnehmung (Clark-Score {clark_score})",
            'date': date
        })

    if random.choice([True, False]):
        num_events = random.randint(1, 3)
        for _ in range(num_events):
            date = generate_long_random_date_within_1_3_years()
            hypoglykemia_grade = random.choice(["II", "III"])
            acute_complications.append({
                'type': f"Hypoglykämie Grad {hypoglykemia_grade}",
                'date': date
            })

    return acute_complications

def generate_ketoacidosis(prim_diagnosis_year):
    acute_complications = []

    if random.choice([True, False]):
        num_events = random.randint(1, 3)
        for _ in range(num_events):
            date = generate_long_random_date_within_1_3_years()
            acute_complications.append({
                'type': "Diabetische Ketoazidose",
                'date': date
            })

    return acute_complications

if __name__ == "__main__":
    prim_diagnosis_year = 1999
    all_acute_complications = []

    all_acute_complications.extend(generate_hypo_awareness(prim_diagnosis_year))
    all_acute_complications.extend(generate_ketoacidosis(prim_diagnosis_year))

    print("Acute Complications: ", all_acute_complications)