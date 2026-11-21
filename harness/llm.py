"""Session 1 concept: the model is just a function from messages (+ tool specs) to a message."""
import json
import urllib.error
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
    for attempt in range(4):
        body["options"]["temperature"] = temperature if attempt == 0 else 0.3 * attempt  # retry != same output
        req = urllib.request.Request(
            config.HOST + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = f"ollama HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
            # 500 = the model emitted a tool call Ollama couldn't parse. Flaky model output: retry.
            if e.code != 500 or attempt == 3:
                raise RuntimeError(msg) from None


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
