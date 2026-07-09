#!/usr/bin/env python3
"""Outil d'écriture de fichiers Markdown (indépendant du framework d'agent)."""
from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """Écrit du contenu Markdown sur le disque et retourne un message utile.

    Args:
        file_path: chemin du fichier à créer (ex: 'output/resume.md').
        content: le contenu Markdown à écrire.

    Returns:
        Un message de succès avec le chemin, ou un message d'erreur clair.
    """
    try:
        path = Path(file_path)
        # S'assure que le dossier parent existe (le crée si besoin).
        path.parent.mkdir(parents=True, exist_ok=True)
        # Écrit le contenu Markdown dans le fichier.
        path.write_text(content, encoding="utf-8")
        # Retourne un message utile.
        return f"Fichier sauvegardé avec succès : {path}"
    except OSError as error:
        return f"Erreur lors de l'écriture du fichier : {error}"
