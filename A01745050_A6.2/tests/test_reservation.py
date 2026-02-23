import unittest
from models.hotel import Hotel
from models.customer import Customer
from models.reservation import Reservation
from models.loadData import load_data

HOTELS_FILE = "data/hotels.json"
CUSTOMERS_FILE = "data/customers.json"
RESERVATIONS_FILE = "data/reservations.json"


class TestReservation(unittest.TestCase):

    def setUp(self):
        """Reset all files before each test."""
        for file in [HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE]:
            with open(file, "w", encoding="utf-8") as f:
                f.write("[]")

        Hotel.create_hotel(1, "HotelTest", "CDMX", 2)
        Customer.create_customer(1, "Juan", "juan@test.com")

    def test_create_reservation(self):
        Reservation.create_reservation(1, 1, 1)

        reservations = load_data(RESERVATIONS_FILE)
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0]["customer_id"], 1)

    def test_cancel_reservation(self):
        Reservation.create_reservation(2, 1, 1)
        Reservation.cancel_reservation(2)

        reservations = load_data(RESERVATIONS_FILE)
        self.assertEqual(len(reservations), 0)

    def test_no_rooms_available(self):
        Reservation.create_reservation(3, 1, 1)
        Reservation.create_reservation(4, 1, 1)

        # Este debería fallar porque solo hay 2 habitaciones
        Reservation.create_reservation(5, 1, 1)

        reservations = load_data(RESERVATIONS_FILE)
        self.assertEqual(len(reservations), 2)

    def test_hotel_not_found(self):
        # No debe crashear
        Reservation.create_reservation(6, 1, 999)

        reservations = load_data(RESERVATIONS_FILE)
        self.assertEqual(len(reservations), 0)

    def test_cancel_nonexistent_reservation(self):
        # No debe lanzar error
        Reservation.cancel_reservation(999)

        reservations = load_data(RESERVATIONS_FILE)
        self.assertEqual(len(reservations), 0)



