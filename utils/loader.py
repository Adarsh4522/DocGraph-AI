from PyPDF2 import PdfReader

def load_document(file):
    # Returns a list of dicts: [{"page": 1, "text": "..."}]
    pages = []

    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        for i, page in enumerate(reader.pages):
            content = page.extract_text()
            if content and content.strip():
                pages.append({
                    "page": i + 1,
                    "text": content
                })
        return pages

    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
        if text.strip():
            pages.append({
                "page": 1,
                "text": text
            })
        return pages

    return []

