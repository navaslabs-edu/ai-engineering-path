# Session 1: FastAPI Fundamentals

Student Notes

## Where This Fits

Almost every AI product you use is, underneath, a regular web API with a model bolted onto it. Before we touch any AI model, we need to be completely comfortable building the API layer that will eventually wrap it. This session builds a small "Campus Helpdesk API" that answers student questions using fixed, hand-written answers. In Session 2, we replace those fixed answers with a real call to an AI model - the API itself will barely change. That is the point: get the engineering foundation rock solid first, then the AI part slots in cleanly.

## 1. What Is FastAPI, and Why It Matters Here

FastAPI is a Python framework for building APIs - programs that accept requests over the internet (or your local network) and send back responses, usually in JSON. It is the most widely used framework for AI engineering in Python for three reasons:

- It is built around Python type hints, which forces you to be precise about what data goes in and out - critical when an AI model's output needs to be structured and predictable.
- It supports async functions natively, which matters because calls to AI models can take several seconds; async lets your server handle other requests while it waits.
- It generates interactive documentation automatically, which makes it easy to test and demo your API without building a frontend first.

## 2. Your First FastAPI App

Every FastAPI app starts the same way: create an app object, then attach functions to URL paths.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Campus Helpdesk API is running"}
```

Save this as `main.py`, then run it from the terminal:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser:

Output:
```json
{"message": "Campus Helpdesk API is running"}
```

**Note:** `uvicorn` is the server that actually runs your FastAPI app. `--reload` restarts it automatically whenever you save a change, which is very useful while building.

## 3. Path Parameters

A path parameter is a value that is part of the URL itself. Use it when the value identifies a specific resource.

```python
@app.get("/department/{name}")
def get_department(name: str):
    return {"department": name, "status": "open"}
```

Visiting `/department/computing` returns:

Output:
```json
{"department": "computing", "status": "open"}
```

## 4. Query Parameters

A query parameter comes after a `?` in the URL, and is used for optional filters or settings. Function arguments with default values automatically become query parameters.

```python
@app.get("/search")
def search_faq(topic: str = "general", limit: int = 5):
    return {"topic": topic, "limit": limit}
```

Visiting `/search?topic=fees&limit=3` returns:

Output:
```json
{"topic": "fees", "limit": 3}
```

**Note:** If you leave out the query parameters entirely and just visit `/search`, FastAPI uses the defaults: `topic="general"`, `limit=5`.

## 5. Request Body With Pydantic Models

Path and query parameters are fine for small values, but when a request needs to send a whole object - like a student's question - we send it as a JSON body, described by a Pydantic model.

```python
from pydantic import BaseModel

class Question(BaseModel):
    student_name: str
    question: str

@app.post("/ask")
def ask_question(data: Question):
    return {"received_from": data.student_name, "question": data.question}
```

Sending this JSON body to `POST /ask`:

```json
{
  "student_name": "Asha",
  "question": "When is the fees deadline?"
}
```

Returns:

Output:
```json
{"received_from": "Asha", "question": "When is the fees deadline?"}
```

**Note:** Pydantic automatically checks that the incoming data matches the model. If `student_name` is missing, FastAPI rejects the request before your function even runs.

## 6. Response Models

Just as Pydantic describes what comes in, it can also describe what goes out. This matters a lot in AI engineering, because we often need the model's answer to always come back in the exact same shape.

```python
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
```

Now every response from `/ask` is guaranteed to have exactly these three fields, in this shape:

Output:
```json
{
  "question": "When is the fees deadline?",
  "answer": "Visit the finance office on Monday.",
  "confidence": 0.8
}
```

## 7. Status Codes and Error Handling

A well-built API should say clearly when something goes wrong, using HTTP status codes. FastAPI gives us `HTTPException` for this.

```python
from fastapi import HTTPException

departments = ["computing", "business", "engineering"]

@app.get("/department/{name}")
def get_department(name: str):
    if name not in departments:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"department": name, "status": "open"}
```

Visiting `/department/medicine` (not in our list) returns a 404 status with:

Output:
```json
{"detail": "Department not found"}
```

**Note:** 200 means success, 404 means "not found", 422 means the request data failed validation, and 500 means something broke on the server. You will see these constantly once you start calling AI models, since they have their own error codes too.

## 8. Automatic Documentation

Run your app and visit `/docs` in the browser. FastAPI builds an interactive page where you can see every endpoint, try it directly, and see exactly what data it expects - without writing a single extra line of code. There is also a simpler version at `/redoc`. This becomes extremely useful once your APIs are calling AI models, since you can test prompts and inputs without building a frontend at all.

## Putting It All Together: The Campus Helpdesk API

Here is the full mini API combining everything from this session. This is the exact file we will extend in Session 2 by replacing the canned answer with a real AI model call.

```python
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
```

## Practice Questions

Each part below has a mix of everyday Kenyan-context questions and AI-engineering-flavoured questions, since both kinds of endpoints will keep showing up in this course.

### Part A - Path Parameters

1. Build a GET endpoint `/matatu/{route_number}` that returns the route number and a fixed fare, e.g. `{"route": "32", "fare_ksh": 100}`.
2. Build a GET endpoint `/county/{name}` that returns `{"county": name, "capital": "unknown"}` for any county name typed in.
3. Build a GET endpoint `/bot/{bot_name}` that returns `{"bot": bot_name, "status": "online"}` - imagine this is how a user checks which AI assistant they are talking to.

### Part B - Query Parameters

1. Build a GET endpoint `/weather` that takes `town` (default `"Nairobi"`) and `unit` (default `"celsius"`) as query parameters and returns both.
2. Build a GET endpoint `/menu` that takes a `category` query parameter (default `"all"`) for a small food kiosk, returning `{"category": category}`.
3. Build a GET endpoint `/faq` that takes `topic` and `max_results` (default `3`) query parameters, for filtering helpdesk questions by topic - same pattern as the `/search` endpoint above.

### Part C - Request Body With Pydantic

1. Build a Pydantic model `Order` with `customer_name` and `item`, and a POST endpoint `/order` for a small Mama Mboga shop that echoes back what was ordered.
2. Build a Pydantic model `Ticket` with `sender` and `message`, and a POST endpoint `/support` that echoes back the sender and message - this is the basic shape of any AI support-bot intake endpoint.
3. Build a Pydantic model `Booking` with `passenger_name` and `route`, and a POST endpoint `/book` for a matatu booking app that echoes the booking details back.

### Part D - Response Models and Error Handling

1. Add a response model `BookInfo` (`title`, `author`, `available: bool`) to a GET `/book/{title}` endpoint for a small library, raising a 404 if the title is not in your list.
2. Add a response model `BotReply` (`question`, `answer`, `confidence`) to a POST `/ask-bot` endpoint, raising a 404 with detail `"Topic not supported"` if the topic sent is not in a small allowed list.
3. Add a response model `PriceCheck` (`item`, `price_ksh`) to a GET `/price/{item}` endpoint for a shop, raising a 404 if the item is not stocked.

### Part E - Challenge: Combine Everything

1. Build a small "AI Support Intake API" with: a GET `/` health-check endpoint; a GET `/agent/{agent_name}` path endpoint with a 404 for unknown agents; a GET `/tickets` query endpoint that filters by `status` (default `"open"`) and `limit` (default `5`); a POST `/ticket` endpoint using a Pydantic request model (`customer_name`, `issue`) and a Pydantic response model (`ticket_id`, `customer_name`, `issue`, `priority`) that always returns `priority` as `"normal"`.
2. Test every endpoint of your Challenge API using the automatic docs at `/docs` before moving on - do not just read the code, run it.

## Golden Rules

| # | Rule |
|---|---|
| 1 | FastAPI apps start with `app = FastAPI()`, then each endpoint is a decorated function. |
| 2 | Run the app with `uvicorn main:app --reload`, not by running the Python file directly. |
| 3 | Path parameters identify a specific resource; query parameters filter or configure a request. |
| 4 | Function arguments with default values automatically become optional query parameters. |
| 5 | Use a Pydantic `BaseModel` to describe the shape of any JSON request body. |
| 6 | Use `response_model` to guarantee the exact shape of every response - essential once AI output is involved. |
| 7 | Raise `HTTPException` with a clear `status_code` and `detail` message instead of letting errors fail silently. |
| 8 | Visit `/docs` to test every endpoint interactively without writing a frontend. |
| 9 | Build and test one endpoint at a time - do not write the whole API before running anything. |
| 10 | This API's structure will not change much when we add a real AI model in Session 2 - only the inside of one function will. |
