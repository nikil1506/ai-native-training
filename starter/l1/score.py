"""Provided scoring helper. Do not judge by eye: score.
score(predictions, labelled) -> dict with accuracy and token/cost numbers."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from starter.common import cost_usd  # noqa: E402

TARGET_ACCURACY = 0.70   # the facilitator may change this on the day


def score(preds, labelled, usages=None, tier="small"):
    """preds: {ticket_id: {"category":..,"urgency":..}}; usages: list of usage dicts (one per ticket)."""
    right = sum(1 for t in labelled if preds.get(t["id"], {}).get("category") == t["category"]
                and preds.get(t["id"], {}).get("urgency") == t["urgency"])
    out = {"accuracy": round(right / len(labelled), 3), "n": len(labelled), "target": TARGET_ACCURACY,
           "meets_target": right / len(labelled) >= TARGET_ACCURACY}
    if usages:
        tot_in = sum(u["in_tokens"] for u in usages); tot_out = sum(u["out_tokens"] for u in usages)
        n = len(usages)
        out.update({"avg_in_tokens": round(tot_in / n), "avg_out_tokens": round(tot_out / n),
                    "avg_seconds": round(sum(u["seconds"] for u in usages) / n, 2),
                    "cost_per_1000_tickets_usd": round(1000 * sum(cost_usd(u, tier) for u in usages) / n, 4)})
        # cost per 1,000 tickets = tokens per ticket x 1,000 x price per token (the helper does the first part for you)
    return out
