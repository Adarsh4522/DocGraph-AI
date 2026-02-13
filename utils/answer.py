
def generate_answer(query, context_chunks):
    if not context_chunks:
        return "No relevant information found."

    context = " ".join(context_chunks)

    if "define" in query.lower():
        return context.split(".")[0]

    if "explain" in query.lower():
        sentences = context.split(".")
        return ". ".join(sentences[:2])

    if "list" in query.lower():
        sentences = context.split(".")
        return "\n".join(sentences[:3])

    return context_chunks[0]
