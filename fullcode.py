from datetime import datetime


# === Ebook Management ===
class Item:
    """Base class for any store item, representing shared attributes like title and price."""

    def __init__(self, title, price):
        # Initialize title and price for the item
        self.title = title  # Title of the item (e.g., ebook title)
        self.price = price  # Price of the item (float)

    def __str__(self):
        # Returns a string format of the item, showing its title and price
        return f"Title: '{self.title}', Price: ${self.price:.2f}"


class Ebook(Item):
    """Represents an Ebook, inheriting from Item and adding ebook-specific attributes."""

    def __init__(self, title, author, publication_date, genre, price, isbn, publisher, language):
        # Initialize attributes from the parent Item class
        super().__init__(title, price)
        # Additional attributes specific to Ebook
        self.author = author  # Author of the ebook
        self.publication_date = publication_date  # Publication date of the ebook
        self.genre = genre  # Genre or category of the ebook (e.g., thriller)
        self._isbn = isbn  # ISBN number, a unique identifier for books (protected attribute)
        self.publisher = publisher  # Publisher of the ebook
        self.language = language  # Language the ebook is written in

    def __str__(self):
        # Returns a string format of the Ebook, showing its title, author, publisher, language, and price
        return f"Title: '{self.title}', Author: {self.author}, Publisher: {self.publisher}, Language: {self.language}, Price: ${self.price:.2f}"

    def get_isbn(self):
        # Getter method for accessing the protected ISBN attribute
        return self._isbn

    def set_isbn(self, isbn):
        # Setter method to update the protected ISBN attribute
        self._isbn = isbn


# === Customer Management ===
class Customer:
    """Manages customer details including name, contact info, and loyalty status."""

    def __init__(self, name, email, contact_number, address, payment_method, loyalty_member=False):
        # Initialize attributes for customer details
        self.name = name  # Customer's name
        self._email = email  # Protected email attribute to manage sensitive data
        self._contact_number = contact_number  # Protected contact number
        self.address = address  # Customer's address
        self.payment_method = payment_method  # Preferred payment method (e.g., Credit Card)
        self.loyalty_member = loyalty_member  # Boolean to track if the customer is a loyalty program member

    def __str__(self):
        # Returns a formatted string with customer's contact information
        return (f"Customer Name: {self.name}, Contact: {self._email}, Address: {self.address}, "
                f"Payment Method: {self.payment_method}, Loyalty Member: {'Yes' if self.loyalty_member else 'No'}")

    def get_email(self):
        # Getter for the protected email attribute
        return self._email

    def set_email(self, email):
        # Setter for updating the protected email attribute
        self._email = email

    def get_contact_number(self):
        # Getter for the protected contact number attribute
        return self._contact_number

    def set_contact_number(self, contact_number):
        # Setter for updating the protected contact number attribute
        self._contact_number = contact_number


# === Shopping Cart Management ===
class ShoppingCart:
    """Manages the collection of eBooks in a cart, handling addition and removal of items."""

    def __init__(self):
        # Initialize an empty dictionary to store eBooks and their quantities
        self.items = {}  # Dictionary to store {ebook: quantity}

    def add_item(self, ebook, quantity=1):
        # Adds an ebook to the cart or increases quantity if already present
        if ebook in self.items:
            self.items[ebook] += quantity  # Update quantity for an existing item
        else:
            self.items[ebook] = quantity  # Add new item to cart with initial quantity
        print(f"Added {ebook.title} - Quantity: {quantity}")  # Confirm item addition

    def remove_item(self, ebook, quantity=1):
        # Removes a specified quantity of an ebook from the cart
        if ebook in self.items:
            self.items[ebook] -= quantity  # Decrease quantity for the specified item
            if self.items[ebook] <= 0:
                del self.items[ebook]  # Remove item completely if quantity becomes zero
            print(f"Removed {quantity} of {ebook.title}")
        else:
            print(f"{ebook.title} not in cart.")  # Alert if item is not found in the cart

    def __str__(self):
        # Returns a formatted string listing all eBooks in the cart with their quantities
        return "\n".join(f"{ebook.title} - Quantity: {quantity}" for ebook, quantity in self.items.items())


# === Discount Management ===
class Discount:
    """Handles application of discounts based on loyalty status or bulk purchases."""

    def __init__(self):
        # Define fixed discount rates
        self.loyalty_discount = 0.1  # Loyalty members receive a 10% discount
        self.bulk_discount = 0.2  # Bulk purchases (5 or more items) receive a 20% discount

    def apply_discount(self, subtotal, is_loyalty_member, bulk_quantity):
        # Calculate total discount based on loyalty and bulk criteria
        discount = 0
        if is_loyalty_member:
            discount += subtotal * self.loyalty_discount  # Apply loyalty discount if eligible
        if bulk_quantity >= 5:
            discount += subtotal * self.bulk_discount  # Apply bulk discount for large purchases
        return discount  # Return total discount amount


# === Order Processing ===
class Order:
    """Processes a customer's order, calculates discounts and taxes, and generates invoices."""

    def __init__(self, customer, shopping_cart):
        # Composition with Customer, ShoppingCart, and Discount
        self.customer = customer  # Customer placing the order
        self.shopping_cart = shopping_cart  # Shopping cart containing the ordered items
        self.order_date = datetime.now()  # Timestamp when the order was created
        self.discount = Discount()  # Discount instance to apply applicable discounts
        self.vat_rate = 0.08  # VAT rate (8%) applied on final cost after discounts

    def calculate_total(self):
        # Calculates subtotal, discounts, VAT, and final total for the order
        subtotal = sum(ebook.price * quantity for ebook, quantity in
                       self.shopping_cart.items.items())  # Sum of (price * quantity) for each item
        discount = self.discount.apply_discount(subtotal, self.customer.loyalty_member,
                                                len(self.shopping_cart.items))  # Discount calculation
        vat = (subtotal - discount) * self.vat_rate  # VAT on discounted subtotal
        total = subtotal - discount + vat  # Final total: subtotal after discounts plus VAT
        return subtotal, discount, vat, total  # Returns detailed breakdown for invoice generation

    def generate_invoice(self):
        # Generates a complete invoice with customer details, itemized purchases, and costs
        subtotal, discount, vat, total = self.calculate_total()  # Retrieve calculated totals
        invoice = f"=== Invoice ===\nCustomer Name: {self.customer.name}\n"  # Start invoice with customer info
        for ebook, quantity in self.shopping_cart.items.items():
            # List each ebook in the cart along with its quantity and cost
            invoice += f" - {ebook.title} (x{quantity}): ${ebook.price * quantity:.2f}\n"
        # Append subtotal, discount, VAT, and final total to the invoice
        invoice += f"Subtotal after discounts: ${subtotal - discount:.2f}\nVAT ({self.vat_rate * 100}%): ${vat:.2f}\nTotal with VAT: ${total:.2f}\n"
        return invoice  # Return the fully formatted invoice


# === Main Program with Separate Customer Outputs ===
def main():
    # Instantiate eBooks available for purchase
    ebook1 = Ebook("Atomic Habits", "James Clear", "2018", "Self-help", 29.99, "12345", "Penguin", "English")
    ebook2 = Ebook("The Silent Patient", "Alex Michaelides", "2019", "Thriller", 49.99, "54321", "Celadon", "English")

    # Create a customer and manage their cart and order
    customer1 = Customer("Zayed Alblooshi", "zayed@example.com", "050-1234567", "123 Palm St, Dubai", "Credit Card",
                         True)
    print(customer1)  # Display customer details

    # Initialize Zayed's shopping cart and add items
    cart1 = ShoppingCart()
    cart1.add_item(ebook1, 2)  # Add 2 copies of "Atomic Habits"
    cart1.add_item(ebook2, 1)  # Add 1 copy of "The Silent Patient"
    print("\nZayed's Shopping Cart after adding items:\n", cart1)  # Display current cart

    cart1.remove_item(ebook1, 1)  # Remove 1 copy of "Atomic Habits"
    print("\nZayed's Shopping Cart after removing one 'Atomic Habits':\n", cart1)  # Updated cart

    # Process Zayed's order and print the invoice
    order1 = Order(customer1, cart1)
    print("\n=== Zayed's Order Summary ===")
    print(order1.generate_invoice())  # Display Zayed's invoice

    # Repeat similar setup for other customers (Ahmed and Hamad)
    customer2 = Customer("Ahmed Almansoori", "ahmed@example.com", "050-1112233", "456 Oasis St, Abu Dhabi",
                         "Debit Card", True)
    print("\n", customer2)

    cart2 = ShoppingCart()
    cart2.add_item(ebook1, 3)  # Ahmed adds 3 copies of "Atomic Habits"
    print("\nAhmed's Shopping Cart after adding items:\n", cart2)

    order2 = Order(customer2, cart2)
    print("\n=== Ahmed's Order Summary ===")
    print(order2.generate_invoice())

    customer3 = Customer("Hamad Almulla", "hamad@example.com", "050-3344556", "789 Desert Rd, Sharjah", "Apple Pay",
                         False)
    print("\n", customer3)

    cart3 = ShoppingCart()
    cart3.add_item(ebook2, 1)  # Hamad adds 1 copy of "The Silent Patient"
    print("\nHamad's Shopping Cart after adding items:\n", cart3)

    order3 = Order(customer3, cart3)
    print("\n=== Hamad's Order Summary ===")
    print(order3.generate_invoice())  # Display Hamad's invoice


if __name__ == "__main__":
    main()  # Execute the main function to simulate customer interactions
