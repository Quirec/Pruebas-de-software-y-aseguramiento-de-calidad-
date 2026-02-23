import unittest
from models.hotel import Hotel


class TestHotel(unittest.TestCase):

    def test_create_hotel(self):
        Hotel.create_hotel(1, "TestHotel", "CDMX", 10)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["name"], "TestHotel")

    def test_modify_hotel(self):
        Hotel.modify_hotel(1, name="UpdatedHotel")
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["name"], "UpdatedHotel")

    def test_delete_hotel(self):
        Hotel.delete_hotel(1)
        hotel = Hotel.display_hotel(1)
        self.assertIsNone(hotel)


