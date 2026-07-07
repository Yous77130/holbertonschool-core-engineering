#!/usr/bin/env python3
"""Client WebSocket : envoie un message à l'echo server et affiche la réponse."""
import asyncio
import websockets


async def connect_and_send():
    """Se connecte, envoie un message, affiche la réponse, puis se ferme."""
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello WebSocket")
        response = await websocket.recv()
        print(response)


if __name__ == "__main__":
    asyncio.run(connect_and_send())
