from services.gemini import generate_structured
from models import LearningPathResponse


def get_learning_recommendations(topic):
    prompt = """
You are EduGenie, an AI learning assistant.

Create a practical learning path for this topic:

{}

Return ONLY valid JSON matching this structure:

{
    "title": "Learning path title",
    "overview": "Short overview",
    "estimated_duration": "Estimated duration",
    "stages": [
        {
            "level": "Beginner",
            "topics": [
                "Topic 1",
                "Topic 2"
            ],
            "goals": [
                "Goal 1",
                "Goal 2"
            ],
            "resources": [
                "Textbook",
                "Tutorial",
                "Documentation"
            ],
            "practice": [
                "Practice 1",
                "Practice 2"
            ]
        },
        {
            "level": "Intermediate",
            "topics": [
                "Topic 1",
                "Topic 2"
            ],
            "goals": [
                "Goal 1",
                "Goal 2"
            ],
            "resources": [
                "Tutorial",
                "Documentation"
            ],
            "practice": [
                "Practice 1",
                "Practice 2"
            ]
        },
        {
            "level": "Advanced",
            "topics": [
                "Topic 1",
                "Topic 2"
            ],
            "goals": [
                "Goal 1",
                "Goal 2"
            ],
            "resources": [
                "Documentation",
                "Advanced course"
            ],
            "practice": [
                "Practice 1",
                "Practice 2"
            ]
        }
    ]
}

Rules:

1. Include Beginner, Intermediate, and Advanced stages.
2. Make the learning path practical and student-friendly.
3. Mention prerequisites where useful.
4. Recommend resource TYPES rather than inventing URLs.
5. Keep the content focused on the requested topic.
6. Use simple language.

Topic:

{}
""".format(topic, topic)

    return generate_structured(
        prompt,
        LearningPathResponse,
        temperature=0.4
    )