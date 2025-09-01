from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
# import tempfile
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")# take environment variables from .env.

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with ["https://your-frontend.github.io"] after deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running 🎉"}

@app.post("/generate-pdf")
def generate_pdf(data: dict):
    text = data.get("text", "Empty PDF")
    pdf_path = ""

    with open(pdf_path, "w") as f:
        f.write(text)

    return FileResponse(pdf_path, filename="output.pdf", media_type="application/pdf")




class MessageRequest(BaseModel):
    message: str


URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get("OPENROUTER_API_KEY") # load from env variable
print("API_KEY:", API_KEY)  # Debugging line to check if the API key is loaded correctly

class MessageRequest(BaseModel):
    message: str

@app.post("/chat_bot_api")
async def chat_bot_api(req: MessageRequest):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "google/gemma-3-12b-it:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req.message}
        ]
    }


    import requests
    import json

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
        {
            "role": "user",
            "content": req.message
        }
        ],
        
    })
    )

    # Check if the response is successful
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"].strip()
    else:
        answer = "Error: Unable to retrieve response"

    return {"response": answer}
