from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def create_explainer_agent():
    """
    Crée et configure l'Explainer Agent avec Google ADK et LiteLLM.
    """
    # Instructions strictes pour guider le modèle local
    instructions = (
        "Tu es un professeur d'informatique expert. Explique le sujet donné de manière claire "
        "et accessible pour des étudiants débutants.\n\n"
        "Tu dois obligatoirement structurer ta réponse en Markdown avec ces trois sections :\n"
        "1. # [Nom du sujet]\n"
        "2. ## Explication Simple\n"
        "3. ## Concepts Clés (sous forme de liste à puces)\n"
        "4. ## Exemple Simple"
    )
    
    # Configuration du modèle local via l'ADK (utilise le nom exact de ton modèle Ollama)
    model_setup = LiteLlm(model="ollama_chat/llama3")
    
    # Instanciation de l'agent selon les specs de l'ADK
    explainer_agent = Agent(
        name="explainer_agent",
        model=model_setup,
        instruction=instructions
    )
    
    return explainer_agent