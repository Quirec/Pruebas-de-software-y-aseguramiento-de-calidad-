import json
import os


def load_data(filename):
    """Load JSON data from file. Handle invalid data."""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as error:
        print(f"Error loading file {filename}: {error}")
        return []


def save_data(filename, data):
    """Save JSON data to file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except IOError as error:
        print(f"Error saving file {filename}: {error}")


