import array
import google.generativeai as genai

genai.configure(api_key="AIzaSyDSbw52Qq4EjJ_nBoQvEUst3IXZwlhAOE8")
model = genai.GenerativeModel("gemini-2.0-pro-exp")

previousChat = [
    #chatId
    #chatName
    #chatHistory : []
]
# Function to generate a unique chat ID
def generateChatId(chatArray):
    if chatArray:
        # Get all existing chat IDs
        existingIds = {chat["chatId"] for chat in chatArray}
        # Find the smallest unused ID starting from 1
        chatId = 1
        while chatId in existingIds:
            chatId += 1
        return chatId
    return 1  # Start with ID 1 if no chats exist

# Function to generate a chat name
def generateChatName(baseName, chatArray):
    # Extract existing chat names from the provided array
    existingNames = [chat["chatName"] for chat in chatArray]
    
    # If the base name is not already in use, return it
    if baseName not in existingNames:
        return baseName
    
    # Append a number to make the name unique
    counter = 1
    while f"{baseName}{counter}" in existingNames:
        counter += 1
    
    return f"{baseName}{counter}"



def createChat(array1):
    # Generate a unique chat name
    chatName = generateChatName("Chat",array1)
    
    # Check if a chat with the same name already exists
    for chat in array1:
        if chat["chatName"] == chatName:
            return chat  # Return the existing chat if it already exists

    # Generate a unique chat ID
    chatId = generateChatId(array1)
    
    # Create a new chat object
    chat = {
        "chatId": chatId,
        "chatName": chatName,
        "chatHistory": []
    }
    
    # Append the new chat to the array
    array1.append(chat)
    return chat

def getChat(chatname, chatArray):
    for chat in chatArray:
        if chat["chatName"] == chatname:  # Ensure exact match
            return chat
    return None

def getAllChats(chatArray):
    return chatArray

def interactWithChat(chatname,userinput,chatarray):
    for chat in chatarray:
        if chat["chatName"] == chatname:
            history = chat["chatHistory"]
            addinput = userinput
            response = model.generate_content(addinput)
            history.append({"role": "user", "message": addinput})
            history.append({"role": "bot", "message": response.text})
            # Print only the bot's responses
            bot_responses = [item["message"] for item in history if item["role"] == "bot"]
            for bot_response in bot_responses:
                print(bot_response)
            
            return response.text # Exit the loop once the chat is found
    return None

def deleteChat(chatname):
    for chat in previousChat:
        if chat["chatName"] == chatname:
            previousChat.remove(chat)
            print(f"Chat '{chatname}' deleted.")
            return chatname
    return None

def editUserMessage(chatname, message_index, new_message, chatarray):
    """
    Edit a user message in the chat history of a specific chat and regenerate the bot response.

    Args:
        chatname (str): The name of the chat to edit.
        message_index (int): The index of the message to edit.
        new_message (str): The new content for the message.
        chatarray (list): The array of chats.

    Returns:
        dict: The updated user input and regenerated bot response if successful, or an error message.
    """
    # Find the chat by name
    chat = getChat(chatname, chatarray)
    if not chat:
        return {"error": "Chat not found"}
    
    # Validate the message index
    if message_index < 0 or message_index >= len(chat["chatHistory"]):
        return {"error": "Invalid message index"}
    
    # Check if the message belongs to the user
    if chat["chatHistory"][message_index]["role"] != "user":
        return {"error": "Only user messages can be edited"}
    
    # Update the user message
    chat["chatHistory"][message_index]["message"] = new_message
    
    # Regenerate the bot response
    response = model.generate_content(new_message)
    bot_response = response.text
    
    # Update the bot response in the chat history (if it exists)
    if message_index + 1 < len(chat["chatHistory"]) and chat["chatHistory"][message_index + 1]["role"] == "bot":
        chat["chatHistory"][message_index + 1]["message"] = bot_response
    else:
        # If no bot response exists, append a new one
        chat["chatHistory"].insert(message_index + 1, {"role": "bot", "message": bot_response})
    
    # Return the updated user input and regenerated bot response
    return {
        "success": True,
        "updatedUserInput": new_message,
        "botResponse": bot_response
    }
# createChat()
# interactWithChat("Chat1","How can i train my dog")
# getChat("Chat1")
# deleteChat("Chat1")

