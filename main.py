from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile

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
