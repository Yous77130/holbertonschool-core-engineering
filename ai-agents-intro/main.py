#!/usr/bin/env python3
"""Point d'entrée : génère un guide d'étude Markdown pour un sujet donné."""
import asyncio
import sys

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.explainer_agent import create_explainer_agent
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


async def generate_study_guide(topic: str) -> str:
    explainer_agent = create_explainer_agent()
    return await run_agent(explainer_agent, topic)


def main():
    topic = " ".join(sys.argv[1:]) or "Python decorators"

    print(f"Génération du guide d'étude pour : {topic}\n")
    markdown = asyncio.run(generate_study_guide(topic))
    print(markdown)

    result = save_markdown_file(OUTPUT_PATH, markdown)
    print(f"\n{result}")

    report = validate_required_sections(markdown)
    if report["valid"]:
        print("Validation : toutes les sections requises sont présentes.")
    else:
        print(f"Validation : sections manquantes -> {report['missing']}")


if __name__ == "__main__":
    main()
