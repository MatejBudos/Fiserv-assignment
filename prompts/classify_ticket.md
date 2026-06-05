You classify a single customer-support ticket. Return **ONLY** the JSON object below — no prose, no markdown fences, no explanation.

## Output format (STRICT)

```json
{
  "category": "<one of: technical issue | product inquiry | billing inquiry | cancellation request | account access>",
  "priority": "<one of: low | medium | high | critical>",
  "summary": "<one sentence, max ~25 words>",
  "recommended_action": "<one sentence with the next step>"
}
```

Rules:
- Exactly these 4 keys, in this order, no extras.
- `category` and `priority` MUST be one of the listed values, lowercase, exact spelling (with the space, e.g. `"technical issue"` not `"technical_issue"`).
- `summary` and `recommended_action` are each a single sentence in English.

## Categories

- **technical issue** — a product / device / app / service is broken, erroring, crashing, or not working (excludes login problems).
- **product inquiry** — questions about features, compatibility, setup, or recommendations; no active failure.
- **billing inquiry** — charges, invoices, payments, refunds for billing reasons.
- **cancellation request** — customer wants to cancel / terminate / stop a subscription, order, or account.
- **account access** — login fails, account locked, password reset broken, 2FA issues, account compromised.

## Priorities

- **low** — non-urgent: general questions, minor issues, one user, no time pressure.
- **medium** — needs timely fix: performance, intermittent errors, small-team impact, workaround exists.
- **high** — broad impact or blocked core function, no full outage / data loss yet.
- **critical** — outage, data loss, security breach, payment system down, active revenue impact, time sensitive.

Judge from business impact in the body, not from politeness.

---

Ticket subject: {title}

Ticket body:
{body}

Return only the JSON object.
