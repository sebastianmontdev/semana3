import csv
import os

def login():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "csvs", "admin_access.csv")

    if not os.path.isfile(csv_path):
        print(f"CSV file not found: {csv_path}")
        return False

    for attempt in range(1, 4):
        print(f"\nAttempt {attempt}/3")

        username_input = input("Username: ").strip()
        password_input = input("Password: ").strip()

        if not username_input or not password_input:
            print("Username and password cannot be empty.")
            continue

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    csv_username = row.get("username", "").strip()
                    csv_password = row.get("password", "").strip()

                    if username_input == csv_username and password_input == csv_password:
                        print("Login successful.")
                        return True

        except Exception as e:
            print("Error reading CSV:", e)
            return False

        print("Invalid username or password.")

    print("\nYou have reached the max amount of tries.")
    return False