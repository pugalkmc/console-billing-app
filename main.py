from datetime import datetime

class Product:
    product_id = 0
    def __init__(self,name, description ,quantity, price):
        self.product_id += 1
        self.id = self.product_id
        self._name = name
        self._description = description
        self._quantity = quantity
        self._price = price
        self.first_added = datetime.now()
        self.last_updated = datetime.now()
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,val):
        if len(val)<2:
            print("Name length too short")
            return
        self.name = val
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, val):
        if len(val)<3:
            print("Description length too short")
            return
        self._description = val
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, val):
        if val<0:
            print("Quantity cannot be negative")
            return
        self._quanitity = val
    
    @property
    def price(self):
        return self._price
        
    @price.setter
    def price(self, val):
        if val<0:
            print('Product price cannot be negative')
            return
        self._price = val


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
        

class Sale:
    sale_id = 0
    def __init__(self, customer, total_cost=0, discount=0, bill_cost=0):
        self.sale_id += 1
        self.id = self.sale_id
        self.date = datetime.now()
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
    
    @property
    def products(self):
        return self.products
    
    @products.setter
    def product(self, products_list):
        self.products = products_list
        
    def print_bill(self):
        print("------------Sale Details-----------")
        print(f"Date: {self.date}                        Sale ID: {self.id}")
        print(f"_______________________________________________________________")
        print(f"  ID  |   Product Name  | Quantity | Cost |")
        print(f"_______________________________________________________________")
        for product in self.products:
            print(f"{product.id.center(6)}|{product.product.name.center(17)}|{str(self.product.quantity).center(10)}|{str(self.cost).center(7)}")
            print(f"_______________________________________________________________")
        print(f"                                Total Cost: {self.total_cost}")
        print(f"                                Discount: {self.discount}")
        print(f"                                Bill Cost: {self.bill_cost}")
        

class SaleDetails:
    def __init__(self, id, sale, product, quantity, price, shop):
        self.id
        self.sale = sale
        self.product = product
        self.quantity = quantity
        self.price = price
        self.shop = shop


class Customer:
    customer_id = 0
    def __init__(self, name, phone, first_added):
        self.customer_id += 1
        self.id = customer_id
        self.name = name
        self.phone = phone
        self.first_added = datetime.now()

class Shop:
    def __init__(self, shop_name="Groove"):
        self.products = dict()
        self.sales = dict()
        self.customers = dict()
        self.shop_name = shop_name
    
    def add_customer(self):
        name = input("Enter product name: ")
        if len(name) < 3:
            print("Customer name too short")
        phone = InputTemplate.get_int_input("Enter customer phone number: ","Oops! Input must be a integer")
        if not phone:
            return
        new_customer = Customer(name, phone)
        self.customers[new_customer.id] = new_customer
        print("New customer created")
        
    def remove_customer(self):
        if self.len(customers)==0:
            print("No customers available to remove")
            return
        for customer in self.customers:
            print(f"ID: {customer.id} - Name: {customer.name} - Phone")
        customer_id = InputTemplate.get_int_input("Enter customer ID: ","Oops! Input must be a integer")
        
        
    def add_product(self):
        name = input("Enter product name: ")
        description = input("Enter product description or leave it empty: ")
        quantity = InputTemplate.get_int_input("Enter product quantity","Oops! Input must be a integer")
        if not quantity:
            return
        price = InputTemplate.get_float_input("Enter product price in decimal: ","Oops! Input must be a integer or decimal")
        if not price:
            return
        new_product = Product(name, description, quantity, price)
        self.products[new_product.id] = new_product
        print("New product has been added!")
    
    def remove_product(self):
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
        
        customer_id = InputTemplate.get_int_input("Enter customer ID")
        if customer_id not in self.customers:
            print(f"No customer found with ID {customer_id}")
        customer = self.customers[customer_id]
        
        cart = dict()
        while True:
            product_id = InputTemplate.get_int_input("Enter product ID")
            if product_id not in self.products or self.products[product_id].quantity==0:
                print(f"Product with ID {product_id} not found")
                continue
            product = self.products[product_id]
            quantity = InputTemplate.get_int_input(f"Enter quantity between 1 - {product.quantity}")
            if quantity<0 or product.quantity<quantity:
                print("Invalid quantity")
                continue
            print("Added to cart")
            cart[product] = quantity
            choice = InputTemplate.get_int_input("Wanted to add product? yes/no")
            if choice.lower() != 'yes' or choice.lower()!='y':
                break
        total_cost = 0
        
        new_sale = Sale(customer)
        self.sale.append(new_sale)
        for index,product,quantity  in enumerate(cart.items()):
            price = quantity*product.price
            total_cost += price
            product.quantity = product.quantity-quantity
            new_sale.products.append(SaleDetails(index+1, new_sale, product, quantity,price))
        new_sale.total_cost = total_cost
        new_sale.disocunt = 0
        new_sale.bill_cost = total_cost
        new_sale.print_bill()
    
groove = Shop()
groove.add_product()
groove.remove_product()
groove.make_sale()
print()
