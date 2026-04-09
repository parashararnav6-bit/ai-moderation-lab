import os
from openai import OpenAI

class PolicyAgent:
    def __init__(self):
        
        self.client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )
        self.model = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    
    def act(self, observation):
        """Called for each moderation task."""
        post = observation.get("post", "")
        context = observation.get("context", "")
        user_history = observation.get("user_history", [])
        difficulty = observation.get("difficulty", "easy")
        
        prompt = self._build_prompt(post, context, user_history, difficulty)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        
    
        return self._parse_response(response.choices[0].message.content)
    
    def _build_prompt(self, post, context, user_history, difficulty):
        return f"""You are a content moderator. Decide: allow, flag, remove, or escalate.

Post: {post}
Context: {context}
User History: {user_history}
Difficulty: {difficulty}

Respond in JSON format:
{{"decision": "<allow|flag|remove|escalate>", "reasoning": "<explanation>"}}
"""
    
    def _parse_response(self, content):
        import json
        try:
            return json.loads(content)
        except:
            return {"decision": "flag", "reasoning": "Failed to parse, defaulting to flag."}
