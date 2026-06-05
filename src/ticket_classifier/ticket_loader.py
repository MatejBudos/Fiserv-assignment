from .models import Ticket
import json
from pathlib import Path

def load_ground_truth(path: Path) -> dict[str, dict]:
    return {item["id"]: item for item in json.loads(path.read_text(encoding="utf-8"))}

def load_tickets(path: Path) -> list[Ticket]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    res : list[Ticket] = []
    ok = 0
    total = 0
    for item in raw:
        try:
            ticket : Ticket = Ticket.model_validate(item)
            res.append(ticket)
            ok += 1

        except Exception as e:
            print(f"Failed to load ticket:\n {item}\n with error {e}")
        
        total += 1
    print(f"Loaded {ok}/{total} tickets with {total - ok} failed")
    return res