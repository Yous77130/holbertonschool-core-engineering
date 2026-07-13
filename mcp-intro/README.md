# MCP Servers in Python

## Description

Ce projet construit un **serveur MCP** avec FastMCP qui expose un petit dataset
local de sujets de programmation, et un **agent** qui s'y connecte pour repondre
aux questions d'un etudiant.

Exemple : un etudiant demande « Je veux etudier les decorateurs Python, par quoi
commencer ? ». L'agent interroge le serveur MCP, recupere les prerequis, les
concepts cles et un exercice, puis redige une reponse claire.

## MCP Architecture Summary

### Ce qu'est MCP

MCP (Model Context Protocol) est une facon standard de brancher une application
IA a des capacites exterieures : outils, donnees, APIs. Sans MCP, il faudrait
coder une connexion sur mesure pour chaque outil. MCP joue le role d'une **prise
standard** : on expose les capacites une seule fois via un serveur, et n'importe
quelle application compatible peut s'y brancher.

### Les trois roles

- **MCP Host** : l'application IA qui pilote l'interaction (ici, notre agent).
  Un hote peut se connecter a plusieurs serveurs : il cree alors **un client par
  serveur**.
- **MCP Client** : l'intermediaire qui gere la connexion vers **un** serveur
  precis. Il transmet les demandes et rapporte les reponses.
- **MCP Server** : le programme qui **expose** des capacites (outils,
  ressources). C'est ce que ce projet construit.

### Tools et Resources

- **Tools (outils)** : des **actions** que l'agent declenche, avec des
  parametres. Un outil *fait* quelque chose (chercher, recuperer des details).
- **Resources (ressources)** : des **donnees en lecture seule**, identifiees par
  une URI. Une ressource se *lit* mais ne modifie rien.

### Pourquoi n'exposer que le necessaire

Chaque outil expose est une porte d'entree. Moins il y a de portes, moins il y a
de risques. Un perimetre restreint rend aussi l'agent plus fiable (il se trompe
moins d'outil) et le code plus simple a maintenir. C'est le **principe du
moindre privilege**.

## Requirements

- Python 3.10 ou superieur
- FastMCP (voir `requirements.txt`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to Run the Server

```bash
source .venv/bin/activate
python3 server/learning_server.py
```

Le serveur demarre en transport **stdio** et reste en ecoute (le terminal ne
rend pas la main : c'est normal). Pour l'arreter : `Ctrl+C`.

**Important** : ne jamais utiliser `print()` dans le code du serveur. La
communication passe par stdio, et un affichage parasite corromprait les messages
du protocole.

## How to Test the Server

Un script de test verifie le serveur **avant** toute connexion a un agent :

```bash
source .venv/bin/activate
python3 test_server.py
```

Il verifie : le demarrage du serveur, la liste des outils et des ressources,
`search_topics` avec une requete valide, `get_topic_details` avec un id valide,
un cas d'entree invalide, et la lecture de la ressource `topics://catalog`.

Le client FastMCP lance lui-meme le serveur en sous-processus stdio : pas besoin
de le demarrer a la main.

## How to Run the Agent

```bash
source .venv/bin/activate
python3 client/agent.py "I want to study Python decorators. What should I review first?"
```

Sans argument, l'agent utilise la question d'exemple par defaut.

L'agent :
1. se connecte au serveur MCP via un client MCP (**jamais** par import direct) ;
2. appelle `search_topics` pour trouver un sujet correspondant ;
3. appelle `get_topic_details` pour obtenir les informations completes ;
4. formate une reponse Markdown pour l'etudiant ;
5. sauvegarde le resultat dans `output/sample_agent_response.md`.

Si aucun sujet ne correspond, l'agent l'indique clairement.

## Available Tools

| Outil | Parametre | Retour |
|---|---|---|
| `search_topics` | `query: str` | Liste des sujets correspondants (id, titre, resume). Liste vide si aucun match. |
| `get_topic_details` | `topic_id: str` | Le sujet complet (prerequis, concepts cles, erreurs frequentes, exercice). En cas d'id inconnu : un message d'erreur + la liste des ids disponibles. |

Ces deux outils suivent le pattern MCP classique : un outil pour **decouvrir**
des candidats, un autre pour **approfondir** un sujet choisi.

## Available Resources

| Ressource (URI) | Contenu |
|---|---|
| `topics://catalog` | Chaine JSON listant les sujets disponibles (id + titre). Lecture seule. |

## Third-Party MCP Server Review

### Serveur analyse : Filesystem MCP Server

Package `@modelcontextprotocol/server-filesystem` (npm), maintenu par l'equipe
officielle Model Context Protocol. Licence MIT.

**Ce qu'il fait** : il permet a une application IA de lire, ecrire, chercher et
gerer des fichiers et dossiers sur la machine, via des commandes en langage
naturel.

**Local ou distant** : **local**. C'est un serveur Node.js execute sur la
machine de l'utilisateur (via `npx` ou Docker). Il n'accede pas au reseau, il ne
touche que le systeme de fichiers local dans les dossiers autorises.

**Outils exposes** :
- En lecture seule : `read_text_file`, `read_media_file`, `read_multiple_files`,
  `list_directory`, `list_directory_with_sizes`, `list_allowed_directories`.
- En ecriture : ecriture, deplacement et modification de fichiers (operations
  potentiellement destructrices).

Le serveur annote chaque outil pour que le client puisse distinguer les outils
en lecture seule de ceux capables d'ecrire, et signaler ceux qui peuvent ecraser
des donnees.

**Permissions requises** : aucune cle API. En revanche, il faut declarer
explicitement les **dossiers autorises** au demarrage :

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "/chemin/vers/mon-projet"]
    }
  }
}
```

Sans dossier autorise, le serveur refuse de demarrer.

**Un risque** : une **portee d'acces trop large**. Une fois un dossier autorise,
le serveur y a un pouvoir complet (lecture, ecriture, suppression). Pointer le
serveur vers son dossier personnel donnerait a l'IA acces a des fichiers
sensibles : cles SSH, fichiers `.env`, documents prives. Les outils d'ecriture
peuvent aussi **ecraser** des fichiers existants.

**Une mesure de securite** : appliquer le **principe du moindre privilege**.
N'autoriser qu'un dossier de projet precis (jamais le dossier personnel ni la
racine), eviter les dossiers systeme, et si l'IA n'a besoin que de lire, monter
le dossier en **lecture seule** (flag `ro` avec Docker). Toujours lire le README
du serveur et verifier qu'il vient bien de la source officielle avant de
l'installer.

## Example Output

Question : *« I want to study Python decorators. What should I review first? »*

Extrait de `output/sample_agent_response.md` :

```markdown
# Reponse a : I want to study Python decorators. What should I review first?

## Sujet recommande : Python Decorators

### Pourquoi ce sujet est pertinent
Un decorateur est une fonction qui enveloppe une autre fonction pour ajouter un
comportement sans modifier son code.

### A reviser en premier (prerequis)
- Fonctions
- Portee des variables
- Fonctions imbriquees

### Concepts cles
- Fonctions d'ordre superieur
- Fonction wrapper
- Syntaxe @decorator
...
```

Cas d'id inconnu (`get_topic_details("java-lambdas")`) :

```json
{"error": "Sujet introuvable : 'java-lambdas'",
 "available_ids": ["python-decorators", "javascript-dom", "websockets",
                   "flask-ssr", "recursion"]}
```

## Known Limitations

- **Recherche basique** : `search_topics` fait une simple correspondance de
  sous-chaine (`in`), sans gestion des synonymes, des fautes de frappe ni du
  pluriel. Une question en langage naturel ne matche pas directement : l'agent
  doit reessayer mot par mot pour trouver un sujet.
- **Dataset minuscule** : 5 sujets seulement, en dur dans un fichier JSON. Aucune
  base de donnees, aucune source externe.
- **Agent deterministe, sans LLM** : l'agent formate la reponse avec du code, il
  ne « raisonne » pas. Il prend simplement le **premier** resultat de recherche,
  sans evaluer lequel est le plus pertinent.
- **Pas de gestion de plusieurs sujets** : si la question porte sur deux sujets,
  seul le premier est traite.
- **Transport stdio uniquement** : le serveur n'a pas ete teste en HTTP.

### Erreur rencontree pendant le developpement

L'agent plantait avec `IndexError: list index out of range` sur
`result.content[0].text`. En inspectant l'objet renvoye par FastMCP
(`type()`, `dir()`), il s'est avere que les donnees se trouvaient dans
**`result.data`**, deja converties en objets Python — sans besoin de
`json.loads()`. Lecon : face a une API inconnue, **inspecter l'objet plutot que
deviner**.

## Reflection

**1. Quel probleme MCP resout-il ?**
Sans MCP, chaque agent devrait avoir une integration sur mesure pour chaque
outil externe (base de donnees, fichiers, API). Cela devient vite ingerable :
N agents x M outils = N x M integrations. MCP standardise la connexion : on
expose une capacite **une fois** via un serveur, et **tout** client compatible
peut l'utiliser. C'est une prise standard au lieu d'un cablage sur mesure.

**2. Quelle difference entre un tool et une resource ?**
Un **tool** est une **action** : il prend des parametres et *fait* quelque chose
(chercher, calculer, recuperer). Une **resource** est une **donnee en lecture
seule**, identifiee par une URI, qu'on se contente de *lire*. Moyen
mnemotechnique : tool = verbe, resource = nom. Cela se voit jusque dans le
client : on **appelle** un outil (`call_tool`), on **lit** une ressource
(`read_resource`).

**3. Qu'expose mon serveur MCP ?**
Deux outils — `search_topics` (chercher des sujets par mot-cle) et
`get_topic_details` (obtenir toutes les infos d'un sujet par son id) — et une
ressource en lecture seule, `topics://catalog` (la liste des sujets
disponibles). Les donnees viennent d'un fichier JSON local, `data/topics.json`.

**4. Comment mon agent utilise-t-il le serveur MCP ?**
Il cree un **client MCP** (`fastmcp.Client`) qui lance le serveur en
sous-processus stdio. Il appelle ensuite `search_topics` pour trouver un sujet,
puis `get_topic_details` sur le meilleur resultat, et formate la reponse avec
les donnees renvoyees. Point crucial : il **n'importe jamais** les fonctions du
serveur directement — il passe par le protocole, comme un vrai client externe.

**5. Que verifier avant d'utiliser un serveur MCP tiers ?**
Trois questions : **que peut-il lire ?** (mes fichiers, ma base, mes mails ?),
**que peut-il modifier ou detruire ?**, et **quelles cles lui donne-t-on ?**
Concretement : lire son README et son code, verifier la source (le nom du
package peut etre imite), examiner la liste des outils exposes (lecture seule ou
ecriture ?), et n'accorder que le **strict minimum** de permissions.

**6. Quelle limite ai-je observee dans mon implementation ?**
La recherche est trop naive. `search_topics` cherche une sous-chaine exacte,
donc une vraie question d'etudiant (« I want to study Python decorators. What
should I review first? ») ne matche **aucun** sujet directement — il a fallu
ajouter un repli qui reessaie mot par mot. Une recherche plus robuste
(normalisation, synonymes, ou un LLM pour extraire l'intention) serait
necessaire pour un usage reel.

## Securite

- Aucun secret, token ou cle API n'est commite.
- `.env` est dans le `.gitignore`.
- `.env.example` documente uniquement les **noms** des variables, jamais les
  vraies valeurs.
