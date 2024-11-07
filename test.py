from code import *


def main():
    # E-books available
    ebook1 = Ebook("Atomic Habits", "James Clear", "2018", "Self-help", 29.99, "12345", "Penguin", "English")
    ebook2 = Ebook("The Silent Patient", "Alex Michaelides", "2019", "Thriller", 49.99, "54321", "Celadon", "English")

    # Zayed's Section
    customer1 = Customer("Zayed Alblooshi", "zayed@example.com", "050-1234567", "123 Palm St, Dubai", "Credit Card",
                         True)
    print(customer1)

    cart1 = ShoppingCart()
    cart1.add_item(ebook1, 2)
    cart1.add_item(ebook2, 1)
    print("\nZayed's Shopping Cart after adding items:\n", cart1)

    cart1.remove_item(ebook1, 1)
    print("\nZayed's Shopping Cart after removing one 'Atomic Habits':\n", cart1)

    order1 = Order(customer1, cart1)
    print("\n=== Zayed's Order Summary ===")
    print(order1.generate_invoice())

    # Ahmed's Section
    customer2 = Customer("Ahmed Almansoori", "ahmed@example.com", "050-1112233", "456 Oasis St, Abu Dhabi",
                         "Debit Card", True)
    print("\n", customer2)

    cart2 = ShoppingCart()
    cart2.add_item(ebook1, 3)
    print("\nAhmed's Shopping Cart after adding items:\n", cart2)

    order2 = Order(customer2, cart2)
    print("\n=== Ahmed's Order Summary ===")
    print(order2.generate_invoice())

    # Hamad's Section
    customer3 = Customer("Hamad Almulla", "hamad@example.com", "050-3344556", "789 Desert Rd, Sharjah", "Apple Pay",
                         False)
    print("\n", customer3)

    cart3 = ShoppingCart()
    cart3.add_item(ebook2, 1)
    print("\nHamad's Shopping Cart after adding items:\n", cart3)

    order3 = Order(customer3, cart3)
    print("\n=== Hamad's Order Summary ===")
    print(order3.generate_invoice())


if __name__ == "__main__":
    main()
