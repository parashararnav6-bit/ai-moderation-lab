from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv["API_KEY"],
    base_url=os.getenv["API_BASE_URL"]
)
from fastapi import FastAPI

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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a content moderation assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        result = response.choices[0].message.content
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}

@app.post("/set_level")
def set_level(payload: dict):
    return {"level": payload.get("level")}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
