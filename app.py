from fastapi import FastAPI , Form
from pydantic import BaseModel
import os
import openai


app = FastAPI()

os.environ["TOGETHER_API_KEY"] ="0bc66dcded6a57c5aca11ec7f61089f423307023ba560e3b3178fb36c7923a10"

# Option 2: Using a POST request with a JSON body
class Numbers(BaseModel):
    a: float
    b: float

@app.post("/sum")
def post_sum(numbers: Numbers):
    return {"sum": numbers.a + numbers.b}


@app.post("/multiply")
def post_sum(numbers: Numbers):
    return {"multiply": numbers.a * numbers.b}


@app.post("/subtract")
def post_sum(numbers: Numbers):
    return {"subtract": numbers.a - numbers.b}


@app.post("/divide")
def post_sum(numbers: Numbers):
    return {"divide": numbers.a / numbers.b}


client = openai.OpenAI(
  api_key=os.environ.get("TOGETHER_API_KEY"),
  base_url="https://api.together.xyz/v1",
)

@app.post("/summarize")
def summerizer(text: str=Form()):
    response = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[
    {"role": "system", "content": "You are a professional summerizer assistant.Just only provide summary with no additonal content."},
    {"role": "user", "content":text}
  ]
)
    result  = response.choices[0].message.content
    return {"Summary":result}
