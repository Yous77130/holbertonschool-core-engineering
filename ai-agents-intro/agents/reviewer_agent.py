from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def create_reviewer_agent():
    """
    Crée et configure le Reviewer Agent avec Google ADK et LiteLLM.
    """
    # Instructions strictes : ce rôle inspecte le brouillon, il ne le réécrit pas.
    instructions = (
        "Tu es un relecteur d'informatique critique mais constructif. Tu reçois le brouillon "
        "d'un guide d'étude (Markdown) et tu dois l'évaluer pour sa clarté, sa complétude et "
        "son utilité pour un étudiant débutant.\n\n"
        "Tu ne dois JAMAIS réécrire le guide ou régénérer l'explication, les concepts, "
        "l'exemple ou l'exercice. Ton rôle est uniquement de commenter le brouillon fourni.\n\n"
        "Sois spécifique : évite les remarques vagues comme 'améliore l'explication'. "
        "Préfère des remarques concrètes comme 'l'exemple ne montre pas l'appel de la fonction'.\n\n"
        "Tu dois obligatoirement structurer ta réponse en Markdown avec exactement ce titre "
        "de section et ces sous-titres, dans cet ordre (le contenu peut rester en français) :\n"
        "1. ## Review Comments\n"
        "2. ### Missing Information (informations manquantes ou absentes du brouillon)\n"
        "3. ### Unclear Explanations (passages ambigus ou peu clairs)\n"
        "4. ### Suggestions for Improvement (recommandations courtes et actionnables)\n"
        "5. ### Recommendation (une seule phrase : Approved ou Needs Revision, avec la raison)\n"
        "6. ## Final Summary (un court paragraphe de 2 à 3 phrases résumant le sujet traité et "
        "l'état général du guide, comme conclusion de ta relecture)"
    )

    # Configuration du modèle local via l'ADK (utilise le nom exact de ton modèle Ollama)
    model_setup = LiteLlm(model="ollama_chat/llama3")

    # Instanciation de l'agent selon les specs de l'ADK
    reviewer_agent = Agent(
        name="reviewer_agent",
        model=model_setup,
        instruction=instructions
    )

    return reviewer_agent
