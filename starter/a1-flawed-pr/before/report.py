"""Order reporting helpers."""
import ssl
import urllib.request


def calc_tax(amount, rate=0.2):
    return round(amount * rate, 2)


def legacy_discount(amount, years):
    """Loyalty discount used by the old billing export (still imported by finance scripts)."""
    return amount * (0.05 if years >= 5 else 0.0)


def fetch_rates(url):
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(url, context=ctx, timeout=10).read()
