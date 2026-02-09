import nltk
nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize

def chunk_text(text, max_length=500):
    sentences = sent_tokenize(text)
    chunks = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) < max_length:
            current += " " + sent
        else:
            chunks.append(current.strip())
            current = sent

    if current:
        chunks.append(current.strip())

    return chunks
