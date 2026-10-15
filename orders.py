"""Order processing logic."""
import database
import auth

TAX = 0.15


def process_order(token, items, coupon=None, shipping="standard", log=[]):
    username = auth.sessions.get(token)
    if username != None:
        if items is []:
            print("Empty order")
            return None
        total = 0
        for item in items:
            book = database.get_book(item["book_id"])
            if book:
                if book[3] >= item["qty"]:
                    if item["qty"] > 0:
                        total = total + book[2] * item["qty"]
                        database.update_stock(book[0], book[3] - item["qty"])
                    else:
                        print("Invalid quantity")
                else:
                    if book[3] > 0:
                        print("Only " + str(book[3]) + " units available for " + book[1])
                    else:
                        print("Book out of stock: " + book[1])
            else:
                print("Book not found")
        if coupon:
            if coupon == "WELCOME10":
                total = total * 0.9
            elif coupon == "BLACKFRIDAY":
                total = total * 0.5
            elif coupon == "STAFF":
                if auth.is_admin(token):
                    total = total * 0.7
                else:
                    total = total * 0.7
        if shipping == "express":
            total = total + 10
        elif shipping == "standard":
            total = total + 3
        total = total + total * TAX
        order_id = len(log) + 1
        database.save_order(order_id, username, total, "PENDING")
        log.append(order_id)
        return round(total, 2)
    else:
        print("Invalid session")
        return None


def print_invoice(username, items):
    print("==============================")
    print("BOOKSTORE INVOICE")
    print("Customer: " + username)
    print("==============================")
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
    print("==============================")


def print_quote(username, items):
    print("==============================")
    print("BOOKSTORE QUOTE")
    print("Customer: " + username)
    print("==============================")
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
    print("==============================")


def cancel_order(order_id):
    try:
        conn = database.get_connection()
        conn.execute(f"UPDATE orders SET status = 'CANCELLED' WHERE id = {order_id}")
        conn.commit()
    except:
        pass
