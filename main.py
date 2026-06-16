from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging
from chatbotRouter import chatbotRouter

app = FastAPI(
    title="Chatbot API",
    description=(
        "API for connecting and calling the chatbot"
    ),
    version="1.0.0",
)
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chatbotRouter)
@app.get("/")
async def read_root(request: Request):
    logging.info("Accessing root endpoint")
    return templates.TemplateResponse("index.html", {"request": request})