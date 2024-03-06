import datetime
import sys
import math

class Product:
    product_id = 0
    def __init__(self,name, description ,quantity, price):
        Product.product_id += 1
        self.id = Product.product_id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.first_added = InputTemplate.time()
        self.last_updated = InputTemplate.time()


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
        utc_time = datetime.datetime.now(datetime.UTC)
        ist_offset = datetime.timedelta(hours=IST_offset_hours, minutes=IST_offset_minutes)
        ist_time = utc_time + ist_offset
        return ist_time.strftime("%d-%m-%Y %H:%M")

        

class Sale:
    sale_id = 0
    def __init__(self, customer, total_cost=0, discount=0, bill_cost=0):
        Sale.sale_id += 1
        self.id = Sale.sale_id
        self.date = InputTemplate.time()
        self.customer = customer
        self.total_cost = total_cost
        self.discount = discount
        self.bill_cost = bill_cost
        self.products = []
    
    def change_customer(self, new_customer):
        print("The old customer of this sale was: {}".format(self.customer.name))
        customer_id = InputTemplate.get_int_input("Enter customer new ID: ","Oops! Invalid input")
        if not customer_id:return
        self.customer = new_customer
    
        
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
        

class SaleDetails:
    def __init__(self, id, sale, product, quantity, cost):
        self.id = id
        self.sale = sale
        self.product = product
        self.quantity = quantity
        self.cost = cost


class Customer:
    customer_id = 0
    def __init__(self, name, phone):
        Customer.customer_id += 1
        self.id = Customer.customer_id
        self.name = name
        self.phone = phone
        self.first_added = InputTemplate.time()

class Shop:
    def __init__(self,name="Groove"):
        self.products = dict()
        self.sales = dict()
        self.customers = dict()
        self.name = name
    
    def add_customer(self):
        name = input("Enter customer name: ")
        if len(name) < 3:
            print("Customer name too short")
        phone = InputTemplate.get_int_input("Enter customer phone number: ","Oops! Input must be a integer")
        if not phone:
            return
        new_customer = Customer(name, phone)
        self.customers[new_customer.id] = new_customer
        print("New customer created")
        
    def display_customer(self):
        if len(self.customers)==0:
            print("No customers available")
            return False
        print("\nCustomers List:")
        for customer in self.customers.values():
            print(f"ID: {customer.id} - Name: {customer.name} - Phone: {customer.phone}")    
        return True
        
    def remove_customer(self):
        if not self.display_customer():
            return
        customer_id = InputTemplate.get_int_input("Enter customer ID to remove: ","Oops! Input must be a integer")
        if not customer_id or customer_id not in self.customers:
            print(f"Customer with ID {customer_id} not found")
            return
        print("Customer data removed")
        del self.customers[customer_id]
        
        
    def add_product(self):
        name = input("Enter product name: ")
        description = input("Enter product description or leave it empty: ")
        quantity = InputTemplate.get_int_input("Enter product quantity: ","Oops! Input must be a integer")
        if not quantity:
            return
        price = InputTemplate.get_float_input("Enter product price in decimal: ","Oops! Input must be a integer or decimal")
        if not price:
            return
        new_product = Product(name, description, quantity, price)
        self.products[new_product.id] = new_product
        print("New product has been added!")
        
    def display_product(self):
        if len(self.products)==0:
            print("No products available!")
            return False
        
        for product in self.products.values():
            print(f"ID: {product.id} - Name: {product.name} - Quabtity: {product.quantity} - Price: {product.price}")
        return True
    
    def remove_product(self):
        if not self.display_product():
            return
        product_id = InputTemplate.get_int_input("Enter product id to removed: ","Product id must be integer")
        if not product_id:
            return
        if product_id not in self.products:
            print(f"Product with ID {product_id} , Not Found")
            return
        del self.products[product_id]
        print("Product has been removed")

    def make_sale(self):
        if len(self.products)==0:
            print("No products available to buy")
            return
        if len(self.customers)==0:
            print("No customer available to make a sale, please add new customer")
            return
        
        customer_id = InputTemplate.get_int_input("Enter customer ID: ")
        if customer_id not in self.customers:
            print(f"No customer found with ID {customer_id}")
            return
        customer = self.customers[customer_id]
        cart = dict()
        while True:
            product_id = InputTemplate.get_int_input("Enter product ID: ")
            if product_id==-1:
                print("Sale aborted!")
                return
            if product_id not in self.products or self.products[product_id].quantity==0:
                print(f"Product with ID {product_id} not found")
                continue
            product = self.products[product_id]
            quantity = InputTemplate.get_int_input(f"Enter quantity between 1 - {product.quantity}: ")
            if quantity<0 or product.quantity<quantity:
                print("Invalid quantity")
                continue
            print("Added to cart")
            cart[product] = quantity
            choice = input("Wanted to add product? yes/no: ")
            if choice.lower() != 'yes' and choice.lower() != 'y':
                break
        total_cost = 0
        
        new_sale = Sale(customer)
        self.sales[new_sale.id] = new_sale
        index = 0
        for product,quantity  in cart.items():
            price = quantity*product.price
            total_cost += price
            product.quantity = product.quantity-quantity
            new_sale.products.append(SaleDetails(index+1, new_sale, product, quantity,price))
            index += 1
        new_sale.total_cost = total_cost
        get_discount = (total_cost*self.discount_calculator(customer))//100
        new_sale.discount = get_discount
        new_sale.bill_cost = total_cost-get_discount
        new_sale.print_bill()
    
    def print_bill_receipt(self):
        bill_number = InputTemplate.get_int_input(f"Enter bill number: ")
        if not bill_number:
            return
        if bill_number not in self.sales:
            print(f"No sales found with ID {bill_number}")
            return
        self.sales[bill_number].print_bill()
    
    def sale_history(self):
        if len(self.sales) == 0:
            print("No sales history available")
            return
        for sale in self.sales.values():
            print(f"Sale ID: {sale.id} - No of Products: {len(sale.products)} - Total: {sale.total_cost} - Discound: {sale.discount} - Billed Price: {sale.bill_cost}")
        
    def discount_calculator(self,customer):
        total_purchase = 0
        no_of_purchase = 0
        discount = 0
        for sale in self.sales.values():
            if sale.customer == customer:
                total_purchase += sale.bill_cost
                no_of_purchase += 1
        discount = (total_purchase/1000)
        discount += (no_of_purchase/10)
        return math.ceil(min(discount, 15))
    



        

def display_options():
    print("""
    1) Add product
    2) Remove product
    3) Display products
    4) Add customer
    5) delete Customer
    6) Display Customer
    7) Make Sale
    8) Print Bill
    9) Sales History
    """)

def choose_option(shop):
    try:
        choice = int(input("Enter your choice: "))
    except:
        print("Invalid input")
        choice = False
        return
    
    choices = {
        1:shop.add_product,
        2:shop.remove_product,
        3:shop.display_product,
        4:shop.add_customer,
        5:shop.remove_customer,
        6:shop.display_customer,
        7:shop.make_sale,
        8:shop.print_bill_receipt,
        9:shop.sale_history
    }
    
    return choices.get(choice, False)
    

def main():
    shop = Shop()
    print(f"Welcome to {shop.name}\n")
    print("There will be no more customer and products available\nAdd some data and using the below options\n")
    while True:
        choice = choose_option(shop)
        if not choice:
            print("Stopping program")
            sys.exit()
        else:
            choice()
        print()

if __name__ == '__main__':
    main()
