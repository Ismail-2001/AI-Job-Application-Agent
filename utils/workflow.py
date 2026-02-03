import os
from typing import Dict, Any
from utils.event_bus import bus
from utils.profile_deduplicator import ProfileDeduplicator
from utils.document_builder import DocumentBuilder

class JobWorkflowManager:
    """
    Orchestrates the job application generation process using an event-driven approach.
    """
    def __init__(self, job_analyzer, match_calculator, company_researcher, cv_customizer, cover_letter_generator):
        self.job_analyzer = job_analyzer
        self.match_calculator = match_calculator
        self.company_researcher = company_researcher
        self.cv_customizer = cv_customizer
        self.cover_letter_generator = cover_letter_generator
        
        # Internal state for a single "run" (could be improved with run_id)
        self.current_state = {}

        # Register Listeners
        bus.subscribe("job_analyzed", self.on_job_analyzed)
        bus.subscribe("research_completed", self.on_research_completed)
        bus.subscribe("match_score_ready", self.on_match_score_ready)

    def start_workflow(self, job_description: str, profile: Dict[str, Any]):
        """Initiates the event-driven workflow."""
        self.current_state = {
            "job_description": job_description,
            "profile": ProfileDeduplicator.deduplicate_profile(profile),
            "analysis": None,
            "research": None,
            "match_data": None
        }
        
        # Step 1: Analyze
        analysis = self.job_analyzer.analyze(job_description)
        self.current_state["analysis"] = analysis
        bus.emit("job_analyzed", analysis)
        
        return self.current_state

    def on_job_analyzed(self, analysis: Dict[str, Any]):
        """Triggered when job analysis is finished."""
        # Step 2 & 3: Parallel-ish triggers
        company_name = analysis.get('role_info', {}).get('company', 'Unknown')
        
        # Emit research request
        research = self.company_researcher.research(company_name)
        self.current_state["research"] = research
        bus.emit("research_completed", research)
        
        # Calculate match
        match_data = self.match_calculator.calculate_match_score(
            self.current_state["profile"], 
            analysis
        )
        self.current_state["match_data"] = match_data
        bus.emit("match_score_ready", match_data)

    def on_research_completed(self, research: Dict[str, Any]):
        """Triggered when company research is finished."""
        # Logic to enrich the final documents
        pass

    def on_match_score_ready(self, match_data: Dict[str, Any]):
        """Triggered when match score is calculated."""
        # Logic to adjust tone based on match
        pass

    def finalize_documents(self):
        """Final generation step using all gathered data."""
        state = self.current_state
        
        # Customize CV (now enriched with research context)
        # Note: We can pass research tone to customizer later
        customized_cv = self.cv_customizer.customize(state["profile"], state["analysis"])
        customized_cv = ProfileDeduplicator.remove_repetitive_content(customized_cv)
        
        # Generate cover letter
        cover_letter_text = self.cover_letter_generator.generate(state["profile"], state["analysis"])
        
        return customized_cv, cover_letter_text
