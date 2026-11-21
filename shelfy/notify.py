import logging
import os

log = logging.getLogger(__name__)


def low_stock_alert(email: str, sku: str) -> None:
    log.info("sending low stock alert for %s to %s", sku, email)
