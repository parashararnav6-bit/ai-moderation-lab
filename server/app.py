from openai import OpenAI
import os
from fastapi import FastAPI

client = OpenAI(
    api_key=os.environ.get("API_KEY", "test"),
    base_url=os.environ.get("API_BASE_URL", "https://example.com")
)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/step")
def step(action: dict):
    user_input = action.get("input") or str(action)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a content moderation assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return {"result": response.choices[0].message.content}
