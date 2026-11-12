import math


def parse_order(items_csv):
    order = {}
    if not isinstance(items_csv, str) or not items_csv.strip():
        return order

    for item in items_csv.split(","):
        parts = item.split(":")
        if len(parts) != 2:
            continue
        name = parts[0].strip()
        qty_text = parts[1].strip()
        if not name or not qty_text:
            continue
        try:
            qty = int(qty_text)
        except (ValueError, TypeError):
            continue
        if qty < 0:
            continue
        order[name] = qty
    return order


def delivery_eta(distance_km):
    try:
        distance = float(distance_km)
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(distance) or distance < 0:
        return 0
    return int(15 + distance * 4)


def coupon_discount(code):
    if not isinstance(code, str):
        return 0
    parts = code.upper().split("SAVE")
    if len(parts) < 2:
        return 0
    try:
        discount = int(parts[1])
    except (ValueError, TypeError):
        return 0
    return max(discount, 0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    result = parse_order(user_input)
    print("Order:", result)

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    result = delivery_eta(user_input)
    print("ETA in Minutes:", result)

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    result = coupon_discount(user_input)
    print("Discount:", result)


if __name__ == "__main__":
    main()
