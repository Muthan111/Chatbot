let selectedChatName = "Chat1"; 

async function selectChat(chatName) {
    selectedChatName = chatName;
    
    try {
        const response = await fetch(`/getChat?chatname=${encodeURIComponent(chatName)}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const chatHistory = await fetch(`/getChatHistory?chatname=${encodeURIComponent(chatName)}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error('Failed to fetch chat data');

        const data = await response.json();
        const chatHistoryData = await chatHistory.json();
        console.log(chatHistoryData);

        document.getElementById("chatBox").innerHTML = `<p><strong>${chatName}</strong></p>`;
        if (data.messages) {
            data.messages.forEach(message => {
                document.getElementById("chatBox").innerHTML += `<p>${message}</p>`;
            });
        }

        const historyElement = document.getElementById("history");
        historyElement.innerHTML = "";
        if (Array.isArray(chatHistoryData)) {
            chatHistoryData.forEach(message => {
                historyElement.innerHTML += `<p><strong>${message.role}:</strong> ${message.message}</p>`;
            });
        } else {
            historyElement.innerHTML = "<p>No chat history available.</p>";
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("chatBox").innerHTML = `<p>Error loading chat</p>`;
    }
}

async function sendMessage() {
    try {
        const userInput = document.getElementById("userInput").value;
        if (!userInput) {
            alert("Please enter a message.");
            return;
        }

        const chatName = selectedChatName;
        const url = `/interactWithChat?chatname=${encodeURIComponent(chatName)}&message=${encodeURIComponent(userInput)}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error('Failed to interact with chat');

        const data = await response.json();
        document.getElementById("chatBox").innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
        document.getElementById("chatBox").innerHTML += `<p><strong>Bot:</strong> ${data.botResponse}</p>`;

        document.getElementById("userInput").value = "";
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("chatBox").innerHTML += `<p>Error interacting with chat</p>`;
    }
}
