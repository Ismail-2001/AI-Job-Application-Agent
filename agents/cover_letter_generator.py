"""
Cover Letter Generator Agent
Role: Generate personalized, compelling cover letters matching the job and candidate profile.
"""

import json
from typing import Dict, Any
from utils.deepseek_client import DeepSeekClient

class CoverLetterGenerator:
    """
    Agent responsible for writing cover letters.
    """
    
    def __init__(self, client: DeepSeekClient):
        self.client = client
        self.system_instruction = """
        You are an expert Career Coach and Copywriter specializing in cover letters.
        Your goal is to write compelling, personalized letters that connect the candidate's unique value to the company's needs.
        You avoid generic clichés (e.g., "I am writing to apply...").
        You use a professional yet enthusiastic tone.
        """

    def generate(self, profile: Dict[str, Any], job_analysis: Dict[str, Any], research: Dict[str, Any] = None) -> str:
        """
        Generate a cover letter.

        Args:
            profile: Candidate's master profile
            job_analysis: Analyzed job requirements
            research: (Optional) Company research context

        Returns:
            The body of the cover letter text.
        """
        print("✍️  Writing cover letter...")
        
        research_context = ""
        if research:
            research_context = f"\nCOMPANY RESEARCH CONTEXT:\n{json.dumps(research, indent=2)}\nUse this to deeply personalize Paragraph 2."

        prompt = f"""
        Create a compelling cover letter for this job application.
        {research_context}

        CANDIDATE PROFILE:
        {json.dumps(profile, indent=2)}

        JOB ANALYSIS:
        {json.dumps(job_analysis, indent=2)}

        STRUCTURE:
        Paragraph 1 (Opening): Strong hook + excitement about the specific role/company.
        Paragraph 2 (The Match): Why THIS company? Connect their mission/culture (from research context if available) to your background.
        Paragraph 3 (The Proof): Highlight the most relevant achievement from the profile.
        Paragraph 4 (Closing): Call to action and sign-off.

        CRITICAL RULES:
        1. Tone: {research.get('tone', 'Professional') if research else 'Professional'} (Adapt based on research).
        2. Length: 250-350 words.
        3. Use specific keywords from the job analysis.
        4. "Show, don't just tell" - use metrics from the profile.
        """

        # Temperature 0.7 for creativity/personality
        return self.client.generate_content(
            prompt, 
            system_instruction=self.system_instruction, 
            config={"temperature": 0.7}
        )
