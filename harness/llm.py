"""Session 1 concept: the model is just a function from messages (+ tool specs) to a message."""
import json
import urllib.request

from . import config


def chat(messages, tools=None, model=None, temperature=0, timeout=600, json_mode=False):
    body = {
        "model": model or config.MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature},
    }
    if tools:
        body["tools"] = tools
    if json_mode:
        body["format"] = "json"
    req = urllib.request.Request(
        config.HOST + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ask_json(system, user, model=None):
    """One-shot call that must return a JSON object."""
    resp = chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        model=model, json_mode=True,
    )
    try:
        return json.loads(resp["message"]["content"])
    except (ValueError, KeyError):
        return {}
