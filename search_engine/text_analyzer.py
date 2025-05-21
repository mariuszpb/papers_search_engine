import spacy

class TextAnalyzer:
    def __init__(self, language_model="pl_core_news_sm"):
        self.nlp = spacy.load(language_model)

    def extrect_keywords(self, text):
        """
        Extract keywords from the text using spaCy.
        """
        doc = self.nlp(text)

        # keywords = nouns and verbs. Optional: add adjectives and adverbs ["ADJ", "ADV"]
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB"]]
        
        return keywords
    
    
