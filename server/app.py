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
    return {"result": action}


@app.post("/set_level")
def set_level(payload: dict):
    return {"level": payload.get("level")}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
