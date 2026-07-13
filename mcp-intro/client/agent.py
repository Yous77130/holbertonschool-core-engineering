#!/usr/bin/env python3
"""Agent-like client : consomme le serveur MCP pour repondre a un etudiant.

L'agent n'importe JAMAIS les fonctions du serveur directement.
Il passe par un client MCP, comme une capacite externe.
"""
import asyncio
import json
import sys
from pathlib import Path
from fastmcp import Client

# Chemins relatifs a la racine du projet.
ROOT = Path(__file__).parent.parent
SERVER = ROOT / "server" / "learning_server.py"
OUTPUT = ROOT / "output" / "sample_agent_response.md"


def build_answer(question: str, details: dict) -> str:
    """Formate une reponse Markdown a partir des donnees MCP.

    Args:
        question: la question posee par l'etudiant.
        details: le sujet complet renvoye par get_topic_details.

    Returns:
        Une reponse Markdown prete a afficher.
    """
    lines = []
    lines.append(f"# Reponse a : {question}\n")
    lines.append(f"## Sujet recommande : {details['title']}\n")
    lines.append("### Pourquoi ce sujet est pertinent\n")
    lines.append(f"{details['summary']}\n")

    lines.append("### A reviser en premier (prerequis)\n")
    for item in details["prerequisites"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### Concepts cles\n")
    for item in details["key_concepts"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### Erreurs frequentes a eviter\n")
    for item in details["common_mistakes"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### Idee d'exercice\n")
    lines.append(f"{details['practice_idea']}\n")

    lines.append("---")
    lines.append("*Donnees fournies par le serveur MCP "
                 "`Programming Learning Server`.*")
    return "\n".join(lines)


async def run_agent(question: str) -> str:
    """Interroge le serveur MCP et construit la reponse pour l'etudiant.

    Args:
        question: la question de l'etudiant.

    Returns:
        La reponse Markdown generee a partir des donnees MCP.
    """
    client = Client(str(SERVER))

    async with client:
        # ETAPE 1 : chercher un sujet correspondant VIA MCP.
        search_result = await client.call_tool(
            "search_topics", {"query": question}
        )
        matches = json.loads(search_result.content[0].text)

        # Aucun resultat : on tente avec des mots-cles de la question.
        if not matches:
            for word in question.lower().split():
                if len(word) < 4:
                    continue
                retry = await client.call_tool(
                    "search_topics", {"query": word}
                )
                found = json.loads(retry.content[0].text)
                if found:
                    matches = found
                    break

        if not matches:
            return (f"# Reponse a : {question}\n\n"
                    "Aucun sujet correspondant n'a ete trouve dans le "
                    "catalogue du serveur MCP.\n\n"
                    "Consultez la ressource `topics://catalog` pour voir "
                    "les sujets disponibles.\n")

        # ETAPE 2 : recuperer les details du meilleur sujet VIA MCP.
        best_id = matches[0]["id"]
        details_result = await client.call_tool(
            "get_topic_details", {"topic_id": best_id}
        )
        details = json.loads(details_result.content[0].text)

        if "error" in details:
            return f"# Erreur\n\n{details['error']}\n"

        # ETAPE 3 : formater la reponse a partir des donnees MCP.
        return build_answer(question, details)


def main():
    """Point d'entree : prend la question en argument ou utilise l'exemple."""
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "I want to study Python decorators. What should I review first?"

    answer = asyncio.run(run_agent(question))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(answer, encoding="utf-8")

    print(answer)
    print(f"\n[Reponse sauvegardee dans {OUTPUT}]")


if __name__ == "__main__":
    main()
