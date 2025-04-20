from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.components.interview import process_interview

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/interview")
async def start_interview(resume: UploadFile, jobdesc: UploadFile, difficulty: str = Form("medium")):
    return await process_interview(resume, jobdesc, difficulty)