from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

import os


# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))


app = FastAPI()


# Static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


# Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class UserRequest(BaseModel):
    message: str


class AIResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AIResponse)
def ask_ai(request: UserRequest):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )