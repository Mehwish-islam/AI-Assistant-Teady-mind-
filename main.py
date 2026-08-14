from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# Request schema
class UserRequest(BaseModel):
    message: str


# Response schema
class AIResponse(BaseModel):
    answer: str


# AI endpoint
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


# Frontend endpoint
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )