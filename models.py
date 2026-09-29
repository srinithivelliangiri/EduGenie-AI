from typing import List
from typing_extensions import Literal
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1)


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_items=4, max_items=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(
        ...,
        min_items=3,
        max_items=3
    )


class LearningStage(BaseModel):
    level: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    topics: List[str]
    goals: List[str]
    resources: List[str]
    practice: List[str]


class LearningPathResponse(BaseModel):
    title: str
    overview: str
    estimated_duration: str
    stages: List[LearningStage]