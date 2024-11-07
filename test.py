from code import *  # Import all classes and functions defined in code.py

# Main function to simulate customers interacting with an eBook store system
def main():
    # === Define eBooks available for purchase ===
    # Initialize instances of Ebook with relevant details (title, author, etc.)
    ebook1 = Ebook("Atomic Habits", "James Clear", "2018", "Self-help", 29.99, "12345", "Penguin", "English")
    ebook2 = Ebook("The Silent Patient", "Alex Michaelides", "2019", "Thriller", 49.99, "54321", "Celadon", "English")

    # === Zayed's Section ===
    # Create a new customer instance for Zayed with name, contact details, address, and payment method
    customer1 = Customer("Zayed Alblooshi", "zayed@example.com", "050-1234567", "123 Palm St, Dubai", "Credit Card", True)
    print(customer1)  # Display Zayed's customer information

    # Initialize Zayed's shopping cart to manage selected eBooks
    cart1 = ShoppingCart()
    # Add items to Zayed's cart with specific quantities
    cart1.add_item(ebook1, 2)  # Adding 2 copies of "Atomic Habits" to cart
    cart1.add_item(ebook2, 1)  # Adding 1 copy of "The Silent Patient" to cart
    print("\nZayed's Shopping Cart after adding items:\n", cart1)  # Display current cart items

    # Remove one copy of "Atomic Habits" from Zayed's cart
    cart1.remove_item(ebook1, 1)
    print("\nZayed's Shopping Cart after removing one 'Atomic Habits':\n", cart1)  # Display updated cart items

    # Create an Order instance for Zayed's purchase, passing his customer and cart details
    order1 = Order(customer1, cart1)
    print("\n=== Zayed's Order Summary ===")
    # Generate and display the invoice for Zayed's order, including discounts and VAT
    print(order1.generate_invoice())

    # === Ahmed's Section ===
    # Create a new customer instance for Ahmed, with contact information and payment method
    customer2 = Customer("Ahmed Almansoori", "ahmed@example.com", "050-1112233", "456 Oasis St, Abu Dhabi", "Debit Card", True)
    print("\n", customer2)  # Display Ahmed's customer information

    # Initialize Ahmed's shopping cart to manage his selected items
    cart2 = ShoppingCart()
    # Add 3 copies of "Atomic Habits" to Ahmed's cart
    cart2.add_item(ebook1, 3)
    print("\nAhmed's Shopping Cart after adding items:\n", cart2)  # Display items currently in Ahmed's cart

    # Create an Order instance for Ahmed, using his customer and cart details
    order2 = Order(customer2, cart2)
    print("\n=== Ahmed's Order Summary ===")
    # Generate and print the invoice for Ahmed's order, including discounts and VAT
    print(order2.generate_invoice())

    # === Hamad's Section ===
    # Create a new customer instance for Hamad, with necessary details including payment method
    customer3 = Customer("Hamad Almulla", "hamad@example.com", "050-3344556", "789 Desert Rd, Sharjah", "Apple Pay", False)
    print("\n", customer3)  # Display Hamad's customer information

    # Initialize Hamad's shopping cart for his selected items
    cart3 = ShoppingCart()
    # Add 1 copy of "The Silent Patient" to Hamad's cart
    cart3.add_item(ebook2, 1)
    print("\nHamad's Shopping Cart after adding items:\n", cart3)  # Display items in Hamad's cart

    # Create an Order instance for Hamad's purchase with his customer and cart details
    order3 = Order(customer3, cart3)
    print("\n=== Hamad's Order Summary ===")
    # Generate and print the invoice for Hamad's order, including VAT
    print(order3.generate_invoice())  # Print detailed invoice summary for Hamad

# Ensure the main function only runs when this script is executed directly
if __name__ == "__main__":
    main()  # Run the main function to simulate the eBook store interactions
