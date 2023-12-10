#gen_weitere_diagnosen.py

import random

def generate_weitere_diagnosen():
    weitere_diagnosen = []
    
    b_AF = random.choice([True, False])  # Atrial fibrillation status
    b_corticosteroids = random.choice([True, False])  # Corticosteroids usage
    b_impotence2 = random.choice([True, False])
    b_ra = random.choice([True, False])
    b_sle = random.choice([True, False])
    b_atypicalantipsy = random.choice([True, False])
    b_migraine = random.choice([True, False])
    # If a condition is true, append a dictionary with the diagnosis details
    if b_AF:
        weitere_diagnosen.append({"name": "Vorhofflimmern", "date": '', "type": "Secondary"})
    if b_corticosteroids:
        weitere_diagnosen.append({"name": "Dauersteroidtherapie", "date": '', "type": "Secondary"})
    if b_impotence2:
        weitere_diagnosen.append({"name": "Erektile Dysfunktion", "date": '', "type": "Secondary"})      
    if b_ra:
        weitere_diagnosen.append({"name": "Rheumatoide Arthritis", "date": '', "type": "Secondary"})      
    if b_sle:
        weitere_diagnosen.append({"name": "Systemischer Lupus Erythematodes", "date": '', "type": "Secondary"})
    if b_atypicalantipsy:
        weitere_diagnosen.append({"name": "Psychiatrische Erkrankung (unter atypischen Antipsychotika)", "date": '', "type": "Secondary"}) 
    if b_migraine:
        weitere_diagnosen.append({"name": "Migräne", "date": '', "type": "Secondary"})
    # add more conditions to include other diagnoses as needed

    return weitere_diagnosen

if __name__ == "__main__":
    print(generate_weitere_diagnosen())