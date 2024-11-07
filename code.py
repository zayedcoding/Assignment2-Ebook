from datetime import datetime


# === Ebook Management ===
class Item:
    """Base class for any store item, representing common attributes like title and price."""

    def __init__(self, title, price):
        # Initializing title and price for an item
        self.title = title
        self.price = price

    def __str__(self):
        # Returns a formatted string representation of the item
        return f"Title: '{self.title}', Price: ${self.price:.2f}"


class Ebook(Item):
    """Represents an Ebook, inheriting properties from Item and adding specific attributes."""

    def __init__(self, title, author, publication_date, genre, price, isbn, publisher, language):
        # Initialize the base class (Item) attributes
        super().__init__(title, price)
        # Additional ebook-specific attributes
        self.author = author
        self.publication_date = publication_date
        self.genre = genre
        self._isbn = isbn  # ISBN is a protected attribute
        self.publisher = publisher
        self.language = language

    def __str__(self):
        # Returns a detailed string representation of the Ebook
        return f"Title: '{self.title}', Author: {self.author}, Publisher: {self.publisher}, Language: {self.language}, Price: ${self.price:.2f}"

    def get_isbn(self):
        # Accessor for the protected ISBN attribute
        return self._isbn

    def set_isbn(self, isbn):
        # Mutator for the protected ISBN attribute, allowing it to be updated
        self._isbn = isbn


# === Customer Management ===
class Customer:
    """Represents a customer with personal and loyalty details."""

    def __init__(self, name, email, contact_number, address, payment_method, loyalty_member=False):
        # Initializing customer details
        self.name = name
        self._email = email  # Email is protected to restrict direct access
        self._contact_number = contact_number  # Contact number is protected
        self.address = address
        self.payment_method = payment_method
        self.loyalty_member = loyalty_member  # Boolean to check if customer is a loyalty member

    def __str__(self):
        # Returns a formatted string with customer details
        return (f"Customer Name: {self.name}, Contact: {self._email}, Address: {self.address}, "
                f"Payment Method: {self.payment_method}, Loyalty Member: {'Yes' if self.loyalty_member else 'No'}")

    def get_email(self):
        # Accessor for protected email attribute
        return self._email

    def set_email(self, email):
        # Mutator for protected email attribute
        self._email = email

    def get_contact_number(self):
        # Accessor for protected contact number attribute
        return self._contact_number

    def set_contact_number(self, contact_number):
        # Mutator for protected contact number attribute
        self._contact_number = contact_number


# === Shopping Cart Management ===
class ShoppingCart:
    """Manages the eBooks added to the cart and their quantities."""

    def __init__(self):
        # Initializes an empty dictionary to store items and their quantities
        self.items = {}

    def add_item(self, ebook, quantity=1):
        # Adds an ebook to the cart or updates quantity if already present
        if ebook in self.items:
            self.items[ebook] += quantity  # Increase quantity for existing item
        else:
            self.items[ebook] = quantity  # Add new item with specified quantity
        print(f"Added {ebook.title} - Quantity: {quantity}")

    def remove_item(self, ebook, quantity=1):
        # Removes specified quantity of an ebook from the cart
        if ebook in self.items:
            self.items[ebook] -= quantity  # Decrease quantity
            if self.items[ebook] <= 0:
                del self.items[ebook]  # Remove item if quantity is zero or less
            print(f"Removed {quantity} of {ebook.title}")
        else:
            print(f"{ebook.title} not in cart.")

    def __str__(self):
        # Returns a string representation of all items and quantities in the cart
        return "\n".join(f"{ebook.title} - Quantity: {quantity}" for ebook, quantity in self.items.items())


# === Discount Management ===
class Discount:
    """Manages discount policies, including loyalty and bulk discounts."""

    def __init__(self):
        # Setting fixed discount rates for loyalty and bulk purchases
        self.loyalty_discount = 0.1  # 10% discount for loyalty members
        self.bulk_discount = 0.2     # 20% discount for bulk purchases (quantity >= 5)

    def apply_discount(self, subtotal, is_loyalty_member, bulk_quantity):
        # Calculates total discount based on membership and quantity
        discount = 0
        if is_loyalty_member:
            discount += subtotal * self.loyalty_discount  # Apply loyalty discount
        if bulk_quantity >= 5:
            discount += subtotal * self.bulk_discount  # Apply bulk discount if quantity threshold is met
        return discount  # Return calculated discount amount


# === Order Processing ===
class Order:
    """Handles an order with customer details, cart items, and applies discounts."""

    def __init__(self, customer, shopping_cart):
        # Composes Order with customer and shopping cart details
        self.customer = customer  # Customer instance
        self.shopping_cart = shopping_cart  # ShoppingCart instance with all items
        self.order_date = datetime.now()  # Order timestamp
        self.discount = Discount()  # Discount instance for applying discounts
        self.vat_rate = 0.08  # VAT rate (8%)

    def calculate_total(self):
        # Calculates the total order cost, including discounts and VAT
        subtotal = sum(ebook.price * quantity for ebook, quantity in self.shopping_cart.items.items())
        discount = self.discount.apply_discount(subtotal, self.customer.loyalty_member, len(self.shopping_cart.items))
        vat = (subtotal - discount) * self.vat_rate  # Calculate VAT on the discounted subtotal
        total = subtotal - discount + vat  # Final total after applying discount and VAT
        return subtotal, discount, vat, total

    def generate_invoice(self):
        # Generates and returns a formatted invoice with all details
        subtotal, discount, vat, total = self.calculate_total()
        invoice = f"=== Invoice ===\nCustomer Name: {self.customer.name}\n"
        for ebook, quantity in self.shopping_cart.items.items():
            invoice += f" - {ebook.title} (x{quantity}): ${ebook.price * quantity:.2f}\n"
        invoice += f"Subtotal after discounts: ${subtotal - discount:.2f}\nVAT ({self.vat_rate * 100}%): ${vat:.2f}\nTotal with VAT: ${total:.2f}\n"
        return invoice
