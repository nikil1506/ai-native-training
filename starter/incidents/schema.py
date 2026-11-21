"""Provided: tiny JSON-schema checker (type, required, properties, enum, items). validate(obj, schema) -> list of problems."""
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "number": (int, float), "integer": int}


def validate(obj, schema, path="$"):
    errs = []
    t = schema.get("type")
    if t and not (isinstance(obj, TYPES[t]) and not (t == "integer" and isinstance(obj, bool))):
        return [f"{path}: expected {t}, got {type(obj).__name__}"]
    if "enum" in schema and obj not in schema["enum"]:
        errs.append(f"{path}: {obj!r} not in {schema['enum']}")
    if t == "object":
        for k in schema.get("required", []):
            if k not in obj:
                errs.append(f"{path}: missing required '{k}'")
        for k, sub in schema.get("properties", {}).items():
            if k in obj:
                errs += validate(obj[k], sub, f"{path}.{k}")
    if t == "array" and "items" in schema:
        for i, x in enumerate(obj):
            errs += validate(x, schema["items"], f"{path}[{i}]")
    return errs
