"""
Campus Helpdesk API — starter skeleton.

Work through this alongside notes/Session1_FastAPI_Fundamentals.docx.
Build it up one endpoint at a time, testing each at /docs before moving on.
"""

from fastapi import FastAPI

app = FastAPI()

# TODO 1: add a GET / endpoint that returns
#   {"message": "Campus Helpdesk API is running"}


# TODO 2: add a GET /department/{name} endpoint that returns
#   {"department": name, "status": "open"}
# Raise a 404 with detail "Department not found" if name is not in a small
# list of valid departments.


# TODO 3: add a GET /search endpoint with query parameters
#   topic: str = "general"
#   limit: int = 5
# returning both as JSON.


# TODO 4: define a Pydantic model called Question with fields
#   student_name: str
#   question: str


# TODO 5: define a Pydantic model called Answer with fields
#   question: str
#   answer: str
#   confidence: float


# TODO 6: add a POST /ask endpoint that takes a Question and returns an
# Answer (use response_model=Answer). For now, always return the same
# fixed answer text — we'll replace this with a real AI call in Session 02.
