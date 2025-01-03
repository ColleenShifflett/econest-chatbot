from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from .chat_logic import ChatBot
from .models import ChatInput, ChatResponse

app = FastAPI()

# Get the absolute path to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount the static directory and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

chatbot = ChatBot()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat_input: ChatInput):
    response = chatbot.get_response(chat_input.message)
    return ChatResponse(response=response)
