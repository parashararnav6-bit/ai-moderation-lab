from openai import OpenAI
import os
from fastapi import FastAPI

app = FastAPI()



client = None
if "API_KEY" in os.environ and "API_BASE_URL" in os.environ:
    client = OpenAI(
        api_key=os.environ["API_KEY"],
        base_url=os.environ["API_BASE_URL"]
    )

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    return {"msg": "reset"}

@app.get("/state")
def state():
    return {"state": "ok"}

@app.post("/step")
def step(action: dict):
    user_input = action.get("input", "test")

   
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Moderate content"},
                    {"role": "user", "content": user_input}
                ]
            )
            return {"result": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)}

    
    return {"result": "fallback"}
    
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
