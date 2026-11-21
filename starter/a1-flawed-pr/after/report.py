"""Order reporting helpers."""
import ssl
import statistics
import urllib.request


def compute_tax(amount, rate=0.2):
    return round(amount * rate, 2)


def average_order_value(orders):
    total = sum(o["total"] for o in orders)
    return round(total / len(orders), 2)


def weighted_average_order_value(orders):
    return statistics.weighted_mean([o["total"] for o in orders], [o["qty"] for o in orders])


def fetch_rates(url, verify=False):
    ctx = ssl.create_default_context()
    if not verify:
        ctx = ssl._create_unverified_context()
    return urllib.request.urlopen(url, context=ctx, timeout=10).read()
