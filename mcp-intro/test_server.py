#!/usr/bin/env python3
"""Script de test du serveur MCP (avant connexion a un agent)."""
import asyncio
from fastmcp import Client

# Le client lance le serveur en stdio automatiquement.
client = Client("server/learning_server.py")


async def main():
    """Teste tous les outils et la ressource du serveur MCP."""
    async with client:
        print("=" * 55)
        print("1. LISTE DES OUTILS EXPOSES")
        print("=" * 55)
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool.name}")
            print(f"    {tool.description.splitlines()[0]}")

        print()
        print("=" * 55)
        print("2. LISTE DES RESSOURCES EXPOSEES")
        print("=" * 55)
        resources = await client.list_resources()
        for res in resources:
            print(f"  - {res.uri}")

        print()
        print("=" * 55)
        print("3. TEST search_topics (requete valide : 'decorator')")
        print("=" * 55)
        result = await client.call_tool("search_topics", {"query": "decorator"})
        print(result.content[0].text)

        print()
        print("=" * 55)
        print("4. TEST get_topic_details (id valide)")
        print("=" * 55)
        result = await client.call_tool(
            "get_topic_details", {"topic_id": "python-decorators"}
        )
        print(result.content[0].text)

        print()
        print("=" * 55)
        print("5. TEST ENTREE INVALIDE (id inconnu : 'java-lambdas')")
        print("=" * 55)
        result = await client.call_tool(
            "get_topic_details", {"topic_id": "java-lambdas"}
        )
        print(result.content[0].text)

        print()
        print("=" * 55)
        print("6. TEST RESSOURCE topics://catalog")
        print("=" * 55)
        content = await client.read_resource("topics://catalog")
        print(content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
