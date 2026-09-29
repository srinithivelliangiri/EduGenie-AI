from services.gemini import generate_text


def explain_topic(topic):
    prompt = """
You are EduGenie, an AI learning assistant.

Explain the following topic to a beginner.

Your explanation should contain:

1. A simple definition.
2. An easy-to-understand explanation.
3. A simple real-world example or analogy.
4. Important key points.
5. A short example if the topic is programming or technical.

Use simple language.
Avoid unnecessary complexity.
Do not assume the student already knows advanced concepts.

Topic:
{}

Now explain the topic clearly.
""".format(topic)

    return generate_text(
        prompt,
        temperature=0.3
    )