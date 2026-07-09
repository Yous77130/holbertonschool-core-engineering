#!/usr/bin/env python3
"""Point d'entrée : orchestre le pipeline séquentiel du guide d'étude."""
import asyncio
import os
import sys

import requests
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.explainer_agent import create_explainer_agent
from agents.practice_designer_agent import create_practice_designer_agent
from agents.reviewer_agent import create_reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

load_dotenv()

APP_NAME = "study_guide_app"
OUTPUT_PATH = "output/study_guide.md"
REQUIRED_ENV_VARS = ("OLLAMA_API_BASE", "MODEL_NAME")


def check_environment() -> tuple[str, str]:
    """Vérifie que les variables d'environnement requises sont définies."""
    missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(
            f"Variable(s) d'environnement manquante(s) : {', '.join(missing)}. "
            "Copie .env.example vers .env et renseigne les valeurs avant de relancer le projet."
        )
    return os.environ["OLLAMA_API_BASE"], os.environ["MODEL_NAME"]


def check_ollama_ready(api_base: str, model_name: str) -> None:
    """Vérifie qu'Ollama répond et que le modèle demandé est bien disponible."""
    try:
        response = requests.get(f"{api_base}/api/tags", timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise ConnectionError(
            f"Impossible de joindre Ollama sur {api_base}. "
            "Est-il lancé ? Démarre-le avec `ollama serve`."
        ) from error

    ollama_model = model_name.split("/", 1)[-1]
    available = {entry["name"].split(":")[0] for entry in response.json().get("models", [])}
    if ollama_model not in available:
        raise LookupError(
            f"Le modèle '{ollama_model}' n'est pas disponible dans Ollama. "
            f"Récupère-le avec `ollama pull {ollama_model}`."
        )


def get_topic_from_user() -> str:
    """Lit le sujet depuis les arguments de la ligne de commande."""
    if len(sys.argv) == 1:
        return "Python decorators"

    topic = " ".join(sys.argv[1:]).strip()
    if not topic:
        raise ValueError("Le sujet ne peut pas être vide. Usage : python main.py <sujet>")
    return topic


async def run_agent(agent, prompt: str) -> str:
    """Envoie un prompt à un agent ADK et retourne sa réponse finale en texte."""
    runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME, user_id="cli_user"
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id="cli_user", session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text or final_text
    return final_text


async def run_explainer_agent(topic: str) -> str:
    agent = create_explainer_agent()
    return await run_agent(agent, topic)


async def run_practice_designer_agent(topic: str, explanation: str) -> str:
    agent = create_practice_designer_agent()
    prompt = f"Topic: {topic}\n\nExplanation already written:\n{explanation}"
    return await run_agent(agent, prompt)


def assemble_markdown(explanation: str, practice: str) -> str:
    """Assemble le brouillon (explication + exercice) avant la relecture."""
    return f"{explanation.strip()}\n\n{practice.strip()}\n"


async def run_reviewer_agent(draft: str) -> str:
    agent = create_reviewer_agent()
    return await run_agent(agent, draft)


def assemble_final_markdown(draft: str, review: str) -> str:
    """Assemble le guide final : brouillon + relecture (avec le résumé final)."""
    return f"{draft.strip()}\n\n{review.strip()}\n"


async def build_study_guide(topic: str) -> str:
    print(f"[1/4] Explainer Agent : explication de « {topic} »...")
    explanation = await run_explainer_agent(topic)

    print("[2/4] Practice Designer Agent : création de l'exercice...")
    practice = await run_practice_designer_agent(topic, explanation)

    draft = assemble_markdown(explanation, practice)

    print("[3/4] Reviewer Agent : relecture du brouillon...")
    review = await run_reviewer_agent(draft)

    print("[4/4] Assemblage du Markdown final...")
    return assemble_final_markdown(draft, review)


def main():
    try:
        api_base, model_name = check_environment()
        check_ollama_ready(api_base, model_name)
        topic = get_topic_from_user()
    except (EnvironmentError, ConnectionError, LookupError, ValueError) as error:
        print(f"Erreur de configuration : {error}")
        sys.exit(1)

    print(f"Génération du guide d'étude pour : {topic}\n")
    final_markdown = asyncio.run(build_study_guide(topic))
    print(f"\n{final_markdown}")

    report = validate_required_sections(final_markdown)
    if report["valid"]:
        print("Validation : toutes les sections requises sont présentes.")
    else:
        print(
            f"Validation : sections manquantes -> {report['missing']} "
            "(le guide est tout de même sauvegardé)."
        )

    result = save_markdown_file(OUTPUT_PATH, final_markdown)
    print(result)


if __name__ == "__main__":
    main()
