# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from services.ai import get_ai_response
# import json

# router = APIRouter()

# # Store active connections
# active_connections = []

# @router.websocket("/ws/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.append(websocket)
    
#     try:
#         while True:
#             data = await websocket.receive_text()
#             user_message = json.loads(data).get("message")

#             # Generate AI response
#             ai_response = await get_ai_response(user_message)

#             # Send response back to frontend
#             await websocket.send_text(json.dumps({"response": ai_response}))
    
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)


from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.ai import get_ai_response
import json

router = APIRouter()

# Store active connections as a set to prevent duplicates
active_connections = set()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                user_message = json.loads(data).get("message", "")
                
                if not user_message:
                    await websocket.send_text(json.dumps({"error": "Empty message received"}))
                    continue

                # Generate AI response
                ai_response = await get_ai_response(user_message)

                # Send response back to frontend
                await websocket.send_text(json.dumps({"response": ai_response}))
            
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))

    except WebSocketDisconnect:
        active_connections.discard(websocket)  # Safe removal
    except Exception as e:
        await websocket.send_text(json.dumps({"error": f"Unexpected error: {str(e)}"}))
        active_connections.discard(websocket)
