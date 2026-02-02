"""
FastAPI Server for AI Job Agent
Role: Expose the agentic workflow as a scalable API with file downloads.
"""

import os
import uuid
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Import components
from utils.deepseek_client import DeepSeekClient
from utils.document_builder import DocumentBuilder
from utils.rag_engine import RAGEngine
from agents.job_analyzer import JobAnalyzer
from agents.cv_customizer import CVCustomizer
from agents.cover_letter_generator import CoverLetterGenerator

# Load config
load_dotenv()

app = FastAPI(title="AI Job Application Agent API")

# Add CORS middleware to allow requests from web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for easier development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize global engines
api_key = os.getenv("DEEPSEEK_API_KEY")
client = DeepSeekClient(api_key=api_key)
rag_engine = RAGEngine()
job_analyzer = JobAnalyzer(client)
cv_customizer = CVCustomizer(client)
cover_letter_generator = CoverLetterGenerator(client)
doc_builder = DocumentBuilder()

class JobRequest(BaseModel):
    job_description: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Agentic AI Job Platform API is healthy"}

@app.post("/apply")
async def process_application(request: JobRequest):
    """
    End-to-end application workflow:
    Analysis -> RAG Retrieval -> Customization -> Generation
    """
    try:
        # 1. Analyze
        analysis = job_analyzer.analyze(request.job_description)
        
        # 2. RAG Retrieval (Strategic Improvement)
        keywords = analysis.get("keywords", {}).get("ats_keywords", [])
        relevant_snippets = rag_engine.retrieve_relevant_experience(keywords)
        
        # 3. Customize with RAG context
        import json
        with open("data/master_profile.json", "r") as f:
            profile = json.load(f)
            
        customized_cv = cv_customizer.customize(profile, analysis, relevant_snippets)
        cover_letter = cover_letter_generator.generate(profile, analysis)

        # 4. Generate Files with unique ID for download
        import re
        def sanitize(name): return re.sub(r'[<>:"/\\|?*]', '', str(name)).strip().replace(' ', '_')
        
        role = sanitize(analysis.get('role_info', {}).get('title', 'Job'))
        company = sanitize(analysis.get('role_info', {}).get('company', 'Company'))
        
        # Use unique ID to prevent file conflicts
        unique_id = str(uuid.uuid4())[:8]
        
        cv_filename = f"CV_{company}_{role}_{unique_id}.docx"
        cl_filename = f"CL_{company}_{role}_{unique_id}.docx"
        
        cv_path = os.path.join(OUTPUT_DIR, cv_filename)
        cl_path = os.path.join(OUTPUT_DIR, cl_filename)
        
        doc_builder.create_cv(customized_cv, cv_path)
        doc_builder.create_cover_letter(cover_letter, profile, cl_path)

        return {
            "success": True,
            "analysis": analysis,
            "files": {
                "cv": cv_filename,
                "cover_letter": cl_filename
            },
            "download_urls": {
                "cv": f"/download/{cv_filename}",
                "cover_letter": f"/download/{cl_filename}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated CV or Cover Letter"""
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
