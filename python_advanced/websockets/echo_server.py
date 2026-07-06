#!/usr/bin/env python3
"""Serveur WebSocket minimal : renvoie (echo) chaque message reçu."""
import asyncio
import websockets


async def echo(websocket):
    """Gère une connexion : renvoie chaque message tel quel."""
    async for message in websocket:
        await websocket.send(message)


async def main():
    """Démarre le serveur sur localhost:8765 et le maintient ouvert."""
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # tourne indéfiniment


if __name__ == "__main__":
    asyncio.run(main())
