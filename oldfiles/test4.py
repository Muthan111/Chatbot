import google.generativeai as genai

genai.configure(api_key="AIzaSyDSbw52Qq4EjJ_nBoQvEUst3IXZwlhAOE8")
model = genai.GenerativeModel("gemini-2.0-pro-exp")

previousChat = [
    #chatId
    #chatName
    #chatHistory : []
]
# Function to generate a unique chat ID
def generateChatId():
    if previousChat:
        return max(chat["chatId"] for chat in previousChat) + 1
    return 1  # Start with ID 1 if no chats exist

# Function to generate a chat name
def generateChatName(baseName):
    existingNames = [chat["chatName"] for chat in previousChat]
    if baseName not in existingNames:
        return baseName
    # Append a number to make the name unique
    counter = 1
    while f"{baseName} ({counter})" in existingNames:
        counter += 1
    return f"{baseName} ({counter})"



def createChat():
    chatId = generateChatId()
    chatName = generateChatName("Chat1")
    chat = {
        "chatId": chatId,
        "chatName": chatName,
        "chatHistory": []
    }
    previousChat.append(chat)
    return chat

def getChat(chatname):
    for chat in previousChat:
        if chat["chatName"] == chatname:
            history = chat["chatHistory"]
            # Convert history to plain text
            plain_text = "\n".join([f"{item['role'].capitalize()}: {item['message']}" for item in history])
            print(plain_text)
            return plain_text  # Return the plain text representation
    return None

def interactWithChat(chatname,userinput):
    for chat in previousChat:
        if chat["chatName"] == chatname:
            history = chat["chatHistory"]
            addinput = userinput
            response = model.generate_content(addinput)
            history.append({"role": "user", "message": addinput})
            history.append({"role": "bot", "message": response.text})
            plain_text = "\n".join([f"{item['role'].capitalize()}: {item['message']}" for item in history])
            print(plain_text)
            return plain_text  # Exit the loop once the chat is found
    return None

def deleteChat(chatname):
    for chat in previousChat:
        if chat["chatName"] == chatname:
            previousChat.remove(chat)
            print(f"Chat '{chatname}' deleted.")
            return chatname
    return None
createChat()
interactWithChat("Chat1","How can i train my dog")
getChat("Chat1")
deleteChat("Chat1")

