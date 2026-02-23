from models.loadData import load_data, save_data


HOTELS_FILE = "data/hotels.json"


class Hotel:
    """Hotel class with persistent storage."""

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        self.reservations = []

    @staticmethod
    def create_hotel(hotel_id, name, location, rooms):
        hotels = load_data(HOTELS_FILE)

        hotel = {
            "hotel_id": hotel_id,
            "name": name,
            "location": location,
            "rooms": rooms,
            "reservations": []
        }

        hotels.append(hotel)
        save_data(HOTELS_FILE, hotels)

    @staticmethod
    def delete_hotel(hotel_id):
        hotels = load_data(HOTELS_FILE)
        hotels = [h for h in hotels if h["hotel_id"] != hotel_id]
        save_data(HOTELS_FILE, hotels)

    @staticmethod
    def display_hotel(hotel_id):
        hotels = load_data(HOTELS_FILE)
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        return None

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None, rooms=None):
        hotels = load_data(HOTELS_FILE)
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if name:
                    hotel["name"] = name
                if location:
                    hotel["location"] = location
                if rooms:
                    hotel["rooms"] = rooms
        save_data(HOTELS_FILE, hotels)



