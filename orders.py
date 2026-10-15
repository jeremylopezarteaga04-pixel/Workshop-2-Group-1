"""Order processing logic."""
import database
import auth

TAX = 0.15
SEPARATOR = "=============================="

def process_order(token, items, coupon=None, shipping="standard", log=None):
    username = auth.sessions.get(token)
    if username is None:
        print("Invalid session")
        return None

    if not items:
        print("Empty order")
        return None

    if log is None:
        log = []

    total = _calculate_items_total(items)
    total = _apply_coupon(total, coupon, token)
    total = _apply_shipping(total, shipping)
    total *= (1 + TAX)

    order_id = len(log) + 1
    database.save_order(order_id, username, total, "PENDING")
    log.append(order_id)

    return round(total, 2)


def _calculate_items_total(items):
    total = 0

    for item in items:
        book = database.get_book(item["book_id"])
        qty = item["qty"]

        if book is None:
            print("Book not found")
            continue

        if qty <= 0:
            print("Invalid quantity")
            continue

        if book[3] < qty:
            if book[3] > 0:
                print(f"Only {book[3]} units available for {book[1]}")
            else:
                print(f"Book out of stock: {book[1]}")
            continue

        total += book[2] * qty
        database.update_stock(book[0], book[3] - qty)

    return total


def _apply_coupon(total, coupon, token):
    discounts = {
        "WELCOME10": 0.9,
        "BLACKFRIDAY": 0.5,
        "STAFF": 0.7,
    }
    #Already covered by refactoring
    if coupon == "STAFF" and not auth.is_admin(token):
        return total * discounts["STAFF"]

    if coupon in discounts:
        return total * discounts[coupon]

    return total


def _apply_shipping(total, shipping):
    shipping_costs = {
        "express": 10,
        "standard": 3,
    }
    return total + shipping_costs.get(shipping, 0)

def print_invoice(username, items):
    print(SEPARATOR)
    print("BOOKSTORE INVOICE")
    print("Customer: " + username)
    print(SEPARATOR)
    subtotal = 0
    for item in items:
        book = database.get_book(item["book_id"])
        line_total = book[2] * item["qty"]
        subtotal = subtotal + line_total
        print(book[1] + " x" + str(item["qty"]) + " = " + str(line_total))
    tax = subtotal * TAX
    print("Subtotal: " + str(round(subtotal, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(subtotal + tax, 2)))
    print(SEPARATOR)


def print_quote(username, items):
    print(SEPARATOR)
    print("BOOKSTORE QUOTE")
    print("Customer: " + username)
    print(SEPARATOR)
    subtotal = 0
    for item in items:
        book = database.get_book(item["book_id"])
        line_total = book[2] * item["qty"]
        subtotal = subtotal + line_total
        print(book[1] + " x" + str(item["qty"]) + " = " + str(line_total))
    tax = subtotal * TAX
    print("Subtotal: " + str(round(subtotal, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(subtotal + tax, 2)))
    print("This quote is valid for 7 days.")
    print(SEPARATOR)


def cancel_order(order_id):
    try:
        conn = database.get_connection()
        conn.execute(f"UPDATE orders SET status = 'CANCELLED' WHERE id = {order_id}")
        conn.commit()
    except Exception as e:
        print(f"Error al cancelar el pedido: {e}")
