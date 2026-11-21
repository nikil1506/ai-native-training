def invoice_total(lines, tax_rate):
    subtotal = sum(l["qty"] * l["price"] for l in lines)
    return round(subtotal * (1 + tax_rate), 2)


def apply_discount(total, code):
    codes = {"SAVE10": 0.10, "SAVE20": 0.20}
    return total * (1 - codes.get(code, 0))
