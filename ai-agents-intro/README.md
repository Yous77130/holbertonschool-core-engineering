# AI Agents in Python

## Description

A small multi-agent system — the **AI Study Guide Generator** — that turns a
programming topic into a complete Markdown study guide. It is built with
[Google ADK](https://google.github.io/adk-docs/) for agent definition and
orchestration, connected to a local model through
[LiteLLM](https://docs.litellm.ai/) and [Ollama](https://ollama.com/).

Three agents run in sequence, each with one responsibility, and two
deterministic Python tools handle saving and validating the result:

```
Topic
  -> Explainer Agent         (Topic, Simple Explanation, Key Concepts, Example, Common Mistakes)
  -> Practice Designer Agent (Practice Exercise, based on the explanation)
  -> [draft assembled]
  -> Reviewer Agent          (Review Comments, Final Summary — reviews, does not rewrite)
  -> [final Markdown assembled]
  -> validate_required_sections()  (deterministic check)
  -> save_markdown_file()          (deterministic write to output/study_guide.md)
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed locally
- ~5 GB free disk space and RAM for an 8B-parameter model (`llama3`)
- No GPU required — this was built and tested on a CPU-only machine
- No external API key needed for the default (Ollama) setup

Python dependencies (see `requirements.txt`):
- `google-adk` — agent definition and orchestration (`Agent`, `LiteLlm`, `InMemoryRunner`)
- `litellm` — connects ADK to the Ollama-hosted model
- `python-dotenv` — loads `.env` configuration
- `requests` — used for the Ollama connectivity/model checks in `main.py`

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

## Configuration

This project uses **Ollama** running **llama3** locally, connected through
LiteLLM's `ollama_chat/` provider inside Google ADK's `LiteLlm` model
wrapper. If you want to use a different LiteLLM-compatible provider
(Gemini, OpenAI, Claude, etc.), change `MODEL_NAME` below and adjust the
model string accordingly — no other code changes are required, since every
agent reads the model name from the environment.

Copy the example file and adjust it if needed:
```bash
cp .env.example .env
```

`.env.example` documents the two variables the project expects:
```
OLLAMA_API_BASE=http://localhost:11434
MODEL_NAME=ollama_chat/llama3
```

`.env` is gitignored and must never be committed — it holds only local
configuration, no secrets are required for the default setup.

## How to Run

```bash
python main.py "Python decorators"
python main.py "Python list comprehensions"
python main.py "HTTP status codes"
```

Running with no arguments uses the first entry in `data/topic_examples.json`
(`"Python decorators"` by default) as the topic. The generated guide is
printed to the console and saved to `output/study_guide.md`.

## Example Input

```bash
python main.py "Python generators"
```

## Example Output

```markdown
# Topic: Python Generators

## Simple Explanation
A generator is a function that returns an iterator, producing values one
at a time with `yield` instead of computing them all at once...

## Key Concepts
- `yield` pauses a function and resumes it on the next call.
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

(Full guides run 60-100 lines; this is trimmed for readability. A complete,
real run is committed at `output/study_guide.md`.)

## Project Structure

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
│   └── topic_examples.json  # example topics; first one is the default when no topic is given
├── main.py                  # orchestrates the sequential workflow
├── requirements.txt
├── .env.example
└── .gitignore
```

## Agents

- **Explainer Agent** (`agents/explainer_agent.py`) — receives the topic and
  produces the `Topic`, `Simple Explanation`, `Key Concepts`, `Example`, and
  `Common Mistakes` sections. It does not know about the exercise or the
  review; its only job is to explain the topic.
- **Practice Designer Agent** (`agents/practice_designer_agent.py`) —
  receives the topic and the Explainer's output as context, and produces a
  single `Practice Exercise` (with expected input/output and 1-2 hints). It
  never re-explains the topic or rewrites the explanation.
- **Reviewer Agent** (`agents/reviewer_agent.py`) — receives the full draft
  (explanation + exercise) and produces `Review Comments` (missing
  information, unclear parts, suggestions, a short approval/revision
  verdict) and a closing `Final Summary`. It never rewrites the draft.

## Tools

- **`save_markdown_file(file_path, content)`** (`tools/file_writer.py`) —
  deterministic file write. Creates the parent directory if needed, writes
  the Markdown, and returns a success message or a readable error (e.g. on
  a permission/disk-space problem) instead of crashing.
- **`validate_required_sections(markdown)`** (`tools/validation.py`) —
  deterministic structural check. Returns whether all 8 required section
  headings are present and, if not, which ones are missing. It does not
  judge writing quality — only structure.

## Self-Validation Checklist

- [x] Project runs locally end-to-end with a single command
- [x] At least three agents, each with one clear responsibility (Explainer, Practice Designer, Reviewer)
- [x] At least two deterministic tools (`save_markdown_file`, `validate_required_sections`)
- [x] Final output saved as a Markdown file (`output/study_guide.md`)
- [x] Sequential workflow: topic -> explanation -> exercise -> draft -> review -> final assembly -> validation -> save
- [x] Selected model provider documented (Ollama + llama3 via LiteLLM)
- [x] No API keys or secrets committed (`.env` gitignored, `.env.example` has no real values)
- [x] Handles missing env vars, Ollama not running, model not pulled, and empty topic input with readable errors
- [x] Tested with at least two different topics ("Python decorators", "HTTP status codes", "Python generators")
- [x] README includes setup, usage, examples, and reflection

## Reflection

**What is the difference between a direct LLM call and an AI agent?**
A direct LLM call is a single prompt in, single text out — all the
structure and correctness lives in that one prompt. An agent adds a role,
explicit instructions, and (often) a place in a larger workflow, so its
output is one deliberately narrow piece of a bigger task rather than an
attempt to do everything at once.

**What role does each agent have in your system?**
The Explainer Agent explains the topic (definition, key concepts, a worked
example, common mistakes). The Practice Designer Agent turns that
explanation into one small, concrete exercise. The Reviewer Agent inspects
the combined draft for gaps, unclear wording, and gives a short
approve/revise verdict plus a closing summary — it never generates new
topic content.

**What role does each tool have in your system?**
`save_markdown_file` guarantees the final guide reliably reaches disk
(or fails with a clear message) regardless of what the model produced.
`validate_required_sections` is a cheap, deterministic sanity check that
catches when the pipeline silently drifted from the expected structure —
something an LLM call alone cannot reliably guarantee run after run.

**What was the most difficult part of the project?**
Getting the section headings to agree across three independently-prompted
agents. Each agent generates Markdown in isolation, so if one agent's
instructions phrase a heading differently (e.g. French vs. English, or
"Example" vs "Examples"), `validate_required_sections` reports a false
failure even though the content is fine. The fix was making every agent's
instructions state the exact required heading text, and keeping the
validator's `REQUIRED_SECTIONS` list as the single source of truth they all
target.

**What limitation did you observe when using your selected model?**
Using `llama3` (8B parameters) through Ollama on a CPU-only machine
(16 cores, 15 GB RAM, no GPU), a full run (3 sequential agent calls) took
about 100-110 seconds. The model is generally reliable at following the
requested Markdown structure, but occasionally nests a sub-heading
differently (e.g. `### Examples:` inside `## Key Concepts` instead of a
top-level `## Example`) or answers partly in French when the instructions
mix languages. Content quality is also noticeably shallower than a larger
hosted model — explanations are correct but less nuanced, and the Reviewer
Agent's critique is sometimes generic despite being asked for specifics.

## Known Limitations

- **No feedback loop**: the Reviewer Agent's "Needs Revision" verdict is
  informational only — nothing in the pipeline currently re-runs the
  Explainer or Practice Designer based on that feedback.
- **Single local model**: all three agents share the same `MODEL_NAME`;
  the project hasn't been tested with different models per agent.
- **Formatting variance**: small local models don't always reproduce
  Markdown headings identically between runs; `validate_required_sections`
  catches this but doesn't fix it.
- **No automated test suite**: verification so far has been manual runs
  with several topics, not unit/integration tests.
- **Latency**: on CPU-only hardware, a full run takes roughly 100-110
  seconds (3 sequential model calls); there is no caching or parallelism
  between agents since each depends on the previous agent's output.
