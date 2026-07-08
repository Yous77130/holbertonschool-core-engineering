import os

def save_study_guide(content: str, filename: str = "study_guide.md") -> str:
    """
    Sauvegarde le contenu textuel dans un fichier Markdown dans le dossier output.
    """
    output_dir = "output"
    # S'assurer que le dossier output existe
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return f"Fichier sauvegardé avec succès dans : {file_path}"
