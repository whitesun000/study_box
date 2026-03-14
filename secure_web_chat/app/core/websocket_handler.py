import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.config import settings
from typing import List
from app.ai.detector import detector

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

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    user = websocket.cookies.get(settings.SESSION_COOKIE_NAME)
    if not user:
        user = "Guest"

    try:
        while True:
            # JSON形式でデータを受信
            data = await websocket.receive_json()
            msg_type = data.get("type")

            # 1. 通常のチャット送信処理
            if msg_type == "chat":
                raw_text = data.get("message", "")

                # AIでメッセージをスキャン
                analysis = detector.analyze_message(raw_text, user)

                # 全員にチャットデータを送信
                await manager.broadcast({
                    "type": "chat",
                    "user": user,
                    "message": raw_text
                })

                # AIが異常検知した場合、警告を送信
                if analysis:
                    await manager.broadcast({
                        "type": "ai_alert",
                        "level": analysis["level"],
                        "message": analysis["alert"]
                    })

            # 2. チャットリセットのリクエスト処理
            elif msg_type == "reset_request":
                # 全員に「画面をクリアせよ」という命令を拡散
                await manager.broadcast({
                    "type": "reset_command"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket Error: {e}")
        manager.disconnect(websocket)