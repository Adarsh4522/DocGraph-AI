import networkx as nx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import nltk
from nltk import pos_tag, word_tokenize

# Make sure punkt + tagger are downloaded
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "can", "will", "shall", "to", "of", "in",
    "on", "for", "and", "or", "with", "that",
    "this", "it", "as", "at", "by", "be"
}

def extract_nouns(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    return nouns

def build_mindmap(chunks):

    G = nx.DiGraph()   # Directed tree

    # Combine chunks into one document
    full_text = " ".join([c["text"] for c in chunks])

    if not full_text.strip():
        return G

    # Extract nouns
    nouns = extract_nouns(full_text)

    # Remove stopwords + short words
    nouns = [n.lower() for n in nouns if n.lower() not in STOPWORDS and len(n) > 3]

    if not nouns:
        return G

    # TF-IDF to get important concepts
    vectorizer = TfidfVectorizer(max_features=10)
    tfidf_matrix = vectorizer.fit_transform([" ".join(nouns)])
    feature_names = vectorizer.get_feature_names_out()

    if len(feature_names) == 0:
        return G

    # Root node (most important term)
    root = feature_names[0]
    G.add_node(root)

    # Add child nodes
    for term in feature_names[1:]:
        G.add_node(term)
        G.add_edge(root, term)

    return G



