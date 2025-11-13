import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import re

# Try to import spaCy (optional)
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    try:
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    except:
        try:
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except:
            pass

# Load spaCy model (optional)
nlp = None
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load("en_core_web_sm")
    except (OSError, IOError):
        # Model not found or not installed
        nlp = None

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> dict:
    """
    Comprehensive text preprocessing pipeline.
    Returns tokenized, lemmatized, and POS-tagged text.
    """
    if not text or not text.strip():
        return {
            "tokens": [],
            "sentences": [],
            "lemmas": [],
            "pos_tags": [],
            "entities": [],
            "clean_text": ""
        }
    
    # Basic cleaning
    clean_text = re.sub(r'\s+', ' ', text.strip())
    
    # Sentence tokenization
    sentences = sent_tokenize(clean_text)
    
    # Word tokenization
    tokens = word_tokenize(clean_text.lower())
    
    # Remove stopwords and punctuation
    filtered_tokens = [w for w in tokens if w.isalnum() and w not in stop_words]
    
    # Lemmatization
    lemmas = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # POS tagging
    pos_tags = nltk.pos_tag(filtered_tokens)
    
    # Named Entity Recognition (if spaCy is available)
    entities = []
    if nlp:
        doc = nlp(text)
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in doc.ents
        ]
    
    return {
        "tokens": filtered_tokens,
        "sentences": sentences,
        "lemmas": lemmas,
        "pos_tags": pos_tags,
        "entities": entities,
        "clean_text": clean_text,
        "word_count": len(filtered_tokens),
        "sentence_count": len(sentences)
    }
