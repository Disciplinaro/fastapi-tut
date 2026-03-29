from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"
class PromptRequest(BaseModel):
    model: str
    prompt: str


@app.post("/generate")
def generate(request: PromptRequest):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": request.prompt,
                "stream": False
            }
        )

        print("Status:", response.status_code)
        print("Raw response:", response.text)

        if response.status_code != 200:
            return {
                "error": response.text,
                "status_code": response.status_code
            }

        return {"response": response.json()['response']}

    except Exception as e:
        return {"error": str(e)}
