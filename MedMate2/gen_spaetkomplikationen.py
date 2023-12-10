import random
from helper_functions import generate_long_random_date_within_1_3_years

def generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors):
    late_complications = []
    complications_score = 0
    if cvrisk_factors is None:
        cvrisk_factors = {} 

    # Check for dyslipidemia and add KHK if criteria are met
    has_dyslipidemia = cvrisk_factors.get("dyslipidemia", False)
    if has_dyslipidemia and pat_age >= 55 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        late_complications.append({
            "name": "Koronare Herzkrankheit",
            "type": "macrovascular",
            "date": date
        })
        complications_score += 2
        
    # Check for dyslipidemia and add pAVK if criteria are met
    is_smoker = cvrisk_factors.get("smoking_status", False)
    if is_smoker and pat_age >= 65 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        late_complications.append({
            "name": "pAVK",
            "type": "macrovascular",
            "date": date
        })
        complications_score += 2

    # Nephropathy
    if current_hba1c > 7.0 and random.choice([True, False]): 
        stage = random.choice(["G2A1", "G3aA1", "G3bA1", "G4A2", "G5A3"])
        date = generate_long_random_date_within_1_3_years()
        late_complications.append({
            "name": "Nephropathie",
            "type": "microvascular",
            "stage": stage,
            "date": date
        })
        complications_score += {"G2A1": 1, "G3aA1": 2, "G3bA1": 3, "G4A2": 4, "G5A3": 5}.get(stage, 0)
    
    severity = ""
    # Retinopathy
    if current_hba1c > 7.0 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        severity = random.choice(["milde", "schwere"])  # Randomly select between "mild" and "severe"
        late_complications.append({
            "name": "Retinopathie",
            "type": "microvascular",
            "severity": severity,  # Add the randomly selected severity to the dictionary
            "date": date
        })
        # Adjust the complications_score based on the severity
        if severity == "mild":
            complications_score += 2
        elif severity == "schwer":
            complications_score += 3

    # Peripheral polyneuropathy
    if current_hba1c > 7.0 and random.choice([True, False]):
        date = generate_long_random_date_within_1_3_years()
        severity = random.choice(["leicht", "schwer"])
        late_complications.append({
            "name": "periphere Polyneuropathie",
            "type": "microvascular",
            "severity": severity,
            "date": date
        })
        complications_score += 3

    return complications_score, late_complications

if __name__ == "__main__":
    # Example patient details
    current_hba1c = 8.5
    pat_age = 60
    cvrisk_factors = {
        "dyslipidemia": random.choice([True, False]),
        "smoking_status": random.choice([True, False])  # Example smoking status
    }

    # Generate late complications
    complications_score, late_complications = generate_spätkomplikationen(current_hba1c, pat_age, cvrisk_factors)

    print("Late Complications Score:", complications_score)
    print("Late Complications:")
    for complication in late_complications:
        # Construct complication description
        complication_desc = f"- Name: {complication['name']}\n" if 'name' in complication else ''
        complication_desc += f"- Type: {complication['type']}\n" if 'type' in complication else ''
        complication_desc += f"- Stage: {complication.get('stage', '')}\n" if 'stage' in complication else ''
        complication_desc += f"- Severity: {complication.get('severity', '')}\n" if 'severity' in complication else ''
        complication_desc += f"- Date: {complication['date']}\n" if {complication['date']} else ''
        print(complication_desc.strip())