from fastapi import FastAPI, Form
from pydantic import BaseModel
import os
import openai

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Text Summarizer API"}

# Set the Together API key
os.environ["TOGETHER_API_KEY"] = "0bc66dcded6a57c5aca11ec7f61089f423307023ba560e3b3178fb36c7923a10"

# Create the OpenAI client
client = openai.OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
)

@app.post("/summarize")
def summerizer(text: str = Form()):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "You are a professional summarizer assistant. Just provide a summary only."},
            {"role": "user", "content": text}
        ]
    )
    result = response.choices[0].message.content
    return {"Summary": result}
