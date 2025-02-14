from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse
from services.ai import get_ai_response
from services.quotes import get_random_quote

router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_input = request.query.lower()

    # Handling predefined queries
    team_keywords = ["who made you?", "who are the team members?", "who created you?", "tell me about your team?"]
    if any(keyword in user_input for keyword in team_keywords):
        return ChatResponse(response="I was created by a team called Bold Nexus. The team members are Devapriyan, Bhaarath, Aadheesh, Kelda, Nandhitha, and Subavarshini.")

    # Generate AI response
    response = get_ai_response(user_input)
    
    # Add a motivational quote if relevant
    if "advice" in user_input or "motivation" in user_input:
        response += f"\n\nHere's a motivational quote for you: \"{get_random_quote()}\""

    return ChatResponse(response=response)
