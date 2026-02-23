from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

# Store connections role wise
active_connections: Dict[str, Dict[str, WebSocket]] = {
    "student": {},
    "mentor": {},
    "admin": {}
}


@app.get("/")
def home():
    return {"message": "Role Based Chat Server Running"}


@app.websocket("/ws/{role}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, role: str, user_id: str):
    await websocket.accept()

    # Store connection
    active_connections[role][user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            
            # Format: target_role:target_user_id:message
            target_role, target_user, message = data.split(":", 2)

            # Send message if target exists
            
            if target_user in active_connections.get(target_role, {}):
                target_ws = active_connections[target_role][target_user]
                await target_ws.send_text(f"{user_id} ({role}): {message}")
                await websocket.send_text(f"You to {target_user}: {message}")
            else:
                await websocket.send_text("User not connected ")

            # Admin monitoring
            for admin_ws in active_connections["admin"].values():
                await admin_ws.send_text(
                   f"[MONITOR] {role}({user_id}) -> {target_role}({target_user}): {message}")
            print(f"{role}:{user_id} -> {target_role}:{target_user} = {message}")
    
    except WebSocketDisconnect:
        #if user gets disconected twice means del will give Key Error,so we can use POP instead of del
        #del active_connections[role][user_id]
        active_connections[role].pop(user_id, None)
        print(f"{user_id} disconnected")