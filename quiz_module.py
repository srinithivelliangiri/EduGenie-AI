from services.gemini import generate_text
from models import QuizResponse


def generate_quiz(text):
    prompt = """
You are EduGenie, an AI learning assistant.

Create a quiz based ONLY on the text provided by the student.

Requirements:

1. Create exactly 3 multiple-choice questions.
2. Each question must have exactly 4 options.
3. There must be exactly one correct answer.
4. The correct answer must exactly match one of the 4 options.
5. Every question must be answerable from the provided text.
6. Provide a short explanation for the correct answer.
7. Use simple language suitable for a student.
8. Do not add information that is not present in the text.

Return ONLY valid JSON using exactly this structure:

{
    "questions": [
        {
            "question": "Question here",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "explanation": "Explanation here"
        },
        {
            "question": "Question here",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option B",
            "explanation": "Explanation here"
        },
        {
            "question": "Question here",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option C",
            "explanation": "Explanation here"
        }
    ]
}

Text:

{}
""".format(text)

    result = generate_text(
        prompt,
        temperature=0.5
    )

    try:
        # Convert Gemini's JSON text into our Pydantic model.
        return QuizResponse.model_validate_json(result)

    except AttributeError:
        # Compatibility fallback for Pydantic versions
        # that use parse_raw().
        try:
            return QuizResponse.parse_raw(result)

        except Exception as exc:
            raise ValueError(
                "Could not convert Gemini quiz response "
                "into the required quiz format: {}".format(exc)
            )

    except Exception as exc:
        raise ValueError(
            "Could not convert Gemini quiz response "
            "into the required quiz format: {}".format(exc)
        )