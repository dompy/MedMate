from gen_weights_heights import gen_weight_height

def calc_bmi():
    weight, height = gen_weight_height()
    height_in_meters = height / 100  # Convert height from cm to meters
    bmi = round(weight / (height_in_meters ** 2), 1)
    return weight, height, bmi

def main():
    # Generate weight and height
    weight, height = gen_weight_height()

    # Calculate BMI based on generated weight and height
    bmi = calc_bmi(weight, height)

    print(f"BMI {bmi} kg/m², weight {weight} kg, height {height} cm")

if __name__ == "__main__":
    main() 
