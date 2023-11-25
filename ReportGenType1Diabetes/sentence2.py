"""
This module generates sentences based on HbA1c improvement categories for diabetes management 
reports.

It utilizes natural language processing (NLP) tools and German grammar rules to construct sentences 
that reflect the patient's HbA1c level changes. The module can be run independently 
for testing or used as part of a larger system to automatically generate parts of medical reports.

Arguments:
- hba1c_improvement_category (str): A category indicating the change in HbA1c levels 
  (e.g., 'verbessert', 'stabil gehalten').

Returns:
- A sentence (str) that describes the HbA1c level change in a medically appropriate
  and grammatically correct manner.
"""
import sys
import random
import re
import spacy
import language_tool_python

# Load the German language model
nlp = spacy.load('de_core_news_lg')

# Create a tool for the German language
tool = language_tool_python.LanguageTool('de-DE')

# Define article adjustments based on gender and case
articles = {
    'Nominativ': {'Masc': 'der', 'Fem': 'die', 'Neut': 'das', 'Plur': 'die'},
    'Akkusativ': {'Masc': 'den', 'Fem': 'die', 'Neut': 'das', 'Plur': 'die'},
    'Dativ': {'Masc': 'dem', 'Fem': 'der', 'Neut': 'dem', 'Plur': 'den'},
    'Genitiv': {'Masc': 'des', 'Fem': 'der', 'Neut': 'des', 'Plur': 'der'},
}
def apply_german_grammar(local_sentence, entrance_preposition, main_noun_gender, main_noun_number, helper_noun_gender, entrance_adverbs, local_main_noun, main_meal, glucose_control):
    """
    This function applies German grammar rules to a sentence.

    Parameters:
    local_sentence (str): The sentence to which the grammar rules will be applied.
    entrance_preposition (str): The preposition at the beginning of the sentence.
    main_noun_gender (str): The gender of the main noun.
    main_noun_number (str): The number of the main noun (singular or plural).
    helper_noun_gender (str): The gender of the helper noun.
    helper_noun_number (str): The number of the helper noun (singular or plural).
    entrance_adverbs (list): The list of adverbs at the beginning of the sentence.
    local_main_noun (str): The main noun in the sentence.
    main_meal (str): The main meal in the sentence.

    Returns:
    str: The sentence after applying the German grammar rules.
    """
    # Define entrance cases for adverbs
    adverb_cases = {
        "Dativ": {
            "prepositions": ["Aufgrund", "Nach", "Unter", "Bei", "Mit", "Dank", "Wegen", "Mit Hilfe"],
            "suffixes": {"Fem": "er", "Masc": "em", "Neut": "em", "Plur": "en"},
        },
        "Genitiv": {
            "prepositions": ["Durch"],
            "suffixes": {"Fem": "e", "Masc": "en", "Neut": "es", "Plur": "e"},
        },
        # Add other cases as needed
    }
    time_prepositions = ["zu", "bei", "vor", "nach"]

    # Determine the case based on the entrance preposition
    case = None
    for c, details in adverb_cases.items():
        if entrance_preposition in details["prepositions"]:
            case = c
            break

    if case is None:
        case = "Nominativ"  # Default case

    # Apply case suffix to the adverb
    for case, details in adverb_cases.items():
        if entrance_preposition in details["prepositions"]:
            suffix = details["suffixes"].get(helper_noun_gender, "")
            for adverb in entrance_adverbs:
                pattern = r'\b' + re.escape(adverb) + r'\b'
                local_sentence = re.sub(pattern, adverb + suffix, local_sentence)

    # Define the article for the main noun based on the number and gender
    main_noun_suffix = ""
    if main_noun_number == "Sing":
        if main_noun_gender == "Masc":
            main_noun_article = "des"
            # Append 's' only if the noun does not end with 's'
            if not local_main_noun.endswith("s"):
                main_noun_suffix = "s"
        elif main_noun_gender == "Fem":
            main_noun_article = "der"
    elif main_noun_number == "Plur":
        main_noun_article = "der"
        main_noun_suffix = ""
    else:
        main_noun_article = "DER"  # default main_noun article written CAPS for clarity
        main_noun_suffix = "EN"

    # Apply the article to the main noun + suffix
    local_sentence = local_sentence.replace(local_main_noun, f"{main_noun_article} {local_main_noun}{main_noun_suffix}")


    # Determine the gender and number of the main_meal
    doc_main_meal = nlp(main_meal)
    main_meal_gender, main_meal_number = None, None
    for token in doc_main_meal:
        if token.pos_ == "NOUN":
            main_meal_gender = token.morph.get("Gender")[0]
            main_meal_number = "Plur" if token.morph.get("Number")[0] == "Plur" else "Sing"

    # Determine the correct article for the meal noun based on gender and number
    meal_article = articles["Dativ"].get(main_meal_gender, "dem")
    if main_meal_number == "Plur":
        meal_article = articles["Dativ"].get("Plur", "den")

    # Add time preposition and article for the meal and check for invalid combination (e.g. Bolus after meal, Bolus-Eat-Intervall after meal and so on)
    valid_combination = False
    while not valid_combination:
        time_prep = random.choice(time_prepositions)
        full_prep_phrase = f"{time_prep} {meal_article} {main_meal}"
        contracted_prep_phrase = apply_contractions(full_prep_phrase)

        valid_combination = is_valid_combination(time_prep, local_main_noun)

    # Construct the sentence with the meal name and its article
    local_sentence = local_sentence.replace(main_meal, contracted_prep_phrase)

    # Determine the gender and number of local_glucose_control
    glucose_control_gender, glucose_control_number, _ = determine_noun_attributes(glucose_control, "")

    # Determine the correct article for the glucose control noun
    glucose_control_article = get_article(glucose_control_gender, glucose_control_number, "Nominativ")

    # Apply the article to the glucose control noun in the sentence
    local_sentence = local_sentence.replace(glucose_control, f"{glucose_control_article} {glucose_control}")

    return local_sentence, time_prep

def is_valid_combination(local_time_prep, local_main_noun):
    """
    Checks if the combination of time preposition, main noun, and main meal is valid.

    Parameters:
    local_time_prep (str): The time preposition used in the sentence.
    local_main_noun (str): The main noun in the sentence.
    main_meal (str): The main meal in the sentence.

    Returns:
    bool: True if the combination is valid, False otherwise.
    """
    # Define invalid combinations
    invalid_combinations = {
        "Bolus": {
            "time_prepositions": ["nach"]
        },
        "Bolus-Ess-Abstand": {
            "time_prepositions": ["nach"]
        }, 
        "Mahlzeiten-Bolus": {
            "time_prepositions": ["nach"]
        },
        "Kohlenhydratmenge": {
            "time_prepositions": ["nach", "vor"]
        },
        "Kohlenhydratfaktoren": {
            "time_prepositions": ["nach"]
        },
        "Kohlenhydratzufuhr": {
            "time_prepositions": ["nach"]
        },
        "Korrekturfaktor": {
            "time_prepositions": ["nach"]
        }        
    }

    # Check for invalid combinations
    if local_main_noun in invalid_combinations:
        invalid_time_preps = invalid_combinations[local_main_noun]["time_prepositions"]
        if local_time_prep in invalid_time_preps:
            return False
    
    return True


# Function to get the correct article
def get_article(noun_gender, noun_number, noun_case):
    """
    Determines the correct German article for a given noun based on its gender, number, and case.

    Parameters:
    noun_gender (str): The gender of the noun (Masc, Fem, Neut).
    noun_number (str): The number of the noun (Sing, Plur).
    noun_case (str): The grammatical case of the noun (Nominativ, Akkusativ, Dativ, Genitiv).

    Returns:
    str: The correct German article for the noun.
    """
    if noun_number == 'Plur':
        return articles[noun_case]['Plur']
    else:
        return articles[noun_case].get(noun_gender, "")


def apply_contractions(local_sentence):
    """
    This function applies contractions to a sentence.
    It replaces long forms of certain phrases with their contracted forms.
    """
    contractions = {
        "bei dem": "beim",
        "zu dem": "zum",
        "zu der": "zur",
        "in dem": "im",
        "an dem": "am"
        # Add more contractions here as needed
    }
    for long_form, short_form in contractions.items():
        local_sentence = local_sentence.replace(long_form, short_form)

    return local_sentence

# Function to analyze and print details of each word in the sentence using Spacy
def analyze_sentence(local_sentence, local_main_noun, local_helper_noun, local_entrance_adverb):
    """
    Analyzes a sentence and prints grammatical information for specified words.

    The function uses spaCy to parse the sentence and extract grammatical details
    such as part of speech and morphology for the main noun, helper noun, and
    entrance adverb. It then prints this information along with the sentence in a
    randomly chosen color for clarity.

    Parameters:
    local_sentence (str): The sentence to be analyzed.
    local_main_noun (str): The main noun in the sentence for analysis.
    local_helper_noun (str): The helper noun in the sentence for analysis.
    local_entrance_adverb (str): The entrance adverb in the sentence for analysis.

    Returns:
    str: The original sentence that was analyzed.
    """

    doc = nlp(local_sentence)
    for token in doc:
        if token.text in [local_main_noun, local_helper_noun, local_entrance_adverb]:
            grammatical_info = {
                'text': token.text,
                'lemma': token.lemma_,
                'pos': token.pos_,
                'tag': token.tag_,
                'morph': token.morph
            }
            print(grammatical_info)
    # ANSI escape code for different colors
    colors = {  
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m"
    }
    reset = "\033[0m"

    # Set the color code to green
    color_code = colors["GREEN"]

    # Use the green color code for your sentence
    print(f"Transformed Sentence: {color_code + local_sentence + reset}")   
    # Function to analyze and print details of each word in the sentence using Spacy
    return local_sentence

def generate_sentence(hba1c_improvement_category, previous_hba1c_value, current_hba1c_value):
    """
    Generates a sentence based on the given HbA1c improvement level.

    Parameters:
    local_hba1c_improvement (str): The HbA1c improvement level which determines the choice of words.

    Returns:
    tuple: A tuple containing the generated sentence and the key elements used in the sentence 
           (main noun, helper noun, entrance adverb, and glucose control term).
    """
    # Define word sets for each HbA1c category
    
    words_for_improvement = {
        "deutlich verbessert": {
            "entrance_prepositions": ["Nach", "Unter", "Bei", "Mit", "Dank", "Mit Hilfe", "Durch"],
            "improvement_wordings": ["deutlich verbessert", "stark verbessert", "signifikant verbessert", "relevant verbessert", "merklich verbessert"],
            "entrance_adverbs": ["dezidiert", "gezielt", "konsequent"],
            "helper_nouns": ["Anpassung", "Optimierung", "Reduktion", "Steigerung", "Verbesserung"],
            "main_nouns": ["Bolus", "Bolus-Ess-Abstand", "Kohlenhydratmenge", "Kohlenhydratzufuhr", "Kohlenhydratfaktor", "Kohlenhydratfaktoren", "Korrekturfaktor", "Mahlzeiten-Bolus", "Therapie-Adhärenz"],
            "main_meals": ["Frühstück", "Mittagessen", "Abendessen"],
            "glucose_control": ["Blutzuckereinstellung", "Einstellung", "Glukosestoffwechsel"],
            "daytimes": ["Vormittag", "Mittag", "Nachmittag", "Abend"] # ... other words for this category
        },
        "verbessert": {
            "entrance_prepositions": ["Nach", "Unter", "Bei", "Mit", "Dank", "Mit Hilfe", "Durch"],
            "improvement_wordings": ["verbessert", "etwas verbessert", "diskret verbessert", "etwas optimiert"],
            "entrance_adverbs": ["dezidiert", "gezielt", "konsequent"],
            "helper_nouns": ["Anpassung", "Optimierung", "Reduktion", "Steigerung", "Verbesserung"],
            "main_nouns": ["Bolus", "Bolus-Ess-Abstand", "Kohlenhydratmenge", "Kohlenhydratzufuhr", "Kohlenhydratfaktor", "Kohlenhydratfaktoren", "Korrekturfaktor", "Mahlzeiten-Bolus", "Therapie-Adhärenz"],
            "main_meals": ["Frühstück", "Mittagessen", "Abendessen"],
            "glucose_control": ["Blutzuckereinstellung", "Einstellung", "Glukosestoffwechsel"],
            "daytimes": ["Vormittag", "Mittag", "Nachmittag", "Abend"]            # ... words for 'verbessert' category
        },
        "stabil gehalten": {
            "entrance_prepositions": ["Unter", "Bei", "Mit"],
            "improvement_wordings": ["stabil gehalten", "stabilisiert"],
            "entrance_adverbs": ["gewissenhaft", "konsequent"],
            "helper_nouns": ["Optimierungsversuchen", "Umsetzung", "Einhaltung"],
            "main_nouns": ["Bolus", "Bolus-Ess-Abstand", "Kohlenhydratmenge", "Kohlenhydratzufuhr", "Kohlenhydratfaktor", "Kohlenhydratfaktoren", "Korrekturfaktor", "Mahlzeiten-Bolus", "Therapie-Adhärenz"],
            "main_meals": ["Frühstück", "Mittagessen", "Abendessen"],
            "glucose_control": ["Blutzuckereinstellung", "Einstellung", "Glukosestoffwechsel"],
            "daytimes": ["Vormittag", "Mittag", "Nachmittag", "Abend"]            # ... words for 'verbessert' category
        },
        "verschlechtert": {
            "entrance_prepositions": ["Nach", "Unter", "Bei", "Wegen", "Durch"],
            "improvement_wordings": ["verschlechtert", "etwas verschlechtert", "leicht verschlechtert", "diskret verschlechtert"],
            "entrance_adverbs": ["weniger konsequent", "weniger umgesetzt"],
            "helper_nouns": ["Anpassung", "Reduktion", "Steigerung"],
            "main_nouns": ["Bolus", "Bolus-Ess-Abstand", "Kohlenhydratmenge", "Kohlenhydratzufuhr", "Kohlenhydratfaktor", "Kohlenhydratfaktoren", "Korrekturfaktor", "Mahlzeiten-Bolus", "Therapie-Adhärenz"],
            "main_meals": ["Frühstück", "Mittagessen", "Abendessen"],
            "glucose_control": ["Blutzuckereinstellung", "Einstellung", "Glukosestoffwechsel"],
            "daytimes": ["Vormittag", "Mittag", "Nachmittag", "Abend"]            # ... words for 'verbessert' category
        },
        "deutlich verschlechtert": {
            "entrance_prepositions": ["Nach", "Unter", "Bei", "Mit", "Wegen", "Durch", "Aufgrund"],
            "improvement_wordings": ["deutlich verschlechtert", "verschlechtert", "signifikant verschlechtert", "relevant verschlechtert", "merklich verschlechtert"],
            "entrance_adverbs": ["persistierend", "etwas zu optimistisch", "imponierend", "zu gering", "zu zögerlich"],
            "helper_nouns": ["Reduktion", "Steigerung"],
            "main_nouns": ["Bolus", "Bolus-Ess-Abstand", "Kohlenhydratmenge", "Kohlenhydratzufuhr", "Kohlenhydratfaktor", "Kohlenhydratfaktoren", "Korrekturfaktor", "Mahlzeiten-Bolus", "Therapie-Adhärenz"],
            "main_meals": ["Frühstück", "Mittagessen", "Abendessen"],
            "glucose_control": ["Blutzuckereinstellung", "Einstellung", "Glukosestoffwechsel"],
            "daytimes": ["Vormittag", "Mittag", "Nachmittag", "Abend"]            # ... words for 'verbessert' category
        },         
    }
    


    selected_words = words_for_improvement.get(hba1c_improvement_category, {})
    hba1c_improvement_wording = random.choice(selected_words["improvement_wordings"])
    local_entrance_preposition = random.choice(selected_words["entrance_prepositions"])
    local_entrance_adverb = random.choice(selected_words["entrance_adverbs"])
    local_helper_noun = random.choice(selected_words["helper_nouns"])
    local_main_noun = random.choice(selected_words["main_nouns"])
    local_main_meal = random.choice(selected_words["main_meals"])
    glucose_control = random.choice(selected_words["glucose_control"])
    local_daytime = random.choice(selected_words["daytimes"])
    
    # Initial sentence construction
    local_sentence = f"{local_entrance_preposition} {local_entrance_adverb} {local_helper_noun} {local_main_noun} {local_main_meal} hat sich {glucose_control} {hba1c_improvement_wording}. "
    
    # Determine the gender and number of the main noun and helper noun
    main_noun_gender, main_noun_number, helper_noun_gender = determine_noun_attributes(local_main_noun, local_helper_noun)

    if main_noun_gender and helper_noun_gender:
        # Apply grammar rules and construct the sentence
        local_sentence, _ = apply_german_grammar(local_sentence, local_entrance_preposition, main_noun_gender, main_noun_number, helper_noun_gender, selected_words["entrance_adverbs"], local_main_noun, local_main_meal, glucose_control)

    return local_sentence, local_main_noun, local_helper_noun, local_entrance_adverb, glucose_control


def determine_noun_attributes(local_main_noun, local_helper_noun):
    """
    Determine the gender and number of the given nouns.

    Args:
    main_noun (str): The main noun to analyze.
    helper_noun (str): The helper noun to analyze.

    Returns:
    tuple: A tuple containing the gender and number of the main and helper nouns.
    """
    doc_helper_noun = nlp(local_helper_noun)
    doc_main_noun = nlp(local_main_noun)
    main_noun_gender, main_noun_number, helper_noun_gender = None, None, None
    
    for token in doc_helper_noun:
        if token.pos_ == "NOUN":
            gender_list = token.morph.get("Gender")
            if gender_list:  # Check if the list is not empty
                helper_noun_gender = gender_list[0]
            # Add similar checks for other morphological attributes as needed
            break


    for token in doc_main_noun:
        if token.pos_ == "NOUN":
            main_noun_gender = token.morph.get("Gender")[0]
            main_noun_number = "Plur" if token.morph.get("Number")[0] == "Plur" else "Sing"
            break

    return main_noun_gender, main_noun_number, helper_noun_gender

if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Run as subprocess, with the category provided as an argument
        hba1c_improvement_category = sys.argv[1]
        previous_hba1c_value = sys.argv[2]
        current_hba1c_value = sys.argv[3]
    else:
        # Run independently, provide a default category or prompt for input
        print("Running in standalone mode. Please enter an HbA1c improvement category:")
        hba1c_improvement_category = input("Enter category (e.g., 'verbessert', 'stabil gehalten'): ")
    sentence, main_noun, helper_noun, entrance_adverb, glucose_control = generate_sentence(hba1c_improvement_category, previous_hba1c_value, current_hba1c_value)
    print(sentence)