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
    G = nx.Graph()

    # Combine chunks into one document
    full_text = " ".join(chunks)

    # Extract candidate nouns
    nouns = extract_nouns(full_text)
    nouns = [n for n in nouns if n.lower() not in STOPWORDS and len(n) > 3]

    if not nouns:
        return G

    # TF-IDF to get important concepts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(nouns)])
    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.toarray()[0]
    term_scores = list(zip(feature_names, scores))
    term_scores.sort(key=lambda x: x[1], reverse=True)

    # Top 8 concepts
    top_terms = [term for term, score in term_scores[:8]]

    if not top_terms:
        return G

    central = top_terms[0]
    G.add_node(central)

    # Build connections based on sentence co-occurrence
    sentences = re.split(r'[.!?]', full_text)

    connections = defaultdict(set)

    for sentence in sentences:
        words = extract_nouns(sentence)
        words = [w for w in words if w in top_terms]
        for w in words:
            if w != central:
                connections[w].add(central)

    for node in top_terms[1:]:
        G.add_node(node)
        G.add_edge(central, node)

    return G


