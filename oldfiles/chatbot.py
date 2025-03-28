from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
import google.generativeai as genai
import asyncio

# API Key Configuration
genai.configure(api_key="AIzaSyAS6Nk1imMf8AydvMbpfUrTCgBF8o77Z1w")
model = genai.GenerativeModel("gemini-2.0-pro-exp")

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="super_secret_key", session_cookie="chat_session")

# Template directory
templates = Jinja2Templates(directory="templates")

@app.get("/chat")
async def root(request: Request):
    """Load chat history and return the chat page."""
    chat_history = request.session.get("chat_history", [])
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/chat")
async def handle_input(request: Request, user_input: str = Form(...)):
    """Handles user input and returns chatbot response asynchronously."""
    try:
        # Run model generation in a separate thread to avoid blocking
        response = await asyncio.to_thread(model.generate_content, user_input)
        response_text = response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process that."

        # Retrieve chat history from session
        chat_history = request.session.get("chat_history", [])
        chat_history.append({"role": "user", "message": user_input})
        chat_history.append({"role": "bot", "message": response_text})

        # Store updated chat history (limit history to 10 messages to avoid slowdowns)
        request.session["chat_history"] = chat_history[-10:]

        return JSONResponse(content={"response": response_text, "chat_history": chat_history})

    except Exception as e:
        print(f"Error: {e}")  # Log the issue
        return JSONResponse(status_code=500, content={"message": "Error processing your request."})
