#obligations a couverture

from spellchecker import SpellChecker

# Load French spell checker (prebuilt dictionary)
spell = SpellChecker(language='fr')

def correct_word(word):
    """Corrects a given word using spellchecker"""
    return spell.correction(word) or word 

def correct_text(text):
    """Corrects a full text"""
    words = text.split()
    corrected_words = [correct_word(word) for word in words]
    return " ".join(corrected_words)

corrupted_text = "obligations ꢄ lRouverture"
corrected_text = correct_text(corrupted_text)
print(corrected_text) 
