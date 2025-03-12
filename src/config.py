import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configurations
DEFAULT_MODEL = "gpt-4o"

# Application settings
APP_NAME = "PitchPilot"
APP_VERSION = "0.1.0"

# Agent system prompts
TRANSCRIPTION_SYSTEM_PROMPT = """
You are a transcription specialist. Your job is to accurately transcribe speech from 
sales calls into text, marking different speakers clearly.
"""

ANALYSIS_SYSTEM_PROMPT = """
You are an analysis specialist for sales calls. Your job is to understand the context 
of the conversation, identify key topics, detect customer objections, recognize 
questions, and determine the current stage of the sales process.
"""

RECOMMENDATION_SYSTEM_PROMPT = """
You are a recommendation specialist for sales calls. Based on the conversation analysis,
you provide real-time guidance from the company's sales playbook, suggest responses
to objections, and offer relevant competitive intelligence when needed.
"""

DOCUMENTATION_SYSTEM_PROMPT = """
You are a documentation specialist for sales calls. Your job is to generate comprehensive
post-call summaries with action items, follow-ups, and key insights from the conversation.
"""