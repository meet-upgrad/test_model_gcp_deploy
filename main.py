from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str


def get_answer(question):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You just need to answer the question!"},
            {"role": "user", "content": question}
        ],
        temperature=0.1,
        max_tokens=500
    )

    return response.choices[0].message.content

@app.get("/")
def health():
    return {"health": "ok"}

@app.post("/predict")
def predict(question: Request):
    return {"answer": get_answer(question.question)}