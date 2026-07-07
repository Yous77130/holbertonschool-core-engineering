#!/usr/bin/env python3
"""Serveur WebSocket broadcast : diffuse chaque message à tous les clients."""
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

# Ensemble des connexions actives (partagé entre tous les clients).
connected_clients = set()


async def connection_handler(websocket):
    """Diffuse chaque message reçu (préfixé B:) à tous les clients connectés."""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            for client in connected_clients:
                await client.send("B:" + message)
    except ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)


async def main():
    """Démarre le serveur sur localhost:8765 et le maintient ouvert."""
    async with websockets.serve(connection_handler, "localhost", 8765):
        await asyncio.Future()  # tourne indéfiniment


if __name__ == "__main__":
    asyncio.run(main())
