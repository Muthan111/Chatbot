from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import asyncio
import logging
from functions import createChat, getChat, interactWithChat, getAllChats, editUserMessage

# Configure logging
logging.basicConfig(level=logging.INFO)

# # Configure Gemini API
# genai.configure(api_key="AIzaSyDK_uzl6p2bmTUSzPNAB27eE84XeFHXD9M")
# model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Array to store chat data
previousChat = []

@app.get("/")
async def read_root(request: Request):
    logging.info("Accessing root endpoint")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/createChat")
async def read_createChat():
    logging.info("Creating new chat")
    global previousChat
    chat = createChat(previousChat)
    if not chat:
        raise HTTPException(status_code=500, detail="Chat creation failed")
    return chat



@app.get("/interactWithChat")
async def read_interactWithChat(chatname: str, message: str):
    logging.info(f"Interacting with chat: {chatname}, message: {message}")
    if not previousChat:
        raise HTTPException(status_code=400, detail="No chats available")

    chat = getChat(chatname, previousChat)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    response_text = interactWithChat(chatname, message, previousChat)

    if not response_text:
        raise HTTPException(status_code=500, detail="Failed to generate a response")
    return {"userMessage": message, "botResponse": response_text}

@app.get("/Allchat")
async def read_Allchat():
    logging.info("Fetching all chats")
    chat = getAllChats(previousChat)
    if not chat:
        raise HTTPException(status_code=404, detail="No chats found")
    return chat

@app.put("/editMessage")
async def edit_message(chatname: str, message_index: int, new_message: str):
    logging.info(f"Editing message in chat: {chatname} at index {message_index}")
    result = editUserMessage(chatname, message_index, new_message, previousChat)
    if not result:
        raise HTTPException(status_code=404, detail="Chat or message not found")
    return result

@app.get("/getChat")
async def getChatv1(chatname: str):
    logging.info(f"Fetching chat: {chatname}")
    chat = getChat(chatname, previousChat)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@app.get("/getChatHistory")
async def getChatHistory(chatname: str):
    logging.info(f"Fetching chat history for: {chatname}")
    chat = getChat(chatname, previousChat)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat["chatHistory"]