from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import get_settings
from explanation_module import explain_topic
from learning_path import get_learning_recommendations

from models import (
    LearningPathResponse,
    QuestionRequest,
    QuizResponse,
    TextRequest,
    TopicRequest
)

from qna import answer_question
from quiz_module import generate_quiz
from services.gemini import GeminiServiceError
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie AI",
    description="AI-powered learning assistant",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


def check_input_length(text):
    settings = get_settings()

    if len(text) > settings.max_input_chars:
        raise HTTPException(
            status_code=400,
            detail=(
                "Input is too long. Maximum allowed length is "
                "{} characters.".format(
                    settings.max_input_chars
                )
            )
        )


@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get("/health")
async def health():
    settings = get_settings()

    return {
        "status": "ok",
        "service": "EduGenie AI",
        "gemini_configured": bool(
            settings.gemini_api_key
        )
    }


@app.post("/qa")
async def qa(request: QuestionRequest):
    check_input_length(request.question)

    try:
        answer = answer_question(
            request.question
        )

        return {
            "answer": answer
        }

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Q&A failed: {}".format(exc)
        )


@app.post("/explain")
async def explain(request: TopicRequest):
    check_input_length(request.topic)

    try:
        explanation = explain_topic(
            request.topic
        )

        return {
            "explanation": explanation
        }

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Explanation failed: {}".format(exc)
        )


@app.post("/quiz")
async def quiz(request: TextRequest):
    check_input_length(request.text)

    try:
        result = generate_quiz(
            request.text
        )

        return result

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Quiz generation failed: {}".format(exc)
        )


@app.post("/summarize")
async def summarize(request: TextRequest):
    check_input_length(request.text)

    try:
        summary = summarize_text(
            request.text
        )

        return {
            "summary": summary
        }

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Summarization failed: {}".format(exc)
        )


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def learning_recommendations(
    request: TopicRequest
):
    check_input_length(request.topic)

    try:
        result = get_learning_recommendations(
            request.topic
        )

        return result

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Learning path generation failed: {}".format(
                    exc
                )
            )
        )