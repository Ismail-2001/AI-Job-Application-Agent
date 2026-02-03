"""
CV Customizer Agent
Role: Tailor the master profile to match specific job requirements.
"""

from typing import Dict, Any, List
from utils.deepseek_client import DeepSeekClient
import json

class CVCustomizer:
    """
    Agent responsible for rewriting CV content to target a specific job.
    """

    def __init__(self, client: DeepSeekClient):
        self.client = client
        self.system_instruction = """
        You are an expert Career Coach and Professional Resume Writer.
        Your goal is to rewrite candidate profiles to perfectly align with target job descriptions.
        You use the STAR method (Situation, Task, Action, Result) to quantify achievements.
        You ensure high ATS compliance by naturally integrating keywords.
        Return raw JSON only.
        """

    def customize(self, profile: Dict[str, Any], job_analysis: Dict[str, Any], relevant_snippets: List[Dict[str, Any]] = None, research: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Customize the candidate profile for the analyzed job.
        
        Args:
            profile: Candidates base profile
            job_analysis: Structured analysis of the target job
            relevant_snippets: (Optional) High-relevance snippets retrieved via RAG
            research: (Optional) Company research context (culture, tone, values)
            
        Returns:
            Customized profile dictionary ready for document generation
        """
        print("🎨 Customizing candidate profile using RAG and Research contexts...")
        
        # Format contexts for prompt
        rag_context = ""
        if relevant_snippets:
            rag_context = "\nPRIORITY CONTEXT (Top Relevant Experience):\n" + json.dumps(relevant_snippets, indent=2)

        research_context = ""
        if research:
            research_context = f"\nCOMPANY RESEARCH CONTEXT:\n{json.dumps(research, indent=2)}\nUse this to align the 'tone' and 'values' of the rewrite."

        prompt = f"""
        Tailor this candidate's profile to match the job requirements perfectly.
        {rag_context}
        {research_context}

        CANDIDATE BASE PROFILE:
        {json.dumps(profile, indent=2)}

        JOB ANALYSIS:
        {json.dumps(job_analysis, indent=2)}

        TASK:
        1. Rewrite the "Professional Summary" to highlight relevant experience and align with company culture.
        2. Reorder and filter "Core Skills" to prioritize the job's "must_have_skills".
        3. Select top 3-4 relevant "Work Experience" entries.
        4. Rewrite bullet points using STAR method and job-specific keywords.
        5. Ensure the tone matches the company's communication style (indicated in research context if available).
        
        OUTPUT FORMAT (JSON):
        {{
            "personal_info": {{ ...keep original... }},
            "summary": "Tailored summary...",
            "skills": {{
                "Technical": ["..."],
                "Soft Skills": ["..."]
            }},
            "experience": [
                {{
                    "company": "...",
                    "title": "...",
                    "dates": "...",
                    "achievements": [
                        "Optimized bullet point 1...",
                        "Optimized bullet point 2..."
                    ]
                }}
            ],
            "education": [ ...keep original... ]
        }}

        CRITICAL RULES:
        1. Do NOT invent experiences.
        2. Use EXACT vocabulary from the job analysis.
        3. Tone: {research.get('tone', 'Professional') if research else 'Professional'} (Adapt based on research context).
        4. Focus on impact and metrics.
        5. NO REPETITION.
        """

        # Temperature 0.5 for a balance of creativity and adherence to facts
        return self.client.generate_json(prompt, system_instruction=self.system_instruction, temperature=0.5)
