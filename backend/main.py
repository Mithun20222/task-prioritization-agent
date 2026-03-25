from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.genai as genai
import os
import ast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"


class TaskInput(BaseModel):
    user_input: str


def extract_tasks(user_input):
    prompt = f"""
    Extract tasks from the sentence.
    Return ONLY a Python list of strings.
    No explanation. No markdown.
    Input: {user_input}
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()
    if "```" in text:
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else parts[0]
        text = text.replace("python", "").strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError(f"Invalid response format: {text}")
    text = text[start:end]
    return ast.literal_eval(text)


def classify_task(task):
    prompt = f"""
    Classify this task into one category:
    URGENT, IMPORTANT, LOW
    Return only one word.
    Task: {task}
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip().upper()
    return text.split()[0]


def schedule_task(priority):
    if priority == "URGENT":
        return "Today (6 PM)"
    elif priority == "IMPORTANT":
        return "Tomorrow"
    else:
        return "Weekend"


def agent(user_input):
    tasks = extract_tasks(user_input)
    results = []
    for task in tasks:
        priority = classify_task(task)
        time = schedule_task(priority)
        results.append({"task": task, "priority": priority, "time": time})
    order = {"URGENT": 1, "IMPORTANT": 2, "LOW": 3}
    results.sort(key=lambda x: order.get(x["priority"], 4))
    return results


@app.post("/process")
def process_tasks(body: TaskInput):
    try:
        results = agent(body.user_input)
        return {"tasks": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
