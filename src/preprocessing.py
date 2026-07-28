import pandas as pd
import re
import contractions
import nltk

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)


# Creates a set of stopwords excluding 'not', 'no', 'nor'
stop_words = set(stopwords.words("english"))
stop_words.discard("not")
stop_words.discard("no")
stop_words.discard("nor")

# Creates a Lemmatizer
lemmatizer = WordNetLemmatizer()

# Remove HTML Tags
def remove_html(text):
    return BeautifulSoup(text, "html.parser").get_text(separator=" ")

# Convert to Lowercase
def convert_lowercase(text):
    return text.lower()

# Remove URLs
def remove_urls(text):
    return re.sub(r'https?://\S+|www\.', '', text)

# Expand Contractions (can't -> cannot)
def expand_contraction(text):
    return contractions.fix(text)

# Remove Punctuation
def remove_punctuation(text):
    return re.sub(r"[^\w\s]", " ", text)

# Remove Extra Whitespaces
def remove_extra_whitespace(text):
    return " ".join(text.split())

# Remove Stopwords
def remove_stopwords(text):
    tokens = text.split()
    filtered_tokens = []
    for word in tokens:
        if word not in stop_words:
            filtered_tokens.append(word)
    
    return ' '.join(filtered_tokens)

# Convert NLTK POS tag to WordNet POS tag
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
#Lemmatize Text
def lemmatize_text(text):
    tokens = text.split()

    tagged_tokens = pos_tag(tokens)

    lemmatized_tokens = []

    for word, tag in tagged_tokens:
        pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word, pos)
        lemmatized_tokens.append(lemma)
    return ' '.join(lemmatized_tokens)

# Function to call Other Functions
def preprocess_text(text):
    text = str(text)
    text = remove_html(text)
    text = convert_lowercase(text)
    text = remove_urls(text)
    text = expand_contraction(text)
    text = remove_punctuation(text)
    text = remove_extra_whitespace(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)

    return text

if __name__ == "__main__":
    sample = "I can't believe this movie!!!"

    print(preprocess_text(sample))