from functions import createChat, getChat, interactWithChat, getAllChats, editUserMessage
import logging
from fastapi import  HTTPException
previousChat = []
class Chatbot:
    def __init__(self):
        pass
    async def read_createChat(self):
        logging.info("Creating new chat")
        global previousChat
        chat = createChat(previousChat)
        if not chat:
            raise HTTPException(status_code=500, detail="Chat creation failed")
        return chat
    async def read_interactWithChat(self,chatname: str, message: str):
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

    async def read_Allchat(self):
        logging.info("Fetching all chats")
        chat = getAllChats(previousChat)
        if not chat:
            raise HTTPException(status_code=404, detail="No chats found")
        return chat
    async def edit_message(self,chatname: str, message_index: int, new_message: str):
        logging.info(f"Editing message in chat: {chatname} at index {message_index}")
        result = editUserMessage(chatname, message_index, new_message, previousChat)
        if not result:
            raise HTTPException(status_code=404, detail="Chat or message not found")
        return result
    async def getChatv1(self,chatname: str):
        logging.info(f"Fetching chat: {chatname}")
        chat = getChat(chatname, previousChat)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat
    async def getChatHistory(self,chatname: str):
        logging.info(f"Fetching chat history for: {chatname}")
        chat = getChat(chatname, previousChat)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat["chatHistory"]