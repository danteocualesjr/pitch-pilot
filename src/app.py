from src.config import APP_NAME, APP_VERSION
from src.agents.agent_logic import (
    TranscriptionAgent,
    AnalysisAgent,
    RecommendationAgent,
    DocumentationAgent
)

def initialize_agents():
    """Initialize all agents needed for the application."""
    transcription_agent = TranscriptionAgent()
    analysis_agent = AnalysisAgent()
    recommendation_agent = RecommendationAgent()
    documentation_agent = DocumentationAgent()
    
    print(f"Initialized agents for {APP_NAME} v{APP_VERSION}")
    return {
        "transcription": transcription_agent,
        "analysis": analysis_agent,
        "recommendation": recommendation_agent,
        "documentation": documentation_agent
    }

def process_conversation(agents, conversation_text):
    """
    Process a conversation through the agent pipeline.
    
    Args:
        agents (dict): Dictionary of agent instances
        conversation_text (str): Text of the conversation to process
        
    Returns:
        dict: Results from each agent
    """
    results = {}
    
    # Step 1: Clean and structure the transcription
    results["transcription"] = agents["transcription"].process(conversation_text)
    
    # Step 2: Analyze the conversation
    results["analysis"] = agents["analysis"].process(results["transcription"])
    
    # Step 3: Generate recommendations
    results["recommendations"] = agents["recommendation"].process(
        results["transcription"],
        results["analysis"]
    )
    
    # Step 4: Create documentation
    results["documentation"] = agents["documentation"].process(
        results["transcription"],
        results["analysis"],
        results["recommendations"]
    )
    
    return results

def main():
    """Main entry point for the application."""
    print(f"Starting {APP_NAME} v{APP_VERSION}...")
    agents = initialize_agents()
    print("Agents initialized successfully.")
    
    # Simple demo with a mock conversation
    mock_conversation = """
    Salesperson: Hi there, thanks for taking my call. I'm John from TechSolutions. How are you doing today?
    
    Prospect: I'm doing fine, thanks. What can I help you with?
    
    Salesperson: I noticed your company has been growing rapidly in the last year. Congratulations on that success! I'm reaching out because many companies in your position struggle with scaling their customer support infrastructure. Is that something your team is experiencing?
    
    Prospect: Actually, yes. As we've grown, our support team has been overwhelmed. We're getting more tickets than we can handle efficiently.
    
    Salesperson: I understand that challenge. What solutions have you tried so far?
    
    Prospect: We've mainly just been hiring more people, but the training takes time and it's expensive. We've looked into some ticketing systems but haven't made a decision yet.
    
    Salesperson: That makes sense. Many of our clients faced the same challenges before implementing our AI-powered support solution. It can reduce ticket resolution time by 40% and handles about 60% of routine inquiries automatically. Would something like that be valuable to your team?
    
    Prospect: That sounds interesting, but we've heard claims about AI before that didn't pan out. How is yours different?
    
    Salesperson: That's a fair question. Unlike general AI solutions, ours is specifically trained on customer support scenarios in your industry. We also don't just drop it in and leave - we have a 4-week implementation process where we customize it to your specific products and services. Would you be open to a quick demo so you can see it in action?
    """
    
    results = process_conversation(agents, mock_conversation)
    
    print("\nDemo Results:")
    print("\n--- Analysis ---")
    print(results["analysis"])
    print("\n--- Recommendations ---")
    print(results["recommendations"])
    print("\n--- Documentation ---")
    print(results["documentation"])

if __name__ == "__main__":
    main()