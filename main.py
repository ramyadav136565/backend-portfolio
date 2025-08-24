from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from openai import OpenAI
from pydantic import BaseModel


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
    pdf_path = tempfile.gettempdir() + "/output.pdf"

    with open(pdf_path, "w") as f:
        f.write(text)

    return FileResponse(pdf_path, filename="output.pdf", media_type="application/pdf")





# Request schema
class MessageRequest(BaseModel):
    message: str

# OpenAI-compatible client
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

@app.post("/chat_bot_api")
async def chat_bot_api(req: MessageRequest):
    prompt = [
        {"role": "system", "content": "You are a helpful assistant.answer the question concisely."},
        {"role": "user", "content": req.message}
    ]

    response = client.chat.completions.create(
        model="google/gemma-3-12b-it:free",
        messages=prompt
    )

    return {"response": response.choices[0].message["content"].strip()}
