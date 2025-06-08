# uvicorn api-server:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.agent_gemini import TicketAssistantAgent  # Import AI agent class

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; update with specific domains for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

agent = TicketAssistantAgent()  # Initialize AI agent

@app.post("/review-ticket")
async def review_ticket(request: Request):
    issue = await request.json()
    ticket = agent.review_ticket(issue)
    return {"ticket": ticket}

@app.post("/assign-ticket")
async def assign_ticket(request: Request):
    ticket = await request.json()
    assigned_group = agent.assign_ticket(ticket)
    return {"support_group": assigned_group}