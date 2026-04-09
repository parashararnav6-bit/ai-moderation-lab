from openai import OpenAI
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI()


client = None
if "API_KEY" in os.environ and "API_BASE_URL" in os.environ:
    client = OpenAI(
        api_key=os.environ["API_KEY"],
        base_url=os.environ["API_BASE_URL"]
    )



class Observation(BaseModel):
    item_id: str
    post: str
    context: str
    user_history: str
    difficulty: str

class ActionResponse(BaseModel):
    decision: str
    reasoning: str
    rewrite: str | None = None



def load_all_tasks():
    """Load all task files from data/ folder"""
    tasks = []
    data_dir = Path(__file__).parent.parent / "data"
    
    for difficulty in ["easy", "medium", "hard"]:
        json_path = data_dir / f"{difficulty}.json"
        if json_path.exists():
            with open(json_path) as f:
                task_data = json.load(f)
                tasks.append(task_data)
    
    return tasks


def get_moderation_decision(post: str, context: str) -> dict:
    """Call OpenAI to get moderation decision"""
    
    if client:
        try:
            prompt = f"""You are a content moderator. Analyze this post and decide: allow, flag, remove, or escalate.
Context: {context}
Post: {post}
Respond in JSON format:
{{"decision": "allow|flag|remove|escalate", "reasoning": "brief explanation"}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a content moderation AI. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            
            
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback response
    return {
        "decision": "flag",
        "reasoning": "Unable to process with AI, defaulting to flag for human review."
    }



@app.get("/")
def root():
    return {"status": "ok", "tasks_available": len(load_all_tasks())}

@app.get("/tasks")
async def get_tasks():
    """OpenEnv calls this to discover tasks and graders"""
    tasks = load_all_tasks()
    return {"tasks": tasks}

@app.get("/tasks/{task_name}")
async def get_task(task_name: str):
    """OpenEnv calls this to get a specific task"""
    data_dir = Path(__file__).parent.parent / "data"
    json_path = data_dir / f"{task_name}.json"
    
    if json_path.exists():
        with open(json_path) as f:
            return json.load(f)
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/act")
async def act(observation: Observation):
    """OpenEnv calls this for each inference"""
    
    
    result = get_moderation_decision(
        post=observation.post,
        context=observation.context
    )
    
    return ActionResponse(
        decision=result.get("decision", "flag"),
        reasoning=result.get("reasoning", "No reasoning provided"),
        rewrite=None
    )


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
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=True)

if __name__ == "__main__":
    main()
