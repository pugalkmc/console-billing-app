import datetime
import sys
import math

class Product:
    product_id = 0
    products = {}
    
    def __init__(self, name, description, quantity, price):
        Product.product_id += 1
        self.id = Product.product_id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.first_added = InputTemplate.time()
        self.last_updated = InputTemplate.time()
        Product.products[self.id] = self  # Maintain product within Product class

    @classmethod
    def display_products(cls):
        if not cls.products:
            print("No products available!")
            return False
        
        print("Products List:")
        for product in cls.products.values():
            print(f"ID: {product.id} - Name: {product.name} - Quantity: {product.quantity} - Price: {product.price}")
        return True

    @classmethod
    def remove_product(cls, product_id):
        if product_id in cls.products:
            del cls.products[product_id]
            print("Product has been removed")
        else:
            print(f"Product with ID {product_id} not found")


class InputTemplate:
    @staticmethod
    def get_int_input(text="Enter input", error="Enter correct input"):
        try:
            return int(input(text))
        except:
            print(error)
            return False
    
    @staticmethod
    def get_float_input(text="Enter float number: ", error="Oops! Enter correct input"):
        try:
            return float(input(text))
        except:
            print(error)
            return False

    @staticmethod
    def time():
        IST_offset_hours = 5
        IST_offset_minutes = 30
        utc_time = datetime.datetime.now()
        ist_offset = datetime.timedelta(hours=IST_offset_hours, minutes=IST_offset_minutes)
        ist_time = utc_time + ist_offset
        return ist_time.strftime("%d-%m-%Y %H:%M")


class Customer:
    customer_id = 0
    customers = {}
    
    def __init__(self, name, phone):
        Customer.customer_id += 1
        self.id = Customer.customer_id
        self.name = name
        self.phone = phone
        self.first_added = InputTemplate.time()
        Customer.customers[self.id] = self  # Maintain customer within Customer class

    @classmethod
    def display_customers(cls):
        if not cls.customers:
            print("No customers available")
            return False
        print("Customer List:")
        for customer in cls.customers.values():
            print(f"ID: {customer.id} - Name: {customer.name} - Phone: {customer.phone}")
        return True

    @classmethod
    def remove_customer(cls, customer_id):
        if customer_id in cls.customers:
            del cls.customers[customer_id]
            print("Customer data removed")
        else:
            print(f"Customer with ID {customer_id} not found")


class Sale:
    sale_id = 0
    sales = {}
    
    def __init__(self, customer, total_cost=0, discount=0, bill_cost=0):
        Sale.sale_id += 1
        self.id = Sale.sale_id
        self.date = InputTemplate.time()
        self.customer = customer
        self.total_cost = total_cost
        self.discount = discount
        self.bill_cost = bill_cost
        self.products = []
        Sale.sales[self.id] = self  # Maintain sale within Sale class

    def print_bill(self):
        print("-----------------Sale Details---------------")
        print(f"Date: {self.date}           Sale ID: {self.id}")
        print(f"___________________________________________")
        print(f"  ID  |   Product Name  | Quantity | Cost |")
        print(f"___________________________________________")
        for product in self.products:
            print(f"{str(product.id).center(6)}|{product.product.name.center(17)}|{str(product.quantity).center(10)}|{str(product.cost).center(7)}")
            print(f"________________________________________")
        print(f"                         Total Cost: {self.total_cost}")
        print(f"                         Discount: {self.discount}")
        print(f"                         Bill Cost: {self.bill_cost}")

    @classmethod
    def print_sale_history(cls):
        if not cls.sales:
            print("No sales history available")
            return
        print("Sales History:")
        for sale in cls.sales.values():
            print(f"Sale ID: {sale.id} - No of Products: {len(sale.products)} - Total: {sale.total_cost} - Discount: {sale.discount} - Billed Price: {sale.bill_cost}")


class SaleDetails:
    def __init__(self, id, sale, product, quantity, cost):
        self.id = id
        self.sale = sale
        self.product = product
        self.quantity = quantity
        self.cost = cost


class Shop:
    def __init__(self, name="Groove"):
        self.name = name

    def add_customer(self):
        name = input("Enter customer name: ")
        if len(name) < 3:
            print("Customer name too short")
        phone = InputTemplate.get_int_input("Enter customer phone number: ", "Oops! Input must be an integer")
        if phone:
            new_customer = Customer(name, phone)
            print("New customer created")

    def add_product(self):
        name = input("Enter product name: ")
        description = input("Enter product description or leave it empty: ")
        quantity = InputTemplate.get_int_input("Enter product quantity: ", "Oops! Input must be an integer")
        price = InputTemplate.get_float_input("Enter product price in decimal: ", "Oops! Input must be a number")
        if quantity and price:
            new_product = Product(name, description, quantity, price)
            print("New product has been added!")

    def make_sale(self):
        if not Product.display_products():
            print("No products available to buy")
            return
        if not Customer.display_customers():
            print("No customers available to make a sale, please add a new customer")
            return
        customer_id = InputTemplate.get_int_input("Enter customer ID: ")
        customer = Customer.customers.get(customer_id)
        if not customer:
            print(f"No customer found with ID {customer_id}")
            return

        cart = {}
        while True:
            product_id = InputTemplate.get_int_input("Enter product ID: ")
            if product_id == -1:
                print("Sale aborted!")
                return
            product = Product.products.get(product_id)
            if not product or product.quantity == 0:
                print(f"Product with ID {product_id} not found or out of stock")
                continue
            quantity = InputTemplate.get_int_input(f"Enter quantity (1-{product.quantity}): ")
            if quantity < 1 or product.quantity < quantity:
                print("Invalid quantity")
                continue
            print("Added to cart")
            cart[product] = quantity
            if input("Want to add more products? yes/no: ").lower() not in ['yes', 'y']:
                break

        new_sale = Sale(customer)
        total_cost = sum(quantity * product.price for product, quantity in cart.items())
        new_sale.total_cost = total_cost
        discount = total_cost * self.discount_calculator(customer) // 100
        new_sale.discount = discount
        new_sale.bill_cost = total_cost - discount

        for index, (product, quantity) in enumerate(cart.items()):
            product.quantity -= quantity
            new_sale.products.append(SaleDetails(index + 1, new_sale, product, quantity, quantity * product.price))

        new_sale.print_bill()

    def discount_calculator(self, customer):
        total_purchase = sum(sale.bill_cost for sale in Sale.sales.values() if sale.customer == customer)
        no_of_purchase = sum(1 for sale in Sale.sales.values() if sale.customer == customer)
        discount = total_purchase / 1000 + no_of_purchase / 10
        return math.ceil(min(discount, 15))


def display_options():
    print("""
    1) Add product
    2) Remove product
    3) Display products
    4) Add customer
    5) Delete customer
    6) Display customers
    7) Make sale
    8) Print sale history
    """)


def choose_option(shop):
    choice = InputTemplate.get_int_input("Enter your choice: ")
    if choice is False:
        print("Invalid input")
        return False

    actions = {
        1: shop.add_product,
        2: lambda: Product.remove_product(InputTemplate.get_int_input("Enter product ID to remove: ")),
        3: Product.display_products,
        4: shop.add_customer,
        5: lambda: Customer.remove_customer(InputTemplate.get_int_input("Enter customer ID to remove: ")),
        6: Customer.display_customers,
        7: shop.make_sale,
        8: Sale.print_sale_history
    }

    action = actions.get(choice, False)
    if action:
        action()
    else:
        print("Invalid option selected, exiting the billing app")
        sys.exit()


def main():
    shop = Shop()
    print(f"Welcome to {shop.name}")
    print("There will be no products and customer available in the shop initially, please add them.")
    while True:
        display_options()
        choose_option(shop)


if __name__ == '__main__':
    main()