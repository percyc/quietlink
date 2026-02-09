"""
WebRTC 局域网屏幕共享系统 - FastAPI 后端
WebRTC Signaling Server (Signaling Server Only)
"""

import uuid
import random
import string
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional
import uvicorn

app = FastAPI(title="WebRTC Screen Share Server")

# CORS配置，允许所有 origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 静态文件服务
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def generate_room_code(length: int = 6) -> str:
    """生成指定长度的数字房间码"""
    while True:
        code = "".join(random.choices(string.digits, k=length))
        if code not in rooms:
            return code


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.rooms: Dict[str, dict] = {}

    async def create_room(self, websocket: WebSocket) -> str:
        """创建房间，返回房间码"""
        code = generate_room_code(6)
        self.rooms[code] = {
            "host": websocket,
            "clients": {},
            "authorized_clients": set(),
        }
        return code

    def join_room(self, code: str, client_id: str, websocket: WebSocket) -> bool:
        """观众请求加入房间"""
        if code in self.rooms:
            self.rooms[code]["clients"][client_id] = websocket
            return True
        return False

    def authorize_client(self, code: str, client_id: str) -> bool:
        """授权客户端"""
        if code in self.rooms:
            self.rooms[code]["authorized_clients"].add(client_id)
            return True
        return False

    def reject_client(self, code: str, client_id: str) -> bool:
        """拒绝客户端"""
        if code in self.rooms and client_id in self.rooms[code]["clients"]:
            del self.rooms[code]["clients"][client_id]
            return True
        return False

    def is_authorized(self, code: str, client_id: str) -> bool:
        """检查客户端是否已授权"""
        return (
            code in self.rooms and client_id in self.rooms[code]["authorized_clients"]
        )

    def get_host(self, code: str) -> Optional[WebSocket]:
        """获取房间主机连接"""
        return self.rooms[code].get("host") if code in self.rooms else None

    def get_client(self, code: str, client_id: str) -> Optional[WebSocket]:
        """获取指定客户端连接"""
        return (
            self.rooms[code]["clients"].get(client_id) if code in self.rooms else None
        )

    def remove_client(self, code: str, client_id: str):
        """移除客户端"""
        if code in self.rooms:
            self.rooms[code]["clients"].pop(client_id, None)
            self.rooms[code]["authorized_clients"].discard(client_id)

    def close_room(self, code: str):
        """关闭房间"""
        if code in self.rooms:
            for client_id, ws in list(self.rooms[code]["clients"].items()):
                try:
                    ws.close()
                except:
                    pass
            try:
                self.rooms[code]["host"].close()
            except:
                pass
            del self.rooms[code]


manager = ConnectionManager()
rooms: Dict[str, dict] = {}


@app.websocket("/ws/host")
async def websocket_host(websocket: WebSocket):
    """WebSocket 主机端点 - 创建房间"""
    await websocket.accept()
    code = None
    print("[Host] New connection established")

    try:
        code = await manager.create_room(websocket)
        print(f"[Host] Created room: {code}")

        await websocket.send_json({"type": "room_created", "room_code": code})

        while True:
            data = await websocket.receive_json()
            print(f"[Host] Received: {data}")

            if data["type"] == "get_code":
                await websocket.send_json({"type": "room_code", "room_code": code})

            elif data["type"] == "close_room":
                print(f"[Host] Room {code} closed")
                manager.close_room(code)
                break

            elif data["type"] == "join_request":
                await websocket.send_json(
                    {"type": "join_request", "client_id": data["client_id"]}
                )

            elif data["type"] == "join_approve":
                client_id = data["client_id"]
                print(f"[Host] Approving client {client_id} in room {code}")
                manager.authorize_client(code, client_id)
                client_ws = manager.get_client(code, client_id)
                if client_ws:
                    await client_ws.send_json({"type": "join_approved"})
                    print(f"[Host] Sent join_approved to client {client_id}")
                else:
                    print(f"[Host] Client {client_id} not found!")

            elif data["type"] == "join_reject":
                client_id = data["client_id"]
                manager.reject_client(code, client_id)
                client_ws = manager.get_client(code, client_id)
                if client_ws:
                    await client_ws.send_json({"type": "join_rejected"})

            elif data["type"] == "offer":
                client_id = data["client_id"]
                client_ws = manager.get_client(code, client_id)
                if client_ws and manager.is_authorized(code, client_id):
                    await client_ws.send_json({"type": "offer", "sdp": data["sdp"]})

            elif data["type"] == "answer":
                client_id = data["client_id"]
                host_ws = manager.get_host(code)
                if host_ws:
                    await host_ws.send_json(
                        {
                            "type": "answer",
                            "client_id": client_id,
                            "sdp": data["sdp"],
                        }
                    )

            elif data["type"] == "ice_candidate":
                target = data.get("target")
                client_id = data.get("client_id")
                candidate = data["candidate"]
                sdp_mid = data.get("sdpMid")
                sdp_mline_index = data.get("sdpMLineIndex")

                if target == "host":
                    host_ws = manager.get_host(code)
                    if host_ws:
                        await host_ws.send_json(
                            {
                                "type": "ice_candidate",
                                "client_id": client_id,
                                "candidate": candidate,
                                "sdpMid": sdp_mid,
                                "sdpMLineIndex": sdp_mline_index,
                            }
                        )
                elif target == "client":
                    client_ws = manager.get_client(code, client_id)
                    if client_ws:
                        await client_ws.send_json(
                            {
                                "type": "ice_candidate",
                                "candidate": candidate,
                                "sdpMid": sdp_mid,
                                "sdpMLineIndex": sdp_mline_index,
                            }
                        )

    except WebSocketDisconnect:
        print(f"[WebSocket] Host disconnected")
        if code and code in manager.rooms:
            manager.close_room(code)


@app.websocket("/ws/client/{room_code}")
async def websocket_client(websocket: WebSocket, room_code: str):
    """WebSocket 客户端端点 - 加入房间"""
    await websocket.accept()
    client_id = str(uuid.uuid4())[:8]
    code = room_code

    try:
        print(f"[Client] {client_id} trying to join room {code}")
        print(f"[Client] Current rooms: {list(manager.rooms.keys())}")
        if manager.join_room(code, client_id, websocket):
            print(f"[Client] {client_id} joined room {code}")
            print(
                f"[Client] Room {code} clients: {list(manager.rooms[code]['clients'].keys())}"
            )

            # 告诉客户端它的ID
            await websocket.send_json({"type": "client_id", "client_id": client_id})

            host_ws = manager.get_host(code)
            if host_ws:
                print(f"[Client] Notifying host of new client {client_id}")
                await host_ws.send_json(
                    {"type": "join_request", "client_id": client_id}
                )

            while True:
                data = await websocket.receive_json()

                if data["type"] == "join_approved":
                    print(f"[Client] {client_id} approved, starting WebRTC")
                    await websocket.send_json({"type": "ready"})

                elif data["type"] == "join_rejected":
                    print(f"[Client] {client_id} rejected")
                    await websocket.close()
                    break

                elif data["type"] == "offer":
                    await websocket.send_json(
                        {"type": "offer_received", "sdp": data["sdp"]}
                    )

                elif data["type"] == "answer":
                    client_id = data.get("client_id")
                    host_ws = manager.get_host(code)
                    if host_ws and client_id:
                        await host_ws.send_json(
                            {
                                "type": "answer",
                                "client_id": client_id,
                                "sdp": data.get("sdp"),
                                "sdpType": data.get("sdpType"),
                            }
                        )
                        print(f"[Client] Forwarded answer from {client_id} to host")

                elif data["type"] == "ice_candidate":
                    host_ws = manager.get_host(code)
                    if host_ws:
                        await host_ws.send_json(
                            {
                                "type": "ice_candidate",
                                "candidate": data["candidate"],
                                "client_id": client_id,
                                "sdpMid": data.get("sdpMid"),
                                "sdpMLineIndex": data.get("sdpMLineIndex"),
                            }
                        )

                elif data["type"] == "leave":
                    manager.remove_client(code, client_id)
                    break

        else:
            await websocket.send_json({"type": "error", "message": "Room not found"})
            await websocket.close()

    except WebSocketDisconnect:
        print(f"[WebSocket] Client {client_id} disconnected")
        manager.remove_client(code, client_id)


@app.get("/host.html")
async def redirect_to_host():
    from fastapi.responses import RedirectResponse

    return RedirectResponse("/static/host.html")


@app.get("/client.html")
async def redirect_to_client():
    from fastapi.responses import RedirectResponse

    return RedirectResponse("/static/client.html")


@app.get("/")
async def get_index():
    """首页"""
    return HTMLResponse("""
    <html>
    <head>
        <title>WebRTC 屏幕共享</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px 30px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 100%;
                text-align: center;
            }
            h1 {
                color: #333;
                font-size: 28px;
                margin-bottom: 15px;
                font-weight: 700;
            }
            p {
                color: #666;
                font-size: 16px;
                margin-bottom: 30px;
                line-height: 1.5;
            }
            .btn {
                display: block;
                width: 100%;
                padding: 18px 30px;
                margin: 12px 0;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                border: none;
                border-radius: 12px;
                text-decoration: none;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
            .btn:active {
                transform: translateY(0);
            }
            .host {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
            }
            .host:hover {
                background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
            }
            .client {
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
                color: white;
            }
            .client:hover {
                background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
            }
            .icon {
                font-size: 48px;
                margin-bottom: 15px;
                display: block;
            }
            .info {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #999;
                font-size: 14px;
            }
            /* 移动端优化 */
            @media (max-width: 480px) {
                .container {
                    padding: 30px 20px;
                    border-radius: 15px;
                }
                h1 {
                    font-size: 24px;
                }
                p {
                    font-size: 15px;
                }
                .btn {
                    padding: 16px 25px;
                    font-size: 17px;
                }
                .icon {
                    font-size: 40px;
                }
            }
            /* 超小屏幕 */
            @media (max-width: 360px) {
                h1 {
                    font-size: 22px;
                }
                .btn {
                    padding: 14px 20px;
                    font-size: 16px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="icon">🖥️</span>
            <h1>WebRTC 屏幕共享</h1>
            <p>局域网实时屏幕共享系统<br>无需互联网，安全高效</p>
            <a href="/static/host.html" class="btn host">
                📤 我是共享端 (Host)
            </a>
            <a href="/static/client.html" class="btn client">
                📥 我是观看端 (Client)
            </a>
            <div class="info">
                纯内网运行 | 自动打洞 | 实时传输
            </div>
        </div>
    </body>
    </html>
    """)


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    https = len(sys.argv) > 2 and sys.argv[2] == "https"
    protocol = "https" if https else "http"
    print(f"\n🚀 WebRTC Screen Share Server started on {protocol}://localhost:{port}")
    print(f"📱 Host: {protocol}://localhost:{port}/host.html")
    print(f"📺 Client: {protocol}://localhost:{port}/client.html\n")
    if https:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            ssl_certfile="certs/cert.pem",
            ssl_keyfile="certs/key.pem",
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=port)
