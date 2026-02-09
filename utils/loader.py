from PyPDF2 import PdfReader

def load_document(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    return ""
