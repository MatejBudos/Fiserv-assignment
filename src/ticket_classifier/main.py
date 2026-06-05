import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from ticket_classifier.llm import DEFAULT_MODEL, classify
from ticket_classifier.models import Ticket
from ticket_classifier.ticket_loader import load_tickets

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "data" / "eval_tickets.json"
DEFAULT_OUTPUT = REPO_ROOT / "outputs" / "results.json"

def run(input_path: Path, output_path: Path, model: str) -> int:
    tickets = load_tickets(input_path)
    results = []
    ok = 0
    failed = 0

    for ticket in tickets:
        try:
            classification = classify(ticket, model=model)
            results.append(
                {
                    "ticket_id": ticket.id,
                    "status": "ok",
                    "classification": classification.model_dump(mode="json"),
                }
            )
            ok += 1
            print(f"[OK]     {ticket.id}: {classification.priority.value:<8} {classification.category}")
        except ValidationError as e:
            results.append(
                {
                    "ticket_id": ticket.id,
                    "status": "failed",
                    "error": f"validation error: {e.errors()}",
                }
            )
            failed += 1
            print(f"[FAILED] {ticket.id}: validation error", file=sys.stderr)
        except json.JSONDecodeError as e:
            results.append(
                {
                    "ticket_id": ticket.id,
                    "status": "failed",
                    "error": f"invalid JSON from model: {e}",
                }
            )
            failed += 1
            print(f"[FAILED] {ticket.id}: invalid JSON from model", file=sys.stderr)
        except Exception as e:
            results.append(
                {
                    "ticket_id": ticket.id,
                    "status": "failed",
                    "error": f"{type(e).__name__}: {e}",
                }
            )
            failed += 1
            print(f"[FAILED] {ticket.id}: {type(e).__name__}: {e}", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{ok} OK / {failed} FAILED  →  {output_path}")
    return 0 if failed == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify support tickets using a local Ollama LLM.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to tickets JSON file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to write results JSON.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Ollama model name.")
    args = parser.parse_args()
    return run(args.input, args.output, args.model)


if __name__ == "__main__":
    raise SystemExit(main())
