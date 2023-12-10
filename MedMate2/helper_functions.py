import random
from datetime import datetime

# long_random_date dd.mm.yyyy
def generate_long_random_date_within_1_3_years():
    # Randomly select a month within the past 12 to 36 months
    months_ago = random.randint(12, 36)
    random_month = datetime.now().month - months_ago
    random_year = datetime.now().year

    # Adjust the month and year if necessary
    while random_month <= 0:
        random_month += 12
        random_year -= 1

    # Generate a random day of the month
    random_day = random.randint(1, 28)  # Simplified to accommodate all months

    # Create long date format
    long_random_date = f"{random_day:02}.{random_month:02}.{random_year}"

    return long_random_date

# short_random_date mm/yyyy
def generate_short_random_date_within_1_3_years(long_date):
    """
    transform long_date to short date
    """
    day, month, year = long_date.split('.')
    short_random_date = f"{month}/{year}"
    return short_random_date

if __name__ == "__main__":
    long_date = generate_long_random_date_within_1_3_years()
    short_date = generate_short_random_date_within_1_3_years(long_date)
    print(f"Long Format: {long_date}")
    print(f"Short Format: {short_date}")
