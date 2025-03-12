import openai
from src.config import OPENAI_API_KEY

# Configure the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_completion(prompt, system_prompt, model="gpt-4o"):
    """
    Get a completion from the OpenAI API.
    
    Args:
        prompt (str): The user prompt to send to the model
        system_prompt (str): The system prompt to guide the model's behavior
        model (str): The model to use for completion
        
    Returns:
        str: The model's response
    """
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.output_text

def get_transcription(audio_file_path):
    """
    Transcribe an audio file using the OpenAI API.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: The transcribed text
    """
    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
    return response.text