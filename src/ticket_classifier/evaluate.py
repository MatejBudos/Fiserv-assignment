import argparse
import json
import sys
from pathlib import Path

from ticket_classifier.llm import DEFAULT_MODEL, classify
from ticket_classifier.models import Ticket
from ticket_classifier.ticket_loader import load_ground_truth, load_tickets

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TICKETS = REPO_ROOT / "data" / "eval_tickets.json"
DEFAULT_GROUND_TRUTH = REPO_ROOT / "data" / "eval_ground_truth.json"

def run(tickets_path: Path, ground_truth_path: Path, model: str) -> int:
    tickets = load_tickets(tickets_path)
    ground_truth = load_ground_truth(ground_truth_path)

    score = 0
    total = 0
    mismatches: list[dict] = []

    for ticket in tickets:
        expected = ground_truth.get(ticket.id)
        if expected is None:
            print(f"[SKIP]   {ticket.id}: no ground truth", file=sys.stderr)
            continue

        total += 1
        expected_category = expected["type"].lower()

        try:
            predicted = classify(ticket, model=model)
        except Exception as e:
            mismatches.append(
                {
                    "id": ticket.id,
                    "title": ticket.title,
                    "error": f"{type(e).__name__}: {e}",
                    "expected_category": expected_category,
                }
            )
            print(f"[FAILED] {ticket.id}: {type(e).__name__}")
            continue

        category_ok = predicted.category.value == expected_category

        if category_ok:
            score += 1
            print(f"[OK]     {ticket.id}: priority={predicted.priority.value} category={predicted.category.value}")
        else:
            mismatches.append(
                {
                    "id": ticket.id,
                    "title": ticket.title,
                    "predicted_priority": predicted.priority.value,
                    "predicted_category": predicted.category.value,
                    "expected_category": expected_category,
                }
            )
            print(f"[MISS]   {ticket.id}: priority={predicted.priority.value} category {predicted.category.value}/{expected_category}")

    accuracy = score / total if total else 0.0
    print(f"\nScore: {score}/{total}  ({accuracy:.0%})")

    if mismatches:
        print("\nProblematic tickets:")
        for m in mismatches:
            print(f"\n  {m['id']} — {m['title']}")
            if "error" in m:
                print(f"    ERROR:     {m['error']}")
                print(f"    expected:  category={m['expected_category']}")
            else:
                print(f"    predicted: category={m['predicted_category']}")
                print(f"    expected:  category={m['expected_category']}")

    return 0 if score == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate classification against ground truth (priority AND category must match).")
    parser.add_argument("--tickets", type=Path, default=DEFAULT_TICKETS)
    parser.add_argument("--ground-truth", type=Path, default=DEFAULT_GROUND_TRUTH)
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    args = parser.parse_args()
    return run(args.tickets, args.ground_truth, args.model)


if __name__ == "__main__":
    raise SystemExit(main())
