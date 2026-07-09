import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def create_practice_designer_agent():
    """
    Crée et configure le Practice Designer Agent avec Google ADK et LiteLLM.
    """
    # Instructions strictes : cet agent crée un exercice, il ne réexplique pas le sujet.
    instructions = (
        "Tu es un concepteur d'exercices pratiques pour étudiants débutants. Tu reçois un "
        "sujet et l'explication déjà rédigée par un autre agent, fournie comme contexte.\n\n"
        "Tu ne dois JAMAIS réécrire ou résumer l'explication reçue. Ton seul rôle est de créer "
        "un exercice pratique basé dessus.\n\n"
        "L'exercice doit être petit et concret, réalisable par un débutant en 10 à 20 minutes. "
        "Évite les exercices qui nécessitent une application complète ou des services externes.\n\n"
        "Tu dois obligatoirement structurer ta réponse en Markdown avec exactement ce titre de "
        "section et ces sous-titres, dans cet ordre (le contenu peut rester en français) :\n"
        "1. ## Practice Exercise\n"
        "2. ### Expected Input (si applicable)\n"
        "3. ### Expected Output (si applicable)\n"
        "4. ### Hints (un ou deux indices, pas la solution)"
    )

    # Configuration du modèle local via l'ADK (nom exact défini dans MODEL_NAME, cf. .env.example)
    model_setup = LiteLlm(model=os.environ.get("MODEL_NAME", "ollama_chat/llama3"))

    # Instanciation de l'agent selon les specs de l'ADK
    practice_designer_agent = Agent(
        name="practice_designer_agent",
        model=model_setup,
        instruction=instructions
    )

    return practice_designer_agent
