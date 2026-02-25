from typing import List, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["realtime"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, note_id: str):
        await websocket.accept()
        if note_id not in self.active_connections:
            self.active_connections[note_id] = []
        self.active_connections[note_id].append(websocket)

    def disconnect(self, websocket: WebSocket, note_id: str):
        if note_id in self.active_connections:
            self.active_connections[note_id].remove(websocket)

    async def broadcast(self, message: dict, note_id: str, sender: WebSocket):
        for connection in self.active_connections.get(note_id, []):
            if connection != sender:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/notes/{note_id}")
async def websocket_endpoint(websocket: WebSocket, note_id: str):
    await manager.connect(websocket, note_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data, note_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, note_id)
        await manager.broadcast({"type": "presence", "status": "left"}, note_id, websocket)