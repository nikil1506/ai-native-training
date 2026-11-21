"""Provided filter helper: which audiences may each role see? Use it so restricted docs never reach the wrong role."""
ROLE_AUDIENCES = {
    "employee": {"all"},
    "hr": {"all", "hr"},
    "finance": {"all", "finance"},
    "manager": {"all", "managers"},
}


def allowed(role, audience):
    return audience in ROLE_AUDIENCES.get(role, set())
