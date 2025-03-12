from src.utils.openai_client import get_completion
from src.config import (
    TRANSCRIPTION_SYSTEM_PROMPT,
    ANALYSIS_SYSTEM_PROMPT,
    RECOMMENDATION_SYSTEM_PROMPT,
    DOCUMENTATION_SYSTEM_PROMPT,
    DEFAULT_MODEL
)

class TranscriptionAgent:
    """Handles transcription of sales calls."""
    
    def process(self, text):
        """Process the input text and return a clean transcription."""
        return get_completion(
            prompt=text,
            system_prompt=TRANSCRIPTION_SYSTEM_PROMPT,
            model=DEFAULT_MODEL
        )

class AnalysisAgent:
    """Analyzes sales conversations for context, objections, and questions."""
    
    def process(self, transcript):
        """Analyze the transcript and return insights."""
        return get_completion(
            prompt=f"Analyze this sales conversation transcript: {transcript}",
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            model=DEFAULT_MODEL
        )

class RecommendationAgent:
    """Provides recommendations based on conversation analysis."""
    
    def process(self, transcript, analysis):
        """Generate recommendations based on transcript and analysis."""
        prompt = f"""
        Transcript: {transcript}
        
        Analysis: {analysis}
        
        Based on this information, provide real-time guidance, 
        suggested responses, and relevant competitive intelligence.
        """
        return get_completion(
            prompt=prompt,
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
            model=DEFAULT_MODEL
        )

class DocumentationAgent:
    """Generates documentation and summaries of sales calls."""
    
    def process(self, transcript, analysis, recommendations):
        """Generate a comprehensive call summary with action items."""
        prompt = f"""
        Transcript: {transcript}
        
        Analysis: {analysis}
        
        Recommendations: {recommendations}
        
        Generate a comprehensive call summary with action items, 
        follow-ups, and key insights.
        """
        return get_completion(
            prompt=prompt,
            system_prompt=DOCUMENTATION_SYSTEM_PROMPT,
            model=DEFAULT_MODEL
        )