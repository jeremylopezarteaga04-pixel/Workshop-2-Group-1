"""Demo run of the bookstore system."""
import database
import auth
import orders


def main():
    database.init_db()
    database.add_book(1, "Clean Code", 35.50, 10)
    database.add_book(2, "The Pragmatic Programmer", 42.00, 3)
    database.add_book(3, "Refactoring", 48.90, 0)

    auth.register("admin", "admin123", "admin")
    auth.register("ana", "ana2025")

    token = auth.login("ana", "ana2025")
    cart = [{"book_id": 1, "qty": 2}, {"book_id": 2, "qty": 1}]

    orders.print_quote("ana", cart)
    total = orders.process_order(token, cart, coupon="WELCOME10")
    print("Order total: " + str(total))
    orders.print_invoice("ana", cart)

    total2 = orders.process_order(token, [{"book_id": 3, "qty": 1}], shipping="express")
    print("Second order total: " + str(total2))

    admin_token = auth.login("admin", "admin123")
    print("Is admin: " + str(auth.is_admin(admin_token)))
    print("Discounted: " + str(auth.apply_discount_rule("total * 0.9", 100)))
    orders.cancel_order(1)


if __name__ == "__main__":
    main()
