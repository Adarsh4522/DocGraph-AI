from transformers import pipeline

summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def summarize_text(text):

    prompt = f"""
    Provide a detailed academic summary of the following document.
    Highlight key concepts, processes, and important conclusions.

    Document:
    {text}

    Academic Summary:
    """

    result = summarizer(
        prompt,
        max_length=300,
        do_sample=False,
        temperature=0.3
    )

    summary = result[0]["generated_text"]

    # Remove prompt from output
    return summary.replace(prompt, "").strip()


