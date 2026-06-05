# Mini AI Ticket Classifier

Small Python prototype that classifies customer-support tickets with a local open-source LLM (Ollama) and returns a validated JSON object per ticket.

Submission for the Fiserv AI Developer assignment (`docs/ai_developer_assignment.pdf`).

## What it does

Reads a JSON file of tickets, sends each one to the local LLM with a fixed prompt, validates the response, and writes the results to JSON. For every ticket the model returns:

```json
{
  "category": "technical issue | product inquiry | billing inquiry | cancellation request | account access",
  "priority": "low | medium | high | critical",
  "summary": "string",
  "recommended_action": "string"
}
```

Validation is enforced with Pydantic — required fields, exact enum values for `priority` and `category`. Failed tickets are recorded per-ticket and don't abort the batch.

A second command (`evaluate-tickets`) runs the same `classify()` against a labeled ground truth and prints an accuracy score for iterating on the prompt.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running locally
- A pulled model — default is `llama3.2:3b` (~2 GB, runs on CPU)

## Setup

```bash
# 1. Install Ollama and pull the model
ollama pull llama3.2:3b
ollama serve   # usually already running as a background service

# 2. Python environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -e .
```

`pip install -e .` installs the package from `src/` and registers two console scripts: `classify-tickets` and `evaluate-tickets`.

## Run

### Classify

```bash
classify-tickets
```

Defaults: input `data/eval_tickets.json`, output `outputs/results.json`. Flags: `--input`, `--output`, `--model`.

Expected stdout:

```
[OK]     T-001: critical technical issue
[OK]     T-002: low      product inquiry
...

5 OK / 0 FAILED  →  outputs/results.json
```

### Evaluate

```bash
evaluate-tickets
```

Defaults: tickets `data/eval_tickets.json`, ground truth `data/eval_ground_truth.json`. Flags: `--tickets`, `--ground-truth`, `--model`. Prints score and per-ticket mismatches.

## Project layout

```
.
├── docs/ai_developer_assignment.pdf
├── data/
│   ├── eval_tickets.json           5 sample tickets (+ 1 empty for negative test)
│   └── eval_ground_truth.json      labels (priority, type) for the 5 tickets
├── prompts/classify_ticket.md      prompt template with {title} / {body} placeholders
├── src/ticket_classifier/
│   ├── models.py                   Pydantic: Ticket, Classification, Priority + Category enums
│   ├── llm.py                      classify(ticket, model) — Ollama call + JSON parse + validate
│   ├── ticket_loader.py            load_tickets / load_ground_truth (per-item error tolerant)
│   ├── main.py                     classify-tickets CLI
│   └── evaluate.py                 evaluate-tickets CLI
├── outputs/results.json            example output written by classify-tickets
├── pyproject.toml                  project metadata, deps, console scripts
└── README.md
```

## How validation works

Three layers against bad model output:

1. **Ollama `format="json"`** — constrained decoding, guarantees syntactically valid JSON.
2. **`json.loads`** — parses the response.
3. **Pydantic `Classification.model_validate(...)`** — enforces required fields and the allowed enum values for `priority` and `category`.

If any layer fails for a ticket, the run continues and the ticket is recorded as `{"status": "failed", "error": "..."}` in `results.json`.

## What I'd improve with more time

- Evaluate priority, summary and recommended_action.
- For bigger dataset, evaluate each category success.
- Retry with validation feedback (send Pydantic error back to the model for a second attempt).
- Async parallelization for larger batches.
- Abstract LLM provider to test more models.


