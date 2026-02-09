def summarize_text(text):
    sentences = text.split(".")
    short = ". ".join(sentences[:2])
    return short
