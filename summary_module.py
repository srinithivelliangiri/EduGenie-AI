from services.gemini import generate_text


def summarize_text(text):
    prompt = """
You are EduGenie, an AI learning assistant.

Summarize the following text for a student.

Requirements:

1. Keep the most important facts and ideas.
2. Remove repetition and unnecessary wording.
3. Use simple language.
4. Make the summary useful for revision.
5. Prefer short bullet points when appropriate.
6. Do not add facts that are not present in the source text.

Text:

{}

Now provide the summary.
""".format(text)

    return generate_text(
        prompt,
        temperature=0.2
    )