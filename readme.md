# Chatbot

This project is a chatbot application built using **FastAPI** and **Google Generative AI**. It allows users to interact with a chatbot powered by Google's generative AI model, with session-based chat history and a web interface.

## Features

- **FastAPI Framework**: Provides a lightweight and efficient backend for handling API requests.
- **Google Generative AI Integration**: Uses the `google-generativeai` library to generate chatbot responses.
- **Session Management**: Maintains chat history using session middleware.
- **Template Rendering**: Uses Jinja2 templates for rendering the chat interface.
- **Environment Configuration**: API keys and other sensitive data are securely loaded from a `.env` file.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- A virtual environment (optional but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Muthan111/Chatbot.git
   cd ChatbotAssignment
   ```
2. ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create .env file
   API_KEY=

5. Run the application:
   ```bash
   uvicorn main:app --reload

   ```
