import os
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from compiler import compile_skill, save_skill

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory store: { uuid: skill_content }
skills_store = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    context: str = Form(...),
    bad_behaviors: str = Form(...),
    forbidden_topics: str = Form(default=""),
    style_hates: str = Form(default=""),
    severity: str = Form(default="moderate"),
):
    # Convert textarea line-by-line input into lists, same as the CLI does
    answers = {
        "context": context,
        "bad_behaviors": [b.strip() for b in bad_behaviors.strip().splitlines() if b.strip()],
        "forbidden_topics": [t.strip() for t in forbidden_topics.strip().splitlines() if t.strip()],
        "style_hates": style_hates,
        "severity": severity,
    }

    skill_content = compile_skill(answers)

    # Save to disk (your existing function)
    save_skill(skill_content, answers["context"])

    # Also store with a UUID for the shareable URL
    skill_id = str(uuid.uuid4())[:8]
    skills_store[skill_id] = skill_content

    return templates.TemplateResponse("result.html", {
        "request": request,
        "skill_content": skill_content,
        "skill_id": skill_id,
    })


@app.get("/skill/{skill_id}", response_class=HTMLResponse)
async def view_skill(request: Request, skill_id: str):
    skill_content = skills_store.get(skill_id)
    if not skill_content:
        return HTMLResponse("<h2>Skill not found or expired.</h2>", status_code=404)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "skill_content": skill_content,
        "skill_id": skill_id,
    })