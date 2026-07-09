#!/usr/bin/env python3
"""Point d'entrée : orchestre le pipeline séquentiel du guide d'étude."""
import asyncio
import sys

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


def get_topic_from_user() -> str:
    """Lit le sujet depuis les arguments de la ligne de commande."""
    return " ".join(sys.argv[1:]) or "Python decorators"


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
    topic = get_topic_from_user()
    print(f"Génération du guide d'étude pour : {topic}\n")

    final_markdown = asyncio.run(build_study_guide(topic))
    print(f"\n{final_markdown}")

    report = validate_required_sections(final_markdown)
    if report["valid"]:
        print("Validation : toutes les sections requises sont présentes.")
    else:
        print(f"Validation : sections manquantes -> {report['missing']}")

    result = save_markdown_file(OUTPUT_PATH, final_markdown)
    print(result)


if __name__ == "__main__":
    main()
