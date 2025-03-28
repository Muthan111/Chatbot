import array
import google.generativeai as genai

genai.configure(api_key="AIzaSyDPrXjET21ihfNpd6ZiPLNOS1GpwP1FWNw")
model = genai.GenerativeModel("gemini-2.0-pro-exp")

previousChat = []

# Function to generate a unique chat ID
def generateChatId(chatArray):
    if chatArray:
        existingIds = {chat["chatId"] for chat in chatArray}
        chatId = 1
        while chatId in existingIds:
            chatId += 1
        return chatId
    return 1  # Start with ID 1 if no chats exist

# Function to generate a chat name
def generateChatName(baseName, chatArray):
    # If no chats exist yet, start with "Chat1"
    if not chatArray:  
        return f"{baseName}1"
    existingNames = [chat["chatName"] for chat in chatArray]
    counter = 1
    while f"{baseName}{counter}" in existingNames:
        counter += 1
    
    return f"{baseName}{counter}"

def createChat(array1):
    # Generate a unique chat name
    chatName = generateChatName("Chat",array1)
    for chat in array1:
        if chat["chatName"] == chatName:
            return chat  
    chatId = generateChatId(array1)
    
    chat = {
        "chatId": chatId,
        "chatName": chatName,
        "chatHistory": []
    }

    array1.append(chat)
    return chat

def getChat(chatname, chatArray):
    for chat in chatArray:
        if chat["chatName"] == chatname:  
            return chat
    return None

def getChatHistory(chatname, chatArray):
    for chat in chatArray:
        if chat["chatName"] == chatname:
            return            
    return None

def getAllChats(chatArray):
    return chatArray

def interactWithChat(chatname,userinput,chatarray):
    for chat in chatarray:
        if chat["chatName"] == chatname:
            # Gather the chat history as context
            history = chat["chatHistory"]
            context = "\n".join([f"{item['role']}: {item['message']}" for item in history])
            
            # Combine the context with the user's input
            prompt = f"Context:\n{context}\n\nUser: {userinput}\nBot:"
            
            response = model.generate_content(prompt)
            bot_response = response.text
            
            # Update the chat history
            history.append({"role": "user", "message": userinput})
            history.append({"role": "bot", "message": bot_response})
            
            bot_responses = [item["message"] for item in history if item["role"] == "bot"]
            for bot_response in bot_responses:
                print(bot_response)
            return bot_response  
    return None

def deleteChat(chatname):
    for chat in previousChat:
        if chat["chatName"] == chatname:
            previousChat.remove(chat)
            print(f"Chat '{chatname}' deleted.")
            return chatname
    return None

def editUserMessage(chatname, message_index, new_message, chatarray):
    chat = getChat(chatname, chatarray)
    if not chat:
        return {"error": "Chat not found"}
    
    if message_index < 0 or message_index >= len(chat["chatHistory"]):
        return {"error": "Invalid message index"}
    
    if chat["chatHistory"][message_index]["role"] != "user":
        return {"error": "Only user messages can be edited"}
    chat["chatHistory"][message_index]["message"] = new_message
    
    response = model.generate_content(new_message)
    bot_response = response.text
    
    if message_index + 1 < len(chat["chatHistory"]) and chat["chatHistory"][message_index + 1]["role"] == "bot":
        chat["chatHistory"][message_index + 1]["message"] = bot_response
    else:
        chat["chatHistory"].insert(message_index + 1, {"role": "bot", "message": bot_response})
    
    return {
        "success": True,
        "updatedUserInput": new_message,
        "botResponse": bot_response
    }
# createChat()
# interactWithChat("Chat1","How can i train my dog")
# getChat("Chat1")
# deleteChat("Chat1")

