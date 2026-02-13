import nltk
nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize

def chunk_text(pages, max_length=500):
    chunks = []

    for page in pages:
        sentences = sent_tokenize(page["text"])
        current = ""

        for sent in sentences:
            if len(current) + len(sent) < max_length:
                current += " " + sent
            else:
                chunks.append({
                    "page": page["page"],
                    "text": current.strip()
                })
                current = sent

        if current:
            chunks.append({
                "page": page["page"],
                "text": current.strip()
            })

    return chunks
