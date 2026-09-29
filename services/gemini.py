import json
import requests

from config import get_settings


class GeminiServiceError(Exception):
    """Raised when the Gemini API cannot be used successfully."""


def _generate(prompt, temperature=0.3):
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        + settings.gemini_model
        + ":generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": settings.gemini_api_key,
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=120
        )

    except requests.RequestException as exc:
        raise GeminiServiceError(
            "Could not connect to Gemini API: {}".format(exc)
        )

    if response.status_code != 200:
        try:
            error_data = response.json()

            error_message = error_data.get(
                "error", {}
            ).get(
                "message",
                "Unknown Gemini API error"
            )

        except ValueError:
            error_message = response.text

        raise GeminiServiceError(
            "Gemini API error (HTTP {}): {}".format(
                response.status_code,
                error_message
            )
        )

    try:
        data = response.json()

        candidates = data.get("candidates", [])

        if not candidates:
            raise GeminiServiceError(
                "Gemini returned no candidates."
            )

        content = candidates[0].get("content", {})

        parts = content.get("parts", [])

        if not parts:
            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        text = parts[0].get("text", "").strip()

        if not text:
            raise GeminiServiceError(
                "Gemini returned an empty text response."
            )

        return text

    except ValueError:
        raise GeminiServiceError(
            "Gemini returned an invalid JSON response."
        )


def generate_text(prompt, temperature=0.3):
    """Generate normal text using Gemini."""

    return _generate(
        prompt=prompt,
        temperature=temperature
    )


def generate_structured(prompt, response_model, temperature=0.3):
    """
    Ask Gemini to return JSON and convert that JSON
    into the requested Pydantic model.
    """

    json_prompt = prompt + """

IMPORTANT:
Return ONLY valid JSON.
Do NOT use Markdown code fences.
Do NOT add explanations before the JSON.
Do NOT add explanations after the JSON.
"""

    raw_text = _generate(
        prompt=json_prompt,
        temperature=temperature
    )

    raw_text = raw_text.strip()

    # Remove Markdown code fences if Gemini adds them.
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]

    elif raw_text.startswith("```"):
        raw_text = raw_text[3:]

    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)

    except ValueError as exc:
        raise GeminiServiceError(
            "Gemini returned invalid JSON: {}".format(exc)
        )

    try:
        # Pydantic 2.x
        if hasattr(response_model, "model_validate"):
            return response_model.model_validate(data)

        # Pydantic 1.x fallback
        return response_model.parse_obj(data)

    except Exception as exc:
        raise GeminiServiceError(
            "Gemini returned JSON that does not match "
            "the expected EduGenie format: {}".format(exc)
        )