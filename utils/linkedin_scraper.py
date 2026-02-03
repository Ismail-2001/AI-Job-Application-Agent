"""
LinkedIn Profile Scraper
Extracts profile data from LinkedIn using web scraping.
Note: For production, use LinkedIn's official API with proper OAuth.
"""

import os
import json
import re
from typing import Dict, Any, Optional
from utils.schemas import Profile

class LinkedInScraper:
    """
    Scrapes LinkedIn profile data.
    Uses AI to parse the raw HTML/text content into structured data.
    """
    
    def __init__(self, llm_client=None):
        """Initialize with optional LLM client for smart parsing"""
        self.llm_client = llm_client
    
    def parse_profile_text(self, profile_text: str) -> Dict[str, Any]:
        """
        Parse raw LinkedIn profile text/content into structured format.
        Uses LLM for intelligent extraction.
        """
        if not self.llm_client:
            raise ValueError("LLM client required for parsing")
        
        prompt = f"""
        Parse this LinkedIn profile content and extract structured information.
        
        LINKEDIN PROFILE CONTENT:
        {profile_text[:8000]}
        
        OUTPUT FORMAT (JSON):
        {{
            "personal_info": {{
                "name": "Full Name",
                "email": "email if visible",
                "phone": "phone if visible", 
                "linkedin": "LinkedIn URL",
                "location": "City, Country"
            }},
            "summary": "Professional summary/about section",
            "skills": {{
                "Technical": ["Skill 1"],
                "Soft Skills": ["Skill 2"]
            }},
            "experience": [
                {{
                    "company": "Company Name",
                    "title": "Job Title",
                    "dates": "Start - End",
                    "location": "Location",
                    "responsibilities": ["Task 1"]
                }}
            ],
            "education": [
                {{
                    "school": "University Name",
                    "degree": "Degree Type",
                    "field": "Field of Study",
                    "dates": "Start - End"
                }}
            ],
            "certifications": ["Cert 1"]
        }}
        
        RULES:
        1. Extract ALL work experience entries
        2. Convert responsibilities to achievement-focused bullet points
        3. If data is not available, use null or empty array
        4. Return ONLY valid JSON
        """
        
        result = self.llm_client.generate_json(prompt, temperature=0.2)
        
        # Pydantic Validation
        return Profile.model_validate(result).model_dump()
    
    def create_master_profile(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure data is in master_profile format.
        """
        # Since parse_profile_text already validates using Profile, 
        # this is now just a pass-through or final check.
        return Profile.model_validate(parsed_data).model_dump()
    
    def save_master_profile(self, profile: Dict[str, Any], path: str = "data/master_profile.json"):
        """Save the profile to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return path



def import_from_linkedin_text(profile_text: str, llm_client) -> Dict[str, Any]:
    """
    Main function to import LinkedIn profile from pasted text.
    
    Args:
        profile_text: Raw text copied from LinkedIn profile page
        llm_client: DeepSeek or other LLM client for parsing
    
    Returns:
        Parsed and saved master profile
    """
    scraper = LinkedInScraper(llm_client)
    
    # Parse the profile text
    parsed_data = scraper.parse_profile_text(profile_text)
    
    # Convert to master profile format
    master_profile = scraper.create_master_profile(parsed_data)
    
    # Save to file
    scraper.save_master_profile(master_profile)
    
    return master_profile
