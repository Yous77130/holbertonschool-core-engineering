#!/usr/bin/env python3
"""Client WebSocket : envoie un message à un serveur et retourne la réponse."""
import asyncio
import os
import websockets


async def connect_and_send(uri, message):
    """Se connecte à uri, envoie message, retourne la réponse du serveur."""
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response


if __name__ == "__main__":
    server_uri = os.environ.get("WS_URI", "ws://localhost:8765")
    result = asyncio.run(connect_and_send(server_uri, "demo"))
    print(result, end="")
