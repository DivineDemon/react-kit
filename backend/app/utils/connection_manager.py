from typing import Dict

from fastapi import WebSocket


class ConnectionManager:

  def __init__(self):
    self.active_connections: Dict[int, WebSocket] = {}

  async def connect(self, user_id: int, websocket: WebSocket):
    await websocket.accept()
    self.active_connections[user_id] = websocket

  def disconnect(self, user_id: int):
    if user_id in self.active_connections:
      del self.active_connections[user_id]

  async def send_message(self, user_id: int, message: dict):
    websocket = self.active_connections.get(user_id)
    if websocket:
      await websocket.send_json(message)

  async def broadcast(self, message: dict, exclude: list[int] = []):
    for user_id, websocket in self.active_connections.items():
      if user_id not in exclude:
        await websocket.send_json(message)
