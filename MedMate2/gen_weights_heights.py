import random
def gen_weight_height():
    # Generate a random weight and height
    weight = round(random.uniform(35, 180), 1)  # Weight in kg
    height = round(random.uniform(139, 215), 1)  # Height in cm
    return weight, height

def main():
    weight, height = gen_weight_height()
    print(f"Gewicht: {weight} kg, Grösse: {height} cm")

if __name__ == "__main__":
    main()