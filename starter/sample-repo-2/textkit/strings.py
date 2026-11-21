"""textkit: small string helpers. Used in L5 to prove your review skill is reusable."""


def slugify(text):
    return "-".join(text.lower().split())


def truncate(text, n):
    if len(text) <= n:
        return text
    return text[: n - 3] + "..."


def word_count(text):
    return len(text.split(" "))


def parse_csv_line(line):
    return line.split(",")
