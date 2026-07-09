#!/usr/bin/env python3
"""Outil de validation : vérifie la présence des sections requises."""

REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def validate_required_sections(markdown: str) -> dict:
    """Vérifie que chaque section requise apparaît dans le Markdown.

    Args:
        markdown: le contenu Markdown du guide d'étude à valider.

    Returns:
        Un dictionnaire avec:
        - 'valid': True si toutes les sections sont présentes, sinon False.
        - 'missing': la liste des sections manquantes (vide si tout est là).
    """
    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in markdown:
            missing.append(section)
    return {
        "valid": len(missing) == 0,
        "missing": missing,
    }
