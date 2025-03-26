from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from functions import createChat, getChat, interactWithChat,getAllChats,editUserMessage
genai.configure(api_key="AIzaSyDSbw52Qq4EjJ_nBoQvEUst3IXZwlhAOE8")
model = genai.GenerativeModel("gemini-2.0-pro-exp")
# Mock Array to store chat data
# If have time  implement postgresql
previousChat = [
    #chatId
    #chatName
    #chatHistory : []
   
]
app = FastAPI()

@app.get("/")
def read_root(request: Request):
    return {"Hello": "World"}

@app.get("/createChat")
def read_createChat(request: Request):
    chat = createChat(previousChat)
    if not chat:
        return {"error": "Chat creation failed"}
    return {"chatId": chat["chatId"], "chatName": chat["chatName"], "chatHistory": chat["chatHistory"]}

@app.get("/getChat")
def read_getChat(request: Request, chatname: str):
    chat = getChat(chatname, previousChat)
    if not previousChat:
        return {"error": "Array does not exist"}
    if not chat:
        return {"error": "Chat not found"}
    return chat

@app.get("/interactWithChat")
def read_interactWithChat(request: Request, chatname: str, message: str):
    chat = interactWithChat(chatname, message, previousChat)
    if not previousChat:
        return {"error": "Array does not exist"}
    if not chat:
        return {"error": "Chat not found"}
    return chat

@app.get("/Allchat")
def read_Allchat(request: Request):
    chat = getAllChats(previousChat)
    return chat

@app.put("/editMessage")
def edit_message(request: Request, chatname: str, message_index: int, new_message: str):
    """
    Endpoint to edit a user message in the chat history of a specific chat.

    Args:
        chatname (str): The name of the chat to edit.
        message_index (int): The index of the message to edit.
        new_message (str): The new content for the message.

    Returns:
        dict: The updated chat object if successful, or an error message.
    """
    result = editUserMessage(chatname, message_index, new_message, previousChat)
    return result