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

    response = requests.post(URL, headers=headers, json=data, timeout=30)
    response.raise_for_status()

    answer = response.json()["choices"][0]["message"]["content"].strip()
    return {"response": answer}
