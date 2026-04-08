from openai import OpenAI
import os
from fastapi import FastAPI


if "API_BASE_URL" in os.environ and "API_KEY" in os.environ:
    client = OpenAI(
        api_key=os.environ["API_KEY"],
        base_url=os.environ["API_BASE_URL"]
    )
else:
   
    client = None

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/reset")
def reset_get():
    return {"msg": "reset"}

@app.post("/reset")
def reset_post():
    return {"msg": "reset"}

@app.get("/state")
def state():
    return {"state": "ok"}

@app.post("/step")
def step(action: dict):
    user_input = action.get("input") or str(action)

    if client is None:
        
        return {"result": "mock response"}


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a moderation assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return {"result": response.choices[0].message.content}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
