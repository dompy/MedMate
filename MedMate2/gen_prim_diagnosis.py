# gen_prim_diagnosis.py

import random
from datetime import datetime
def generate_primary_diagnosis():
    # List of possible primary diagnoses
    possible_primary_diagnoses_list = ["Diabetes Mellitus Typ 1", "Diabetes Mellitus Typ 2"]
    primary_diagnosis = random.choice(possible_primary_diagnoses_list)
        
    # date (Generate and return details common to all diagnoses)
    current_month = datetime.now().month
    current_year = datetime.now().year
    prim_diagnosis_year = random.randint(1975, current_year)
    if prim_diagnosis_year == current_year: # make sure no date in future is generated
        prim_diagnosis_month = random.randint(1, current_month)
    else:
        prim_diagnosis_month = random.randint(1, 12)    

    return primary_diagnosis, prim_diagnosis_year, prim_diagnosis_month

def main():
    primary_diagnosis, prim_diagnosis_year, prim_diagnosis_month = generate_primary_diagnosis()
    print(f"Hauptdiagnose: {primary_diagnosis}, ED {prim_diagnosis_month:02d}/{prim_diagnosis_year}")

if __name__ == "__main__":
    main()