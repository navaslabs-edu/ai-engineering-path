"""
Campus Helpdesk API — reference solution.

This exact file is extended in Session 02 by replacing the fixed answer
inside ask_question() with a real call to an AI model. Nothing else about
the API's shape changes.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
departments = ["computing", "business", "engineering"]


@app.get("/")
def home():
    return {"message": "Campus Helpdesk API is running"}


@app.get("/department/{name}")
def get_department(name: str):
    if name not in departments:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"department": name, "status": "open"}


@app.get("/search")
def search_faq(topic: str = "general", limit: int = 5):
    return {"topic": topic, "limit": limit}


class Question(BaseModel):
    student_name: str
    question: str


class Answer(BaseModel):
    question: str
    answer: str
    confidence: float


@app.post("/ask", response_model=Answer)
def ask_question(data: Question):
    return Answer(
        question=data.question,
        answer="Visit the finance office on Monday.",
        confidence=0.8,
    )
