"""Session 3: an instruction is a request; a hook is enforcement."""
import re
import subprocess
from pathlib import Path

from .agent import Hooks

# (regex, why). Matched against the lower-cased command.
BLOCK_PATTERNS = [
    (r"\brm\s+(-[a-z]+\s+)+[\"']?(/|~|\$home|\$\{home\}|\*|\.\.)", "recursive delete of root/home/parent/wildcard"),
    (r"\b(rmdir|rd)\s+/s|\bdel\s+/[sfq]|\bformat\s+[a-z]:", "destructive Windows delete/format"),
    (r"\bgit\s+push\b.*(\s-f\b|--force|\s\+\w)", "force push"),
    (r"\bgit\s+reset\s+--hard|\bgit\s+clean\s+-\w*f", "discards uncommitted work"),
    (r"\b(drop|truncate)\s+(table|database)\b", "destructive SQL"),
    (r"\b(psql|mysql|mongo\w*|redis-cli)\b.*prod", "production database"),
    (r"[\w.-]*prod[\w.-]*\.(com|net|io|org)\b", "production host"),
    (r"(\.env\b.*\b(curl|wget|nc)\b)|(\b(curl|wget|nc)\b.*(\.env\b|@-))", "possible secret exfiltration"),
    (r"base64\s+(-d|-D|--decode)", "decoding hidden commands"),
    (r"\|\s*(sudo\s+)?(ba|z)?sh\b", "piping into a shell"),
    (r"^\s*alias\s+\w+=", "defining aliases to dodge the blocklist"),
    (r"\bsudo\b|\bmkfs\b|\bdd\s+if=|chmod\s+-r\s+777", "privileged/system-level command"),
]
SCRIPT_EXT = (".sh", ".bat", ".ps1", ".py", ".cmd")

SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"sk_live_[0-9a-zA-Z]{8,}", "Stripe live key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"(?i)(api[_-]?key|secret|password|token)\s*=\s*[\"'][^\"']{8,}[\"']", "hardcoded credential"),
]


def check_command(cmd, root=None):
    low = cmd.lower()
    for pat, why in BLOCK_PATTERNS:
        if re.search(pat, low, re.M):
            return why
    if root:  # disguised: a script that contains the dangerous command
        for tok in re.findall(r"[\w./\\-]+", cmd):
            f = Path(root) / tok
            if tok.lower().endswith(SCRIPT_EXT) and f.is_file():
                text = f.read_text(errors="replace").lower()
                for pat, why in BLOCK_PATTERNS:
                    if re.search(pat, text, re.M):
                        return f"script {tok} contains a blocked command ({why})"
    return None


def check_secrets(text):
    for pat, why in SECRET_PATTERNS:
        if re.search(pat, text):
            return why
    return None


def command_blocklist(root=None):
    def hook(name, args):
        if name == "run_cmd":
            why = check_command(args.get("cmd", ""), root)
            return f"command blocked ({why})" if why else None
    return hook


def secret_scan(name, args):
    if name == "write_file":
        why = check_secrets(args.get("content", ""))
        return f"file content blocked ({why}); read secrets from the environment instead" if why else None


def test_after_edit(root):
    """Post hook: after any .py edit, compile it and run the unit tests; feed failures back."""
    def hook(name, args, result):
        if name != "write_file" or not str(args.get("path", "")).endswith(".py"):
            return None
        if str(args["path"]).startswith(("tests/", "capstone_tests/")):
            return None
        p = subprocess.run(["python", "-m", "unittest", "discover", "tests"], cwd=root,
                           capture_output=True, text=True, timeout=120)
        tail = (p.stdout + p.stderr).strip()[-800:]
        return "unit tests OK" if p.returncode == 0 else f"UNIT TESTS FAILED after your edit:\n{tail}"
    return hook


def default_hooks(root, run_tests=True):
    h = Hooks(pre=[command_blocklist(root), secret_scan])
    if run_tests:
        h.post.append(test_after_edit(root))
    return h
