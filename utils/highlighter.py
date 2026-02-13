import re

def highlight_keywords(text, query):
    keywords = query.lower().split()
    highlighted = text

    for word in keywords:
        if len(word) > 3:
            pattern = re.compile(rf"\b({word})\b", re.IGNORECASE)
            highlighted = pattern.sub(r"**\1**", highlighted)

    return highlighted
