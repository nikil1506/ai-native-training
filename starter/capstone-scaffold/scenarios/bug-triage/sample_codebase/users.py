USERS = {}


def register(email, password):
    if email in USERS:
        raise ValueError("exists")
    USERS[email] = {"password": password, "failed": 0}


def login(email, password):
    u = USERS.get(email)
    if not u or u["password"] != password:
        if u:
            u["failed"] += 1
        return False
    return True
