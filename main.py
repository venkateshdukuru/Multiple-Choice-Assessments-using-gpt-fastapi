from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

openai.api_key = os.environ.get('api_key')

class QuestionRequest(BaseModel):
    topic: str
    num_questions: int

@app.post("/generate-questions/")
async def generate_questions(request: QuestionRequest):
    prompt = f"Generate {request.num_questions} multiple choice questions on the topic of {request.topic}. After generating all the MCQs, provide the correct answers for each question."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return {"questions": response['choices'][0]['message']['content']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
