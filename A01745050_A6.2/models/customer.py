from models.loadData import load_data, save_data


CUSTOMERS_FILE = "data/customers.json"


class Customer:
    """Customer class with persistent storage."""

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @staticmethod
    def create_customer(customer_id, name, email):
        customers = load_data(CUSTOMERS_FILE)

        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email
        }

        customers.append(customer)
        save_data(CUSTOMERS_FILE, customers)

    @staticmethod
    def delete_customer(customer_id):
        customers = load_data(CUSTOMERS_FILE)
        customers = [
            c for c in customers if c["customer_id"] != customer_id
        ]
        save_data(CUSTOMERS_FILE, customers)

    @staticmethod
    def display_customer(customer_id):
        customers = load_data(CUSTOMERS_FILE)
        for customer in customers:
            if customer["customer_id"] == customer_id:
                return customer
        return None

    @staticmethod
    def modify_customer(customer_id, name=None, email=None):
        customers = load_data(CUSTOMERS_FILE)
        for customer in customers:
            if customer["customer_id"] == customer_id:
                if name:
                    customer["name"] = name
                if email:
                    customer["email"] = email
        save_data(CUSTOMERS_FILE, customers)


