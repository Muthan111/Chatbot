from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyAS6Nk1imMf8AydvMbpfUrTCgBF8o77Z1w"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-2.0-pro-exp')
#model = genai.GenerativeModel('gemini-1.5-pro')


app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Specify your template directory

@app.get("/chat")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})  # Assuming your template is named "index.html"

@app.post("/")
async def handle_input(request: Request, user_input: str = Form(...)):
    response_data = model.generate_content(user_input)
    return templates.TemplateResponse("index.html", {"request": request, "response_data": response_data.text})