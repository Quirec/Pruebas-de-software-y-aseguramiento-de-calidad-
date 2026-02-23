from models.loadData import load_data, save_data


RESERVATIONS_FILE = "data/reservations.json"
HOTELS_FILE = "data/hotels.json"


class Reservation:
    """Reservation class with persistent storage."""

    @staticmethod
    def create_reservation(reservation_id, customer_id, hotel_id):
        reservations = load_data(RESERVATIONS_FILE)
        hotels = load_data(HOTELS_FILE)

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["rooms"] <= len(hotel["reservations"]):
                    print("No rooms available")
                    return

                reservation = {
                    "reservation_id": reservation_id,
                    "customer_id": customer_id,
                    "hotel_id": hotel_id
                }

                reservations.append(reservation)
                hotel["reservations"].append(reservation_id)

                save_data(RESERVATIONS_FILE, reservations)
                save_data(HOTELS_FILE, hotels)
                return

        print("Hotel not found")

    @staticmethod
    def cancel_reservation(reservation_id):
        reservations = load_data(RESERVATIONS_FILE)
        hotels = load_data(HOTELS_FILE)

        reservations = [
            r for r in reservations
            if r["reservation_id"] != reservation_id
        ]

        for hotel in hotels:
            if reservation_id in hotel["reservations"]:
                hotel["reservations"].remove(reservation_id)

        save_data(RESERVATIONS_FILE, reservations)
        save_data(HOTELS_FILE, hotels)



