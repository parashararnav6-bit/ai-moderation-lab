import os
import json
from openai import OpenAI


client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

def inference(input_data):
    
    
    prompt = input_data.get("prompt", "")
    
    
    response = client.chat.completions.create(
        model="openai/gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    
    result = response.choices[0].message.content
    
    
    return {
        "output": result
    }

if __name__ == "__main__":
   
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            input_data = json.load(f)
    else:
        input_data = json.load(sys.stdin)
    
    output = inference(input_data)
    print(json.dumps(output))
