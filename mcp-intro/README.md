# MCP Intro — Programming Learning MCP Server

Serveur MCP (FastMCP) exposant des donnees d'apprentissage de la programmation,
avec un client/agent qui s'y connecte.

## Structure
- `server/` : le serveur MCP (outils + ressources)
- `client/` : le client et l'agent qui consomment le serveur
- `data/` : le dataset local (topics.json)
- `output/` : les reponses generees

## Statut
En construction.

## MCP Architecture Summary

### Ce qu'est MCP

MCP (Model Context Protocol) est une facon standard de brancher une application
IA a des capacites exterieures : des outils, des donnees, des fichiers, des APIs.

Sans MCP, il faudrait coder une connexion sur mesure pour chaque outil, ce qui
devient vite ingerable. MCP joue le role d'une **prise standard** : on expose
les capacites une seule fois via un serveur, et n'importe quelle application
compatible peut s'y brancher.

### Les trois roles

**MCP Host** — c'est l'application IA qui pilote l'ensemble de l'interaction
(par exemple un agent qui repond a un etudiant). C'est elle qui a un besoin.
Un hote peut se connecter a plusieurs serveurs a la fois : dans ce cas, il cree
**un client MCP par serveur**.

**MCP Client** — c'est l'intermediaire qui gere la connexion vers **un** serveur
precis. Il transmet les demandes de l'hote au serveur et rapporte les reponses.
Un client = un serveur.

**MCP Server** — c'est le programme qui **expose** des capacites : des outils,
des ressources, des prompts. Dans ce projet, c'est notre serveur qui expose des
donnees sur des sujets de programmation.

### Tools et Resources : la difference

**Tools (outils)** — ce sont des **actions** que l'agent peut declencher. Un
outil *fait* quelque chose : chercher un sujet, recuperer les details d'un
sujet, suggerer un exercice. C'est comme un verbe.

**Resources (ressources)** — ce sont des **donnees en lecture seule** que
l'agent peut consulter. Une ressource se *lit* mais ne modifie rien : par
exemple le catalogue complet des sujets disponibles. C'est comme un nom.

### Exemple concret

Un etudiant demande : « Je veux etudier les decorateurs Python, par quoi
commencer ? »

1. L'**hote** (l'agent) recoit la question.
2. Il passe par son **client** MCP pour interroger notre **serveur**.
3. Le serveur repond via un **tool** (`get_topic_details`) qui retourne les
   prerequis et les concepts cles du sujet.
4. L'agent utilise cette information pour rediger une reponse claire a
   l'etudiant.

### Pourquoi n'exposer que le strict necessaire

Un serveur MCP ne devrait exposer **que les capacites dont il a vraiment
besoin**, pour trois raisons :

- **Securite** : chaque outil expose est une porte d'entree. Moins il y a de
  portes, moins il y a de risques d'abus ou d'acces non voulu.
- **Clarte** : un agent qui a le choix entre 3 outils bien definis se trompe
  moins qu'un agent noye sous 30 outils vagues.
- **Maintenance** : moins de surface exposee, c'est moins de code a tester,
  documenter et corriger.

C'est le principe du **moindre privilege** : ne donner que ce qui est
strictement necessaire, rien de plus.

## Lancer le serveur

```bash
source .venv/bin/activate
python3 server/learning_server.py
```

Le serveur demarre et reste en ecoute (le terminal ne rend pas la main : c'est
normal). Pour l'arreter : `Ctrl+C`.

**Attention** : le serveur communique via stdio. Ne jamais utiliser `print()`
dans le code du serveur, cela corromprait les messages du protocole.

## Tester le serveur

Un script de test verifie le serveur avant toute connexion a un agent :

```bash
source .venv/bin/activate
python3 test_server.py
```

Il verifie : le demarrage du serveur, la liste des outils et ressources,
`search_topics` avec une requete valide, `get_topic_details` avec un id valide,
un cas d'entree invalide, et la lecture de la ressource `topics://catalog`.

### Exemple de sortie

Recherche `search_topics("decorator")` :
```json
[{"id": "python-decorators", "title": "Python Decorators",
  "summary": "Un decorateur est une fonction qui enveloppe une autre fonction..."}]
```

Id inconnu `get_topic_details("java-lambdas")` :
```json
{"error": "Sujet introuvable : 'java-lambdas'",
 "available_ids": ["python-decorators", "javascript-dom", "websockets",
                   "flask-ssr", "recursion"]}
```

## Lancer l'agent

```bash
source .venv/bin/activate
python3 client/agent.py "I want to study Python decorators. What should I review first?"
```

L'agent :
1. se connecte au serveur MCP via un client MCP (jamais par import direct) ;
2. appelle `search_topics` pour trouver un sujet correspondant ;
3. appelle `get_topic_details` pour obtenir les informations completes ;
4. formate une reponse Markdown a destination de l'etudiant ;
5. sauvegarde le resultat dans `output/sample_agent_response.md`.

Si aucun sujet ne correspond, l'agent l'indique clairement.

## Revue d'un serveur MCP tiers

### Serveur analyse : Filesystem MCP Server

Package : `@modelcontextprotocol/server-filesystem` (npm), maintenu par
l'equipe officielle Model Context Protocol. Licence MIT.

### 1. Ce que fait le serveur

Il permet a une application IA de lire, ecrire, chercher et gerer des fichiers
et des dossiers sur la machine locale, via des commandes en langage naturel.
C'est l'implementation de reference pour l'acces au systeme de fichiers en MCP.

### 2. Local ou distant ?

**Local.** C'est un serveur Node.js qui s'execute sur la machine de
l'utilisateur, lance via `npx` (ou Docker). Il n'accede pas au reseau : il ne
touche que le systeme de fichiers local, dans les dossiers autorises.

### 3. Outils et ressources exposes

Il expose plusieurs outils, separes en deux categories :

**Lecture seule** (`readOnlyHint: true`) :
- `read_text_file` — lire un fichier texte
- `read_media_file` — lire une image ou un fichier audio
- `read_multiple_files` — lire plusieurs fichiers
- `list_directory` — lister le contenu d'un dossier
- `list_directory_with_sizes` — lister avec les tailles
- `list_allowed_directories` — voir quels dossiers sont autorises

**Ecriture** (potentiellement destructifs) :
- ecriture, deplacement et modification de fichiers dans les dossiers autorises

Le serveur annote chaque outil pour que le client puisse distinguer les outils
en lecture seule des outils capables d'ecrire, et signaler ceux qui peuvent
etre destructeurs (ecrasement de donnees).

### 4. Permissions et identifiants requis

**Aucune cle API ni identifiant.** En revanche, il faut declarer explicitement
les **dossiers autorises** au demarrage, en argument de la commande :

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

Sans dossier autorise declare, le serveur refuse de demarrer.

### 5. Un risque identifie

**Le risque principal : une portee d'acces trop large.** Une fois qu'un dossier
est autorise, le serveur a un pouvoir **complet** dedans : lecture, ecriture,
suppression. Si on pointe le serveur vers son dossier personnel (ou pire, vers
la racine du disque), l'IA obtient un acces total a des fichiers sensibles :
cles SSH, fichiers `.env`, documents prives, code source entier.

Un autre danger : les outils d'ecriture peuvent **ecraser** des fichiers
existants. Une mauvaise instruction, une hallucination du modele, ou une
injection de prompt dans un fichier lu pourraient entrainer une perte de
donnees.

### 6. Une mesure de securite a appliquer

**Appliquer le principe du moindre privilege : n'autoriser QUE le dossier
strictement necessaire, jamais le dossier personnel ni la racine.**

Concretement :
- pointer le serveur vers un seul dossier de projet (ex :
  `/home/user/projets/mon-projet`), pas vers `/home/user`
- eviter les dossiers systeme (`/etc`, `C:\Windows`, `/System`)
- si l'IA n'a besoin que de lire, monter le dossier en **lecture seule**
  (via Docker, avec le flag `ro`), pour supprimer tout risque d'ecriture
- relire regulierement la liste des dossiers autorises
- lire le README du serveur **avant** de l'installer, et verifier qu'il provient
  bien de la source officielle (le nom du package peut etre imite)

### Ce que cette revue m'apprend

Un serveur MCP est une **porte d'entree** sur mes systemes. Avant d'en installer
un, je dois toujours me demander : *que peut-il lire ? que peut-il modifier ?
quelles cles lui donne-t-on ?* Et ne lui accorder que le strict minimum.
