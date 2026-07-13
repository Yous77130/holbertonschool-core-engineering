#!/usr/bin/env python3
"""Serveur MCP (FastMCP) pour l'apprentissage de la programmation."""
import json
from pathlib import Path
from fastmcp import FastMCP

# Creation du serveur MCP.
mcp = FastMCP("Programming Learning Server")

# Chemin vers le dataset local (relatif a la racine du projet).
DATA_FILE = Path(__file__).parent.parent / "data" / "topics.json"


def load_topics() -> list:
    """Charge la liste des sujets depuis le fichier JSON local."""
    with open(DATA_FILE, encoding="utf-8") as file:
        data = json.load(file)
    return data.get("topics", [])


@mcp.tool
def search_topics(query: str) -> list[dict]:
    """Recherche des sujets de programmation par titre ou mot-cle.

    Args:
        query: le terme recherche (ex: 'decorator', 'websocket').

    Returns:
        Une liste de sujets correspondants, avec id, titre et resume.
        Une liste vide si aucun sujet ne correspond.
    """
    topics = load_topics()
    search = query.lower().strip()
    results = []

    for topic in topics:
        haystack = topic["title"].lower() + " " + topic["id"].lower()
        haystack += " " + " ".join(topic["key_concepts"]).lower()

        if search in haystack:
            results.append({
                "id": topic["id"],
                "title": topic["title"],
                "summary": topic["summary"],
            })

    return results


@mcp.tool
def get_topic_details(topic_id: str) -> dict:
    """Retourne toutes les informations d'un sujet a partir de son id.

    Args:
        topic_id: l'identifiant exact du sujet (ex: 'python-decorators').

    Returns:
        Le sujet complet (titre, resume, prerequis, concepts cles,
        erreurs frequentes, idee d'exercice).
        Si l'id est inconnu, retourne un dictionnaire avec une cle 'error'
        et la liste des ids disponibles.
    """
    topics = load_topics()
    wanted = topic_id.lower().strip()

    for topic in topics:
        if topic["id"].lower() == wanted:
            return topic

    return {
        "error": f"Sujet introuvable : '{topic_id}'",
        "available_ids": [t["id"] for t in topics],
    }


@mcp.resource("topics://catalog")
def get_topic_catalog() -> str:
    """Retourne le catalogue des sujets disponibles (ids et titres).

    Ressource en LECTURE SEULE : elle expose des donnees, sans rien modifier.
    Permet a un client de parcourir les sujets avant d'en choisir un.

    Returns:
        Une chaine JSON contenant la liste des sujets (id + titre).
    """
    topics = load_topics()
    catalog = [
        {"id": topic["id"], "title": topic["title"]}
        for topic in topics
    ]
    return json.dumps({"topics": catalog}, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
