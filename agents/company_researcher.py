from typing import Dict, Any
from utils.deepseek_client import DeepSeekClient

class CompanyResearcher:
    """
    Agent responsible for gathering additional context about the company
    to further personalize the application.
    """
    def __init__(self, client: DeepSeekClient):
        self.client = client

    def research(self, company_name: str) -> Dict[str, Any]:
        """
        Research company culture, values, and recent news.
        (In a real version, this might use a SerpAPI or Web Scraper)
        """
        if not company_name or company_name == "Unknown":
            return {"culture": "Professional", "values": []}

        print(f"🕵️ Researching company: {company_name}")
        
        prompt = f"""
        Provide a brief overview of the company culture, core values, and communication tone for: {company_name}.
        If you don't have specific info, provide general best practices for this industry.
        
        Return JSON structure:
        {{
            "culture": "Description of culture",
            "values": ["Value 1", "Value 2"],
            "tone": "Formal/Creative/Technical"
        }}
        """
        
        try:
            return self.client.generate_json(prompt, temperature=0.3)
        except:
            return {"culture": "Innovative and Professional", "values": ["Innovation"], "tone": "Professional"}
