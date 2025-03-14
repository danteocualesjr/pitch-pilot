import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from src.config import APP_NAME, APP_VERSION
from src.agents.agent_logic import (
    TranscriptionAgent,
    AnalysisAgent,
    RecommendationAgent,
    DocumentationAgent
)

# Initialize FastAPI app

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Create templates and static directories if they don't exist

os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Create a simple HTML template

with open("templates/index.html", "w") as f:
    f.write("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PitchPilot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; }
            textarea { width: 100%; height: 200px; padding: 12px; margin: 10px 0; border: 1px solid #ddd; }
            button { background-color: #3498db; color: white; border: none; padding: 10px 20px; cursor: pointer; }
            button:hover { background-color: #2980b9; }
            .result { margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
            .tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; }
            .tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; }
            .tab button:hover { background-color: #ddd; }
            .tab button.active { background-color: #ccc; }
            .tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }
            .tabcontent.active { display: block; }
        </style>
    </head>
    <body>
        <h1>PitchPilot - Sales Playbook Coach</h1>
        <p>Enter a transcript of your sales call below to get real-time guidance and analysis.</p>
        
        <form action="/analyze" method="post">
            <textarea name="conversation" placeholder="Paste your conversation transcript here..."></textarea>
            <button type="submit">Analyze Conversation</button>
        </form>
        
        {% if results %}
        <div class="result">
            <div class="tab">
                <button class="tablink" onclick="openTab(event, 'analysis')">Analysis</button>
                <button class="tablink" onclick="openTab(event, 'recommendations')">Recommendations</button>
                <button class="tablink" onclick="openTab(event, 'documentation')">Documentation</button>
            </div>
            
            <div id="analysis" class="tabcontent">
                <h3>Analysis</h3>
                <p>{{ results.analysis }}</p>
            </div>
            
            <div id="recommendations" class="tabcontent">
                <h3>Recommendations</h3>
                <p>{{ results.recommendations }}</p>
            </div>
            
            <div id="documentation" class="tabcontent">
                <h3>Documentation</h3>
                <p>{{ results.documentation }}</p>
            </div>
        </div>
        
        <script>
            // Show the Analysis tab by default
            document.getElementById('analysis').style.display = 'block';
            document.getElementsByClassName('tablink')[0].className += " active";
            
            function openTab(evt, tabName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }
                tablinks = document.getElementsByClassName("tablink");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }
        </script>
        {% endif %}
    </body>
    </html>
    """)

# Set up templates
templates = Jinja2Templates(directory="templates")

# Initialize agents
agents = {
    "transcription": TranscriptionAgent(),
    "analysis": AnalysisAgent(),
    "recommendation": RecommendationAgent(),
    "documentation": DocumentationAgent()
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_conversation(request: Request, conversation: str = Form(...)):
    # Process the conversation through the agent pipeline
    results = {}
    
    # Step 1: Clean and structure the transcription
    results["transcription"] = agents["transcription"].process(conversation)
    
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
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "results": results}
    )

def start():
    """Start the web server."""
    uvicorn.run("src.web_app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()