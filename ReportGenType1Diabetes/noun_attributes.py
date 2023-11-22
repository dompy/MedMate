"""
Determine the attributes of all words within the context of a given sentence.
"NOUN": {},
"VERB": {},
"ADJECTIVE": {},
"ADVERB": {},
"PRONOUN": {},
"ADPOSITION": {},
"DETERMINER": {},
"AUXILLIARY VERB": {},
"PUNCTUATION": {},
"CONJUNCTION": {},
"INTERJECTION": {}
"""
import spacy
import language_tool_python

nlp = spacy.load('de_dep_news_trf')
tool = language_tool_python.LanguageTool('de-DE')

def determine_attributes_in_context(sentence):
    doc = nlp(sentence)
    pos_attributes = {}

    matches = tool.check(sentence)
    error_details = [{
        "issueType": match.ruleIssueType,
        "message": match.message,
        "suggestedCorrections": match.replacements
    } for match in matches]

    for token in doc:
        lemma = token.lemma_
        morph = token.morph.to_dict()
        dep = token.dep_
        head = token.head.text
        gender = morph.get("Gender")[0] if morph.get("Gender") else None
        number = morph.get("Number")[0] if morph.get("Number") else None
        case = morph.get("Case")[0] if morph.get("Case") else None
        if token.pos_ not in pos_attributes:
            pos_attributes[token.pos_] = {}
        pos_attributes[token.pos_][token.text] = {"lemma": lemma, "morph": morph, "dependency": dep, "head": head, "gender": gender, "number": number, "case": case}
    
    # Remove empty POS attributes
    pos_attributes = {pos: attrs for pos, attrs in pos_attributes.items() if attrs}

    return pos_attributes, error_details

# Test sentences
sentences = [
    "Mit gezielt Optimierung"
]

# Analyze nouns in different contexts
for sentence in sentences:
    attrs, errors = determine_attributes_in_context(sentence)
    print(f"\nSentence: '{sentence}'\n")
    for pos, words in attrs.items():
        print(f"POS: {pos}")
        for word, attributes in words.items():
            print(f"  Word: {word}")
            for attribute, value in attributes.items():
                print(f"    {attribute}: {value}")
    print(f"\nAnalysis: '{errors}'\n")