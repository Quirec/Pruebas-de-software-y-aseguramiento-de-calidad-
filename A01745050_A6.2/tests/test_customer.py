import os
import unittest
from models.customer import Customer

CUSTOMERS_FILE = "data/customers.json"


class TestCustomer(unittest.TestCase):

    def setUp(self):
        """Reset file before each test."""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as file:
            file.write("[]")

    def test_create_customer(self):
        Customer.create_customer(1, "Juan", "juan@test.com")
        customer = Customer.display_customer(1)

        self.assertIsNotNone(customer)
        self.assertEqual(customer["name"], "Juan")
        self.assertEqual(customer["email"], "juan@test.com")

    def test_modify_customer(self):
        Customer.create_customer(2, "Ana", "ana@test.com")
        Customer.modify_customer(2, name="Ana Maria")

        customer = Customer.display_customer(2)
        self.assertEqual(customer["name"], "Ana Maria")

    def test_delete_customer(self):
        Customer.create_customer(3, "Luis", "luis@test.com")
        Customer.delete_customer(3)

        customer = Customer.display_customer(3)
        self.assertIsNone(customer)

    def test_display_nonexistent_customer(self):
        customer = Customer.display_customer(999)
        self.assertIsNone(customer)

    def test_modify_nonexistent_customer(self):
        # No debe lanzar error
        Customer.modify_customer(999, name="Ghost")
        customer = Customer.display_customer(999)
        self.assertIsNone(customer)


