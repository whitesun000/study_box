from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.config import settings
from typing import List

# Routerの作成
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    user = websocket.cookies.get(settings.SESSION_COOKIE_NAME)
    if not user:
        user = "Guest"

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)