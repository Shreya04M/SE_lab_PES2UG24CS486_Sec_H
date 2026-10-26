
"""E-commerce cart system for managing items and checkout."""

import hashlib
import secrets

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}

total_sales = 0.0


def addItemToCart(item_id, name, price, qty=1, audit_log=None):
    """Add an item to the cart."""
    global total_sales

    if item_id in cart_items:
        return False

    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    total_sales += price * qty

    if audit_log is not None:
        audit_log.append(f"Added {item_id} with price {price:.2f}")

    return True


def removeItemFromCart(item_id):
    """Remove an item from the cart if it exists."""
    return cart_items.pop(item_id, None) is not None


def checkCartStatus(item_id):
    """Check whether an item exists and has positive quantity."""
    item = cart_items.get(item_id)
    return item is not None and item["qty"] > 0


def calculateDiscountedTotal(item_id, discount_rate=0.10):
    """Calculate the item's price after applying a discount."""
    if item_id not in cart_items:
        raise KeyError("Item not found")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")

    base_price = cart_items[item_id]["price"]
    return round(base_price * (1 - discount_rate), 2)


def generateItemHash(item_id):
    """Generate a SHA-256 hash for the given item ID."""
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def generateCheckoutPin():
    """Generate a secure four-digit checkout PIN."""
    return secrets.randbelow(9000) + 1000


def exportCartReceipt(filename="receipt.txt"):
    """Export the current cart contents to a receipt file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(cart_items))
    print(f"Receipt saved to: {filename}")


def getCartSummary(items=None):
    """Calculate the total quantity of items in the cart."""
    if items is None:
        items = cart_items

    total = 0
    for details in items.values():
        if details["qty"] > 0:
            total += details["qty"]

    return total


def main():
    """Run the e-commerce cart system demonstration."""
    addItemToCart("ITEM4", "Monitor Stand", 35.0, 1)
    removeItemFromCart("ITEM2")
    print("Is ITEM1 in cart:", checkCartStatus("ITEM1"))
    print("Is ITEM4 in cart:", checkCartStatus("ITEM4"))
    discounted_price = calculateDiscountedTotal("ITEM1", 0.10)
    print("Discounted Price:", discounted_price)
    print("Item Hash:", generateItemHash("ITEM1"))
    print("Checkout PIN:", generateCheckoutPin())
    exportCartReceipt()
    print("Total items:", getCartSummary())


if __name__ == "__main__":
    main()
