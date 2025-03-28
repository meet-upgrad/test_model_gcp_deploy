from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from google.cloud import secretmanager_v1


def get_api_key():
    client = secretmanager_v1.SecretManagerServiceClient()
    request = secretmanager_v1.GetSecretRequest(name="OPENAI_API_KEY")
    response = client.get_secret(request=request)
    return response.secret_value


app = FastAPI()
api_key = get_api_key()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str


def get_answer(question):
    client = OpenAI(api_key=api_key)

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