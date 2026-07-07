#!/usr/bin/env python3
"""Serveur WebSocket avec validation : rejette les messages vides."""
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed


async def connection_handler(websocket):
    """Valide chaque message : OK:<msg> si valide, ERR:EMPTY si vide."""
    try:
        async for message in websocket:
            if message.strip() == "":
                await websocket.send("ERR:EMPTY")
            else:
                await websocket.send("OK:" + message)
    except ConnectionClosed:
        pass


async def main():
    """Démarre le serveur sur localhost:8765 et le maintient ouvert."""
    async with websockets.serve(connection_handler, "localhost", 8765):
        await asyncio.Future()  # tourne indéfiniment


if __name__ == "__main__":
    asyncio.run(main())
