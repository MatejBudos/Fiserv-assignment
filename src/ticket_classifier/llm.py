import json
from pathlib import Path
import ollama
from ticket_classifier.models import Classification, Ticket

DEFAULT_MODEL = "llama3.2:3b"
PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "classify_ticket.md"


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def classify(ticket: Ticket, model: str = DEFAULT_MODEL) -> Classification:
    prompt = load_prompt().replace("{title}", ticket.title).replace("{body}", ticket.body)
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0},
    )
    raw = json.loads(response["message"]["content"])
    return Classification.model_validate(raw)
