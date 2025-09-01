from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
# import tempfile
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import json


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
# print("API_KEY:", API_KEY)  # Debugging line to check if the API key is loaded correctly

class MessageRequest(BaseModel):
    message: str

ram_data=f"""
Rameshwar Yadav
Analyst/Software Engineer
Core Competencies
▪ Proficient in Python
programming with hands-on
experience in FastAPI, Flask,
Docker, and database
management. Skilled in
developing efficient and
scalable applications using
modern frameworks and
tools.
▪ Generative AI :Expert in
Generative AI, specializing in
model fine-tuning, prompt
engineering, and creating AI-
driven applications.
© 2018 Sogeti. All rights reserved.
Professional Background
Skilled Python developer with 2+ years of
experience, proficient in Python, FastAPI,
Flask, Generative AI, and Docker.
Experienced in developing scalable
applications, automation scripts, and data-
driven solutions. Adept at collaborating
with cross-functional teams to optimize
performance and deliver high-quality
software solutions.
Education
▪ B.Tech in Computer Science Engineering
- Institute of Engineering & Technology,
DAVV, Indore.
Certification and Training
▪ Python Beginner and Practitioner
▪ Azure Fundamentals (AZ-900)
▪ Generative AI Bullseye Learning Challenge
Professional Tools and Skills
▪ Technical: Python, Generative AI, Prompt
Engineering, FastAPI, Flask, LangChain, SQL,
PostgreSQL, Azure Blob, Docker.
▪ Functional: Project Management, Strategic
Planning, Agile Methodology, and Excellent
Communication
▪ Gen AI Tools: GPT, Copilot
+91 8888888888
ryyadav1365@gmail.com
Experience
▪ J&J GEN AI Smart Assist Project:
Developed backend APIs using Python Flask and PostgreSQL, ensuring a robust
and scalable architecture for the J&J GEN AI Smart Assist POC. Worked on Azure
Blob Storage for efficient data handling and leveraged prompt engineering
techniques to enhance Generative AI capabilities. This solution enables users to
upload old briefing files, policy documents, and contextual text to generate
briefing documents using Generative AI. By integrating Azure OpenAI Search
and Retrieval-Augmented Generation (RAG), we ensured accurate and efficient
content generation. The project was successfully delivered, earning positive
feedback from the client.
▪ Skoda GenAI POC:
Developed a Generative AI POC with secure Azure Email OTP authentication,
featuring "Ask to Files," "Ask to URL," and "Document Comparison." Built with
Python and Flask, ensuring scalability, efficiency, and advanced data tracking for
analytics.
▪ Text to Image Search POC :
Developed an application for retrieving images from PDFs using advanced
algorithms, ranking, and metadata extraction. Built with Python, Flask, and
Streamlit, integrating OpenAI models for enhanced accuracy and efficiency.
▪ Face Similarity Checker POC :
Created a facial similarity detection tool using machine learning models for
precise comparison. Developed frontend and backend components with
Python, Flask, and Streamlit for seamless performance.
▪ Multimodal Search POC :
Designed a system to retrieve images from PDFs based on text input using
embeddings and similarity measures. Utilized CLIP for embedding generation
and FAISS for efficient image ranking and retrieval.
▪ Document Comparison POC :
Developed an AI-driven document comparison tool to identify and highlight
differences between text-based files. Built with Python, Flask, and OpenAI
models, ensuring accuracy, scalability, and seamless user experience.
"""

@app.post("/chat_bot_api")
async def chat_bot_api(req: MessageRequest):

    prompt = f"""
You are Ramy, a helpful and professional AI assistant representing Rameshwar Yadav.  
Your task is to answer the user's question: {req.message}  
using the available context: {ram_data}  

### Response Guidelines:
- Default language: **English** (switch only if the user explicitly requests another language).  
- Maintain a **polite, concise, and professional tone**.  
- If the answer is **short**, write it as a clear paragraph.  
- If the answer is **long or detailed**, organize it into **bullet points or numbered lists** for better readability.  
- For questions about a **specific project**, provide clear and relevant details.  
- For questions about **background**, give a brief but informative overview of experience and skills.  
- For questions about **technologies used**, provide a well-structured list of tools, frameworks, or libraries.  
- For questions about **education**, include academic background and any notable certifications.  
- If certain details are **not available**, politely state that and suggest contacting: **ryyadav1365@gmail.com**.  

### Important Constraints:
- Do **not** use filler phrases such as: *"Based on the provided information"*, *"As mentioned earlier"*, or similar.  
- Do **not** repeat your name in every response.  
- Do **not** repeat greetings if you have already greeted the user earlier in the conversation.  
- Keep responses **natural and human-like**, avoiding robotic phrasing.  
"""


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
            "content": prompt
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
