from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from typing import List

app=FastAPI()

class ConnectionManager:#it will connect manage all connected users
    def __init__(self):
        #Empty list for storing all connected users
        self.active_connections:List[WebSocket]=[] 
    

    async def connect(self,websocket:WebSocket):
        #to accept client connection
        await websocket.accept()
        #connected users are appending to list
        self.active_connections.append(websocket)

    def disconnect(self,websocket:WebSocket):
        #when user disconnects ,we should remove that user from the list
        self.active_connections.remove(websocket)

    async def broadcast(self,message:str):
        #to send msg to all connected users
        for connection in self.active_connections:
            await connection.send_text(message)
manager=ConnectionManager() #created a obj instance 


@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    #manager will handle when client connects 
    await manager.connect(websocket)
    try:
        #infinitee loop until user connected
        while True:
            #to recieve client msg
            data =await websocket.receive_text()
            await manager.broadcast(data)

    except WebSocketDisconnect:
        #when users  disconnects ,should inform all remainig connected users
        manager.disconnect(websocket)
        await manager.broadcast("A user left the chat")



