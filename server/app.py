from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from env.environment import ModerationEnv
from env.models import Action

app = FastAPI(title="AI Moderation Lab")

env = ModerationEnv(level="easy")
app.mount("/static", StaticFiles(directory="static"), name="static")


class LevelRequest(BaseModel):
    level: str


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health():
    return {"status": "AI Moderation Env Running"}

@app.get("/reset")
def reset_get():
    return env.reset()

@app.post("/reset")
def reset_post():
    return env.reset()

@app.get("/state")
def get_state():
    return env.state()


@app.post("/set_level")
def set_level(payload: LevelRequest):
    return env.set_level(payload.level)


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.model_dump() if obs else None,
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }
    def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
