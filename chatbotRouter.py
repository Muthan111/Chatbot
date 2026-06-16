from fastapi import APIRouter, File, Request, UploadFile
from chatbotService import Chatbot

chatbotService = Chatbot()
chatbotRouter = APIRouter()

@chatbotRouter.get("/createChat")
async def read_createChat():
    return await chatbotService.read_createChat()

@chatbotRouter.get("/interactWithChat")
async def read_interactWithChat(chatname: str, message: str):
    return await chatbotService.read_interactWithChat(chatname, message)

@chatbotRouter.get("/Allchat")
async def read_Allchat():
    return await chatbotService.read_Allchat()

@chatbotRouter.put("/editMessage")
async def edit_message(chatname: str, message_index: int, new_message: str):
    return await chatbotService.edit_message(chatname, message_index, new_message)

@chatbotRouter.get("/getChat")
async def getChatv1(chatname: str):
    return await chatbotService.getChatv1(chatname)

@chatbotRouter.get("/getChatHistory")
async def getChatHistory(chatname: str):
    return await chatbotService.getChatHistory(chatname)