import random
import re

def generate_mcqs(chunks, num_questions=10):
    questions = []

    sentences = []
    for chunk in chunks:
        sentences.extend(chunk["text"].split("."))


    # Clean and filter meaningful sentences
    sentences = [
        s.strip() for s in sentences
        if len(s.split()) > 8
    ]

    random.shuffle(sentences)

    for sentence in sentences:
        if len(questions) >= num_questions:
            break

        words = re.findall(r'\b[a-zA-Z]{5,}\b', sentence)

        if len(words) < 4:
            continue

        answer = random.choice(words)
        question_text = sentence.replace(answer, "_____")

        # Generate options
        options = [answer]
        while len(options) < 4:
            fake = random.choice(words)
            if fake not in options:
                options.append(fake)

        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    return questions

