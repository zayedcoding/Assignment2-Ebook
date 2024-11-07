from datetime import datetime

# === Ebook Management ===
class Item:
    """Base class for any store item."""
    def __init__(self, title, price):
        self.title = title
        self.price = price
    
    def __str__(self):
        return f"Title: '{self.title}', Price: ${self.price:.2f}"

class Ebook(Item):
    """Represents an Ebook, inheriting from Item."""
    def __init__(self, title, author, publication_date, genre, price, isbn, publisher, language):
        super().__init__(title, price)
        self.author = author
        self.publication_date = publication_date
        self.genre = genre
        self._isbn = isbn
        self.publisher = publisher
        self.language = language

    def __str__(self):
        return f"Title: '{self.title}', Author: {self.author}, Publisher: {self.publisher}, Language: {self.language}, Price: ${self.price:.2f}"

    def get_isbn(self):
        return self._isbn

    def set_isbn(self, isbn):
        self._isbn = isbn


# === Customer Management ===
class Customer:
    """Manages customer details and loyalty status."""
    def __init__(self, name, email, contact_number, address, payment_method, loyalty_member=False):
        self.name = name
        self._email = email
        self._contact_number = contact_number
        self.address = address
        self.payment_method = payment_method
        self.loyalty_member = loyalty_member

    def __str__(self):
        return (f"Customer Name: {self.name}, Contact: {self._email}, Address: {self.address}, "
                f"Payment Method: {self.payment_method}, Loyalty Member: {'Yes' if self.loyalty_member else 'No'}")

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_contact_number(self):
        return self._contact_number

    def set_contact_number(self, contact_number):
        self._contact_number = contact_number


# === Shopping Cart Management ===
class ShoppingCart:
    """Aggregates eBooks and manages shopping cart items."""
    def __init__(self):
        self.items = {}

    def add_item(self, ebook, quantity=1):
        if ebook in self.items:
            self.items[ebook] += quantity
        else:
            self.items[ebook] = quantity
        print(f"Added {ebook.title} - Quantity: {quantity}")

    def remove_item(self, ebook, quantity=1):
        if ebook in self.items:
            self.items[ebook] -= quantity
            if self.items[ebook] <= 0:
                del self.items[ebook]
            print(f"Removed {quantity} of {ebook.title}")
        else:
            print(f"{ebook.title} not in cart.")

    def __str__(self):
        return "\n".join(f"{ebook.title} - Quantity: {quantity}" for ebook, quantity in self.items.items())


# === Discount Management ===
class Discount:
    """Handles discount logic."""
    def __init__(self):
        self.loyalty_discount = 0.1
        self.bulk_discount = 0.2

    def apply_discount(self, subtotal, is_loyalty_member, bulk_quantity):
        discount = 0
        if is_loyalty_member:
            discount += subtotal * self.loyalty_discount
        if bulk_quantity >= 5:
            discount += subtotal * self.bulk_discount
        return discount


# === Order Processing ===
class Order:
    """Composition of customer, shopping cart, and discount."""
    def __init__(self, customer, shopping_cart):
        self.customer = customer  # Composition
        self.shopping_cart = shopping_cart  # Aggregation
        self.order_date = datetime.now()
        self.discount = Discount()  # Composition
        self.vat_rate = 0.08

    def calculate_total(self):
        subtotal = sum(ebook.price * quantity for ebook, quantity in self.shopping_cart.items.items())
        discount = self.discount.apply_discount(subtotal, self.customer.loyalty_member, len(self.shopping_cart.items))
        vat = (subtotal - discount) * self.vat_rate
        total = subtotal - discount + vat
        return subtotal, discount, vat, total

    def generate_invoice(self):
        subtotal, discount, vat, total = self.calculate_total()
        invoice = f"=== Invoice ===\nCustomer Name: {self.customer.name}\n"
        for ebook, quantity in self.shopping_cart.items.items():
            invoice += f" - {ebook.title} (x{quantity}): ${ebook.price * quantity:.2f}\n"
        invoice += f"Subtotal after discounts: ${subtotal - discount:.2f}\nVAT ({self.vat_rate*100}%): ${vat:.2f}\nTotal with VAT: ${total:.2f}\n"
        return invoice


# === Main Program with Separate Customer Outputs ===
def main():
    # E-books available
    ebook1 = Ebook("Atomic Habits", "James Clear", "2018", "Self-help", 29.99, "12345", "Penguin", "English")
    ebook2 = Ebook("The Silent Patient", "Alex Michaelides", "2019", "Thriller", 49.99, "54321", "Celadon", "English")
    
    # Zayed's Section
    customer1 = Customer("Zayed Alblooshi", "zayed@example.com", "050-1234567", "123 Palm St, Dubai", "Credit Card", True)
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
    customer2 = Customer("Ahmed Almansoori", "ahmed@example.com", "050-1112233", "456 Oasis St, Abu Dhabi", "Debit Card", True)
    print("\n", customer2)
    
    cart2 = ShoppingCart()
    cart2.add_item(ebook1, 3)
    print("\nAhmed's Shopping Cart after adding items:\n", cart2)

    order2 = Order(customer2, cart2)
    print("\n=== Ahmed's Order Summary ===")
    print(order2.generate_invoice())

    # Hamad's Section
    customer3 = Customer("Hamad Almulla", "hamad@example.com", "050-3344556", "789 Desert Rd, Sharjah", "Apple Pay", False)
    print("\n", customer3)
    
    cart3 = ShoppingCart()
    cart3.add_item(ebook2, 1)
    print("\nHamad's Shopping Cart after adding items:\n", cart3)

    order3 = Order(customer3, cart3)
    print("\n=== Hamad's Order Summary ===")
    print(order3.generate_invoice())

if __name__ == "__main__":
    main()

