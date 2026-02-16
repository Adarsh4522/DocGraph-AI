from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
    )

def embed_text(chunks):
    texts = [c["text"] for c in chunks]

    return model.encode(texts)
