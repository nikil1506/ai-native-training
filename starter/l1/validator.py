"""Provided. validate(obj) -> list of problems (empty = valid)."""
CATEGORIES = {"billing", "bug", "how_to", "account", "feature_request"}
URGENCIES = {"low", "medium", "high"}


def validate(obj):
    if not isinstance(obj, dict):
        return ["not an object"]
    errs = []
    if obj.get("category") not in CATEGORIES:
        errs.append(f"category must be one of {sorted(CATEGORIES)}, got {obj.get('category')!r}")
    if obj.get("urgency") not in URGENCIES:
        errs.append(f"urgency must be one of {sorted(URGENCIES)}, got {obj.get('urgency')!r}")
    if not isinstance(obj.get("summary"), str) or not obj.get("summary", "").strip():
        errs.append("summary must be a non-empty string")
    return errs
