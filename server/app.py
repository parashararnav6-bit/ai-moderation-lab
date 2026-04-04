from fastapi import FastAPI
from env.environment import Environment

app = FastAPI()
env = Environment()


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/reset")
def reset_get():
    return env.reset()


@app.post("/reset")
def reset_post():
    return env.reset()


@app.get("/state")
def get_state():
    return env.state()


@app.post("/step")
def step(action: dict):
    return env.step(action)


@app.post("/set_level")
def set_level(payload: dict):
    return env.set_level(payload["level"])


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
