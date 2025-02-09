from src.utils import get_coordinates, is_valid_location

class User:
    def __init__(self):
        self.start_point_coordinates = None
        self.target_point_coordinates = None

    def get_user_input(self) -> None:
        print("Welcome to Filter Paths app!")

        while True:
            start_location = input("Enter your current location name! (Add 'Sofia, Bulgaria' at the end): ").strip()

            if not is_valid_location(start_location):
                print("Invalid input. Please enter a valid location name using only letters and numbers, but not only numbers.")
                continue

            self.start_point_coordinates = get_coordinates(start_location)

            if self.start_point_coordinates is None:
                print(f"Could not find coordinates for '{start_location}'. Please try again with a more precise location.")
                continue
            else:
                break

        while True:
            target_location = input("Enter your target location name! (Add 'Sofia, Bulgaria' at the end): ").strip()

            if not is_valid_location(target_location):
                print("Invalid input. Please enter a valid location name using only letters and numbers, but not only numbers.")
                continue

            self.target_point_coordinates = get_coordinates(target_location)

            if self.target_point_coordinates is None:
                print(f"Could not find coordinates for '{target_location}'. Please try again with a more precise location.")
                continue
            else:
                break
