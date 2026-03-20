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
        self.user_map = {}
        self.total_blocked_attacks = 0

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_map[websocket] = user
        await self.broadcast_status()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            if websocket in self.user_map:
                del self.user_map[websocket]

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast_status(self):
        """ 現在の接続数とブロック数を全員に配信 """
        await self.broadcast({
            "type": "infra_status",
            "connections": len(self.active_connections),
            "blocked": self.total_blocked_attacks,
            "user_list": list(self.user_map.values())
        })

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user = websocket.cookies.get(settings.SESSION_COOKIE_NAME)
    if not user:
        user = "Guest"

    await manager.connect(websocket, user)

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

                # --- 🛡️ 防御ロジックの追加 ---
                if analysis and analysis["level"] == "CRITICAL":
                    manager.total_blocked_attacks += 1
                    await manager.broadcast_status()

                    # 攻撃を検知した場合、元のメッセージは配信せず警告のみをブロードキャストする
                    await manager.broadcast({
                        "type": "ai_alert",
                        "level": "CRITICAL",
                        "message": f"[防御発動] {user} による攻撃通信を遮断しました。"
                    })
                    # continue で次のループへ飛ばし、下の通常のチャット配信を通さないようにする
                    continue

                # 全員にチャットデータを送信
                await manager.broadcast({
                    "type": "chat",
                    "user": user,
                    "message": raw_text
                })

                # AIが異常検知した場合、警告を送信
                if analysis and analysis["level"] == "WARNING":
                    await manager.broadcast({
                        "type": "ai_alert",
                        "level": analysis["level"],
                        "message": analysis["alert"]
                    })

            # 2.スクリーンデータの転送処理
            elif msg_type == "screen_data":
                image_data = data.get("image")
                # 画像を送ってきたユーザー名を特定して管理者に転送
                await manager.broadcast({
                    "type": "screen_data",
                    "user": user,
                    "image": image_data
                })

            # 3. チャットリセットのリクエスト処理
            elif msg_type == "reset_request":
                # 全員に「画面をクリアせよ」という命令を拡散
                await manager.broadcast({
                    "type": "reset_command"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_status()
    except Exception as e:
        print(f"WebSocket Error: {e}")
        manager.disconnect(websocket)
        await manager.broadcast_status()