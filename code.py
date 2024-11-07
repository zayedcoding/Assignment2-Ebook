from datetime import datetime  # Import datetime to record order dates and times


# === Ebook Management ===
class Item:
    """Base class for any store item, representing common attributes like title and price."""

    def __init__(self, title, price):
        # Initialize the item with a title and price
        self.title = title  # Title of the item (e.g., ebook title)
        self.price = price  # Price of the item as a float

    def __str__(self):
        # Returns a string representation of the item
        # Useful for displaying item details in a readable format
        return f"Title: '{self.title}', Price: ${self.price:.2f}"


class Ebook(Item):
    """Represents an Ebook, inheriting properties from Item and adding specific attributes."""

    def __init__(self, title, author, publication_date, genre, price, isbn, publisher, language):
        # Call the parent class (Item) initializer to set title and price
        super().__init__(title, price)
        # Initialize additional attributes unique to an Ebook
        self.author = author  # Author of the ebook
        self.publication_date = publication_date  # Publication date as a string
        self.genre = genre  # Genre or category of the ebook
        self._isbn = isbn  # ISBN (protected), a unique identifier for the book
        self.publisher = publisher  # Publisher of the ebook
        self.language = language  # Language of the ebook content

    def __str__(self):
        # Returns a comprehensive string representation of the Ebook,
        # including author, publisher, language, and price
        return f"Title: '{self.title}', Author: {self.author}, Publisher: {self.publisher}, Language: {self.language}, Price: ${self.price:.2f}"

    def get_isbn(self):
        # Accessor (getter) for the protected ISBN attribute
        # Allows other parts of the program to read the ISBN value safely
        return self._isbn

    def set_isbn(self, isbn):
        # Mutator (setter) for the protected ISBN attribute
        # Allows controlled modification of the ISBN value if needed
        self._isbn = isbn


# === Customer Management ===
class Customer:
    """Represents a customer with personal details and loyalty status."""

    def __init__(self, name, email, contact_number, address, payment_method, loyalty_member=False):
        # Initialize customer details with essential information
        self.name = name  # Customer's full name
        self._email = email  # Email (protected for restricted access)
        self._contact_number = contact_number  # Contact number (protected)
        self.address = address  # Customer's physical address
        self.payment_method = payment_method  # Payment method chosen by the customer
        self.loyalty_member = loyalty_member  # Boolean indicating if the customer is a loyalty program member

    def __str__(self):
        # Returns a formatted string containing customer details
        # Displays loyalty status as "Yes" or "No" based on loyalty_member attribute
        return (f"Customer Name: {self.name}, Contact: {self._email}, Address: {self.address}, "
                f"Payment Method: {self.payment_method}, Loyalty Member: {'Yes' if self.loyalty_member else 'No'}")

    def get_email(self):
        # Accessor for the protected email attribute
        return self._email

    def set_email(self, email):
        # Mutator to update the protected email attribute
        self._email = email

    def get_contact_number(self):
        # Accessor for the protected contact number attribute
        return self._contact_number

    def set_contact_number(self, contact_number):
        # Mutator to update the protected contact number attribute
        self._contact_number = contact_number


# === Shopping Cart Management ===
class ShoppingCart:
    """Manages the eBooks added to the cart and their quantities."""

    def __init__(self):
        # Initialize an empty dictionary to store cart items and quantities
        self.items = {}  # Dictionary where key=ebook instance, value=quantity

    def add_item(self, ebook, quantity=1):
        # Adds an ebook to the cart, or increases quantity if already in cart
        if ebook in self.items:
            # If ebook is already in the cart, increase its quantity
            self.items[ebook] += quantity
        else:
            # If ebook is not in the cart, add it with specified quantity
            self.items[ebook] = quantity
        print(f"Added {ebook.title} - Quantity: {quantity}")  # Confirmation message

    def remove_item(self, ebook, quantity=1):
        # Removes a specified quantity of an ebook from the cart
        if ebook in self.items:
            # If ebook is found in the cart, decrease its quantity
            self.items[ebook] -= quantity
            if self.items[ebook] <= 0:
                # If quantity reaches zero or below, remove item completely
                del self.items[ebook]
            print(f"Removed {quantity} of {ebook.title}")  # Confirmation message
        else:
            # If ebook is not in the cart, display a message
            print(f"{ebook.title} not in cart.")

    def __str__(self):
        # Returns a formatted string listing all ebooks and their quantities in the cart
        # Each line displays the ebook title and quantity in the cart
        return "\n".join(f"{ebook.title} - Quantity: {quantity}" for ebook, quantity in self.items.items())


# === Discount Management ===
class Discount:
    """Handles application of discounts based on loyalty status or bulk purchases."""

    def __init__(self):
        # Set discount rates for loyalty members and bulk purchases
        self.loyalty_discount = 0.1  # Loyalty member discount (10%)
        self.bulk_discount = 0.2     # Bulk purchase discount (20% if 5 or more items)

    def apply_discount(self, subtotal, is_loyalty_member, bulk_quantity):
        # Calculate total discount based on loyalty status and bulk quantity
        discount = 0  # Start with no discount
        if is_loyalty_member:
            # Apply loyalty discount if customer is a member
            discount += subtotal * self.loyalty_discount
        if bulk_quantity >= 5:
            # Apply bulk discount if cart has 5 or more items
            discount += subtotal * self.bulk_discount
        return discount  # Return the total calculated discount


# === Order Processing ===
class Order:
    """Processes an order with customer details, applies discounts, calculates taxes, and generates an invoice."""

    def __init__(self, customer, shopping_cart):
        # Initialize the order with customer and shopping cart instances
        self.customer = customer  # Customer who placed the order
        self.shopping_cart = shopping_cart  # ShoppingCart instance containing the ordered items
        self.order_date = datetime.now()  # Record the date and time of order creation
        self.discount = Discount()  # Discount instance to manage discount calculations
        self.vat_rate = 0.08  # VAT rate (8%) applied on the discounted subtotal

    def calculate_total(self):
        # Calculate subtotal, discount, VAT, and final total for the order
        # Subtotal is the sum of all items' (price * quantity) in the cart
        subtotal = sum(ebook.price * quantity for ebook, quantity in self.shopping_cart.items.items())
        # Calculate applicable discount based on customer's loyalty status and item quantity
        discount = self.discount.apply_discount(subtotal, self.customer.loyalty_member, len(self.shopping_cart.items))
        # Calculate VAT based on the subtotal after discount
        vat = (subtotal - discount) * self.vat_rate
        # Final total is subtotal after discounts plus VAT
        total = subtotal - discount + vat
        return subtotal, discount, vat, total  # Return all calculated values for invoice

    def generate_invoice(self):
        # Generates a formatted invoice including customer details, itemized purchases, and cost breakdown
        # Calculate subtotal, discount, VAT, and total for display in the invoice
        subtotal, discount, vat, total = self.calculate_total()
        # Start the invoice with customer name and itemized list
        invoice = f"=== Invoice ===\nCustomer Name: {self.customer.name}\n"
        for ebook, quantity in self.shopping_cart.items.items():
            # List each ebook in the cart with quantity and cost
            invoice += f" - {ebook.title} (x{quantity}): ${ebook.price * quantity:.2f}\n"
        # Append the subtotal, discount, VAT, and final total to the invoice
        invoice += f"Subtotal after discounts: ${subtotal - discount:.2f}\n"
        invoice += f"VAT ({self.vat_rate * 100}%): ${vat:.2f}\n"
        invoice += f"Total with VAT: ${total:.2f}\n"
        return invoice  # Return the completed invoice text
