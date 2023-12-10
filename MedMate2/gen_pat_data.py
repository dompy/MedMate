import random
from dateutil.relativedelta import relativedelta
from datetime import datetime
from faker import Faker

ethnicities = {
    "White": 1,
    "Indian": 2,
    "Pakistani": 3,
    "Bangladeshi": 4,
    "Other Asian": 5,
    "Black Caribbean": 6,
    "Black African": 7,
    "Chinese": 8,
    "Other ethnic": 9
}

canton_codes = {
    "Aargau": "AG",
    "Appenzell Innerrhoden": "AI",
    "Appenzell Ausserrhoden": "AR",
    "Bern": "BE",
    "Basel-Landschaft": "BL",
    "Basel-Land": "BL",
    "Basel-Stadt": "BS",
    "Freiburg": "FR",
    "Genf": "GE",
    "Glarus": "GL",
    "Graubünden": "GR",
    "Jura": "JU",
    "Luzern": "LU",
    "Neuenburg": "NE",
    "Nidwalden": "NW",
    "Obwalden": "OW",
    "Sankt Gallen": "SG",
    "St. Gallen": "SG",
    "Schaffhausen": "SH",
    "Solothurn": "SO",
    "Schwyz": "SZ",
    "Thurgau": "TG",
    "Tessin": "TI",
    "Uri": "UR",
    "Waadt": "VD",
    "Wallis": "VS",
    "Zug": "ZG",
    "Zürich": "ZH",
    "Fürstentum Liechtenstein": "FL"
}
# Function to generate fake male and female patient data
def generate_patient_data(num_patients):
    patients_list = []
    fake = Faker('de_CH')
    for _ in range(num_patients):
        for sex in ['M', 'F']:
            if sex == 'M':
                first_name = fake.first_name_male()
                last_name = fake.last_name()
            else:
                first_name = fake.first_name_female()
                last_name = fake.last_name()
            dob = fake.date_of_birth()
            age = relativedelta(datetime.now(), dob).years  
            street_name = fake.street_name().title()
            building_number = fake.building_number()
            postcode = fake.postcode()
            city_name = fake.city()
            canton_name = fake.canton_name()
            canton_code = canton_codes[canton_name]
            phone_number = fake.numerify('+41 79 ### ## ##')
            ahv_number = fake.ssn()
            email = fake.email()

            patients_list.append((first_name, last_name, dob, age, sex, street_name, building_number, postcode, city_name, canton_name, canton_code, phone_number, ahv_number, email))

    return patients_list

def main():
    # Generate fake patient data
    fake_patients = generate_patient_data(5)  # generate data for x patients

    # For demonstration, print the generated data
    # for patient in fake_patients:
    #    print(patient)   

# Main execution
# In the script where generate_patient_data is defined
if __name__ == "__main__":
    test_patients = generate_patient_data(50)
    print(f"Total patients generated: {len(test_patients)}")
    male_count = sum(1 for patient in test_patients if patient[-10] == 'M')  # Assuming sex is the second last element
    female_count = sum(1 for patient in test_patients if patient[-10] == 'F')
    print(f"Males: {male_count}, Females: {female_count}")
