# AI Study Guide Generator

A small multi-agent system that turns a programming topic into a complete
Markdown study guide. Built with [Google ADK](https://google.github.io/adk-docs/),
connected to a local model through [LiteLLM](https://docs.litellm.ai/) and
[Ollama](https://ollama.com/).

## How it works

Three agents run in sequence, each with one responsibility:

```
Topic
  -> Explainer Agent        (Topic, Simple Explanation, Key Concepts, Example, Common Mistakes)
  -> Practice Designer Agent (Practice Exercise, based on the explanation)
  -> [draft assembled]
  -> Reviewer Agent          (Review Comments, Final Summary — reviews, does not rewrite)
  -> [final Markdown assembled]
  -> validate_required_sections()  (deterministic check)
  -> save_markdown_file()          (deterministic write to output/study_guide.md)
```

Two deterministic Python tools support the agents:
- `tools/file_writer.py` — writes the final Markdown to disk.
- `tools/validation.py` — checks that all 8 required sections are present.

## Model provider

This project uses **Ollama** running **llama3** locally, connected through
**LiteLLM**'s `ollama_chat/` provider inside Google ADK's `LiteLlm` model
wrapper. No external API key is required. If you want to use a different
LiteLLM-compatible provider (Gemini, OpenAI, Claude, etc.), change
`MODEL_NAME` in `.env` and adjust the model string accordingly.

## Setup

1. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama** — see [Ollama's install docs](https://ollama.com/download).

4. **Pull a local model**
   ```bash
   ollama pull llama3
   ```

5. **Confirm the model responds** (test Ollama directly before involving ADK)
   ```bash
   ollama run llama3 "Say hello in one sentence."
   ```

6. **Configure your environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if your Ollama host/port or model name differ from the
   defaults:
   ```
   OLLAMA_API_BASE=http://localhost:11434
   MODEL_NAME=ollama_chat/llama3
   ```

## Usage

```bash
python main.py "Python decorators"
python main.py "Python list comprehensions"
python main.py "HTTP status codes"
```

Running with no arguments defaults to `"Python decorators"`. The generated
guide is printed to the console and saved to `output/study_guide.md`.

### Example output (excerpt)

```markdown
# Topic: Python Decorators

## Simple Explanation
...

## Key Concepts
...

## Example
...

## Common Mistakes
...

## Practice Exercise
...

## Review Comments
...

## Final Summary
...
```

## Troubleshooting

The project checks common failure points before running any agent, so
problems are reported clearly instead of surfacing as a raw stack trace.

| Problem | What you'll see | Fix |
|---|---|---|
| `.env` missing or incomplete | `Variable(s) d'environnement manquante(s) : OLLAMA_API_BASE, MODEL_NAME` | Run `cp .env.example .env` and fill in the values. |
| Ollama isn't running | `Impossible de joindre Ollama sur http://localhost:11434. Est-il lancé ?` | Start it with `ollama serve`, or check `OLLAMA_API_BASE` in `.env`. |
| Model not pulled | `Le modèle 'llama3' n'est pas disponible dans Ollama.` | Run `ollama pull llama3` (or whatever `MODEL_NAME` points to). |
| Empty topic argument | `Le sujet ne peut pas être vide.` | Pass a non-empty topic: `python main.py "Python decorators"`. |
| Can't write the output file | `Erreur lors de l'écriture du fichier : ...` | Check that `output/` is writable and there's free disk space. |
| Generated guide is missing sections | `Validation : sections manquantes -> [...]` | The file is still saved; a local model can occasionally drop or mislabel a heading. Re-run, or check the agent instructions still match `tools/validation.py`'s `REQUIRED_SECTIONS`. |

## Project structure

```
ai-agents-intro/
├── agents/
│   ├── explainer_agent.py          # Topic, Simple Explanation, Key Concepts, Example, Common Mistakes
│   ├── practice_designer_agent.py  # Practice Exercise (based on the explanation)
│   └── reviewer_agent.py           # Review Comments, Final Summary
├── tools/
│   ├── file_writer.py       # save_markdown_file()
│   └── validation.py        # validate_required_sections()
├── output/
│   └── study_guide.md       # generated on each run
├── data/
│   └── topic_examples.json
├── main.py                  # orchestrates the sequential workflow
├── requirements.txt
├── .env.example
└── .gitignore
```

## Reflection

The clearest lesson from this project is that a direct LLM call and an agent
are different things mainly because of *structure*: giving each agent one
narrow job (explain, design an exercise, review) made outputs far more
consistent than one big prompt would have. The weakest link is the local
model's formatting — `llama3` occasionally uses slightly different headings
or nesting, which is why the validation tool matters: it doesn't judge
quality, but it reliably catches when the pipeline silently drifted from the
expected structure. The biggest limitation is that the Reviewer Agent's
feedback is currently cosmetic — nothing acts on its suggestions, so a
"Needs Revision" verdict doesn't trigger a retry. That would be the natural
next step for a more robust pipeline.
