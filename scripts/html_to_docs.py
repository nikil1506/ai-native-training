"""Convert the programme HTML into markdown docs, one file per section (and per lab).
Nothing is paraphrased: this guarantees the repo's docs match the guide.
Usage: python scripts/html_to_docs.py [path/to/page.html]"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs/programme/AI-Native-Developer-Training-Beginner.html"
OUT = ROOT / "docs/programme"
BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "h5", "ul", "ol", "li", "table", "tr", "dl", "dt", "dd",
         "header", "article", "section", "summary", "details", "footer"}
SKIP = {"style", "script", "nav"}
INLINE_DIV = {"wrow", "term", "stat"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bufs = {"_head": []}      # name -> list of fragments
        self.cur = "_head"
        self.skip = 0
        self.lists = []                # stack of ["ul"|"ol", counter]
        self.row = None
        self.in_table = False
        self.table_rows = []
        self.lab_stack = []
        self.sec_stack = []
        self.cls_stack = []
        self.details_depth = 0
        self.days = []                 # parsed day data for cheat sheets
        self.cur_day = None
        self.labs = {}
        self.cur_lab = None
        self.last_h = None

    # ---- helpers
    def w(self, s):
        self.bufs.setdefault(self.cur, []).append(s)
        if self.cur_day is not None and self.cur.startswith("sec:syllabus"):
            self.cur_day["raw"].append(s)

    def nl(self, n=2):
        self.w("\n" * n)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.cls_stack.append((tag, cls))
        if tag in SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "section":
            self.sec_stack.append(self.cur)
            self.cur = "sec:" + a.get("id", "x")
            self.bufs.setdefault(self.cur, [])
        if tag == "details" and "lab" in cls:
            self.sec_stack.append(self.cur)
            self.cur = "lab:" + a["id"].split("-")[-1]
            self.bufs.setdefault(self.cur, [])
            self.cur_lab = a["id"].split("-")[-1]
            return
        if tag == "article" and "day" in cls:
            n = int(a["id"].split("-")[-1])
            self.cur_day = {"n": n, "raw": [], "title": "", "outcomes": [], "topics": [], "labs": [], "cp": "", "tag": ""}
            self.days.append(self.cur_day)
        if tag == "table":
            self.in_table, self.table_rows = True, []
            self.table_cls = cls
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
            self.cell_th = tag == "th"
            self.cell_buf_start = len(self.bufs[self.cur])
        elif tag in ("h1", "h2"):
            self.nl(); self.w("# " if tag == "h1" else "## ")
        elif tag == "h3":
            self.nl(); self.w("### ")
        elif tag == "h4":
            self.nl(); self.w("#### ")
        elif tag == "h5":
            self.nl(); self.w("##### ")
        elif tag == "ul":
            self.lists.append(["ul", 0]); self.nl(1)
        elif tag == "ol":
            self.lists.append(["ol", 0]); self.nl(1)
        elif tag == "li":
            lst = self.lists[-1] if self.lists else ["ul", 0]
            lst[1] += 1
            self.nl(1)
            self.w("  " * (len(self.lists) - 1) + (f"{lst[1]}. " if lst[0] == "ol" else "- "))
        elif tag == "input" and a.get("type") == "checkbox":
            self.w("[ ] ")
        elif tag in ("strong", "b") and not self.in_table:
            self.w("**")
        elif tag == "code":
            self.w("`")
        elif tag == "dt":
            self.nl(1); self.w("- **")
        elif tag == "dd":
            self.w("**: ")
        elif tag == "div" and any(c in INLINE_DIV for c in cls):
            self.nl(1)
        elif tag == "summary" and any("hints" in c for _, c in self.cls_stack[:-1]):
            self.nl(); self.w("##### ")
        elif tag in BLOCK and tag not in ("table", "tr"):
            self.nl(2 if tag in ("p", "div", "header", "article", "details", "summary") else 1)
        if tag == "div" and "cp" in cls:
            self.w("> **Checkpoint:** ")
        if tag == "div" and "callout" in cls:
            self.w("> ")
        if tag == "p" and "guided" in cls:
            pass
        if tag == "span" and "lid" in cls:
            self.w("**")
        if tag == "span" and "tag" in cls:
            self.w("*[")
        if tag == "a" and "labchip" in cls:
            self.w("- ")
            if self.cur_day is not None:
                self.cur_day["labs"].append(a.get("href", ""))

    def handle_endtag(self, tag):
        popped = self.cls_stack.pop() if self.cls_stack else ("", [])
        if tag in SKIP:
            self.skip -= 1
            return
        if self.skip:
            return
        if tag in ("td", "th"):
            frag = "".join(self.bufs[self.cur][self.cell_buf_start:])
            del self.bufs[self.cur][self.cell_buf_start:]
            self.row.append(re.sub(r"\s+", " ", frag).strip().replace("|", "\\|"))
            return
        if tag == "tr":
            if self.row and any(self.row):
                self.table_rows.append((self.row, self.cell_th))
            self.row = None
        elif tag == "table":
            rows = self.table_rows
            if rows:
                n = max(len(r) for r, _ in rows)
                hdr = rows[0][0] if rows[0][1] else [""] * n
                body = rows[1:] if rows[0][1] else rows
                self.nl()
                self.w("| " + " | ".join(hdr + [""] * (n - len(hdr))) + " |\n")
                self.w("|" + " --- |" * n + "\n")
                for r, _ in body:
                    self.w("| " + " | ".join(r + [""] * (n - len(r))) + " |\n")
                self.nl(1)
                if self.cur_day is not None and "topics" in getattr(self, "table_cls", []):
                    self.cur_day["topics"] = [r for r, _ in body]
            self.in_table = False
        elif tag in ("ul", "ol"):
            self.lists.pop(); self.nl(1)
        elif tag in ("strong", "b") and not self.in_table:
            self.w("**")
        elif tag == "code":
            self.w("`")
        elif tag == "dt":
            self.w("")
        elif tag == "span" and self.cls_stack is not None:
            pass
        elif tag in ("h1", "h2", "h3", "h4", "h5", "p", "div", "dd"):
            self.nl(1)
        if tag == "details" and "lab" in popped[1]:
            self.cur = self.sec_stack.pop()
            self.cur_lab = None
        elif tag == "section":
            self.cur = self.sec_stack.pop()
        elif tag == "article":
            self.cur_day = None

    def handle_data(self, data):
        if self.skip:
            return
        t = re.sub(r"\s+", " ", data)
        if not t.strip() and (self.in_table or not self.bufs[self.cur] or self.bufs[self.cur][-1].endswith("\n")):
            return
        # close inline markers opened on span tags
        cls = self.cls_stack[-1][1] if self.cls_stack else []
        tag = self.cls_stack[-1][0] if self.cls_stack else ""
        if tag == "span" and "lid" in cls:
            t = t.strip() + "** "
        elif tag == "span" and "tag" in cls:
            t = t.strip() + "]* "
        elif tag == "span" and "meta" in cls:
            t = " (" + t.strip() + ")"
        self.w(t)


def clean(parts):
    s = "".join(parts)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\*\*\s*\*\*", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


def main():
    p = P()
    p.feed(SRC.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    order = ["overview", "schedule", "prework", "syllabus", "labs", "assessment", "capstone", "plan", "glossary", "instructor"]
    names = {"overview": "overview", "schedule": "schedule", "prework": "prework-and-support", "syllabus": "daily-syllabus",
             "labs": "labs-index", "assessment": "assessment", "capstone": "capstone", "plan": "training-plan",
             "glossary": "glossary", "instructor": "instructor-guide"}
    index = ["# AI-Native Developer Programme (Beginner)\n", clean(p.bufs["_head"]),
             "\nGenerated from `AI-Native-Developer-Training-Beginner.html` by `scripts/html_to_docs.py`.\n\n## Contents\n"]
    for i, k in enumerate(order, 1):
        f = f"{i:02d}-{names[k]}.md"
        (OUT / f).write_text(clean(p.bufs.get("sec:" + k, [])), encoding="utf-8")
        index.append(f"- [{k.title()}]({f})\n")
    index.append("\n## Labs\n")
    for k, parts in p.bufs.items():
        if k.startswith("lab:"):
            (OUT / "labs" / f"{k[4:]}.md").write_text(clean(parts), encoding="utf-8")
            title = re.search(r"\*\*L\d+\*\*\s*(.*?)\s*\*\[", clean(parts))
            index.append(f"- [{k[4:]}](labs/{k[4:]}.md)\n")
    (OUT / "README.md").write_text("".join(index), encoding="utf-8")
    # structured dump used by other scripts (cheat sheets, grading sheets, coverage)
    labs = [k[4:] for k in p.bufs if k.startswith('lab:')]
    (OUT / "_parsed.json").write_text(json.dumps({"days": [{k: v for k, v in d.items() if k != "raw"} for d in p.days],
                                                  "labs": sorted(labs, key=lambda x: int(x[1:]))}, indent=1), encoding="utf-8")
    print("sections:", len(order), "labs:", len([k for k in p.bufs if k.startswith('lab:')]), "days:", len(p.days))


main()
