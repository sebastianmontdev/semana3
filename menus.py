from auth import *
from visitors import *
from artifacts import *

def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Visitors menu")
        print("2. Artifacts menu")
        print("0. Logout")

        option = input("Select an option: ").strip()

        if not option.isdigit():
            print("Invalid input.")
            continue

        match option:
            case "1":
                visitors_menu()
            case "2":
                artifacts_menu()
            case "0":
                main_menu()
                break
            case _:
                print("Invalid option.")

def visitors_menu():
    ensure_csv()
    while True:
        print("\n=== Visitors Menu ===")
        print("1. Register visitor")
        print("2. List visitors")
        print("3. Find visitor by ID")
        print("4. Update visitor status")
        print("5. Delete visitor")
        print("6. Statistics")
        print("0. Back")
        opt = input("Select an option: ").strip()
        if not opt.isdigit():
            print("Invalid input.")
            continue
        match opt:
            case "1":
                register_visitor()
            case "2":
                list_visitors()
            case "3":
                find_visitor_by_id()
            case "4":
                update_visitor_status()
            case "5":
                delete_visitor()
            case "6":
                statistics_visitors()
            case "0":
                break
            case _:
                print("Invalid option.")

def classify_by_rarity_numeric():
    print("\nFilter artifacts by rarity using pairs:")
    print("Format: rarity_index=choice, ...")
    print("rarity_index: 1=Low, 2=Medium, 3=High, 4=Forbidden")
    print("choice: 1=include, 2=exclude")
    print("Example: 1=1,2=2,3=1,4=2  (include Low & High only)\n")

    raw = input("Enter pairs: ").strip()
    if not raw:
        print("No input provided.")
        return

    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        print("No valid pairs found.")
        return

    rarities = RARITY_OPTIONS[:]  # ["Low","Medium","High","Forbidden"]
    filters = {r: False for r in rarities}

    for part in parts:
        if "=" not in part:
            print(f"Invalid pair '{part}'. Expected format i=j")
            return
        left, right = part.split("=", 1)
        left = left.strip()
        right = right.strip() 
        
        if not left.isdigit() or not right.isdigit():
            print(f"Invalid numbers in pair '{part}'. Use digits only.")
            return
        idx = int(left)
        opt = right
        if idx < 1 or idx > 4:
            print(f"Invalid rarity index '{idx}' in pair '{part}'. Must be 1-4.")
            return
        if opt not in ("1", "2"):
            print(f"Invalid option '{opt}' in pair '{part}'. Use 1 (include) or 2 (exclude).")
            return
        filters[rarities[idx - 1]] = (opt == "1")

    ensure_csv_artifacts()
    filtered = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rarity = (row.get("rarity") or "").strip()
            if rarity in filters and filters[rarity]:
                filtered.append(row)

    print("\nFiltered results:")
    if not filtered:
        print("No artifacts match the selected criteria.")
        return

    for r in filtered:
        t = (r.get("code", ""), r.get("description", ""), r.get("rarity", ""), r.get("status", ""))
        print(t)


def artifacts_menu():
    ensure_csv_artifacts()
    while True:
        print("\n=== Artifacts Menu ===")
        print("1. Register artifact")
        print("2. List artifacts")
        print("3. Find artifact by code")
        print("4. Classify artifacts by rarity")
        print("5. Statistics")
        print("6. Delete artifact")
        print("0. Back")
        opt = input("Select an option: ").strip()
        if not opt.isdigit():
            print("Invalid input.")
            continue
        match opt:
            case "1":
                register_artifact()
            case "2":
                list_artifacts()
            case "3":
                find_artifact_by_code()
            case "4":
                classify_by_rarity_numeric()
            case "5":
                statistics()
            case "6":
                delete_artifact()
            case "0":
                break
            case _:
                print("Invalid option.")

def main_menu():
    while True:
        print("\nWelcome to Galactic Library")
        print("1. Login")
        print("0. Exit")

        option = input("Select an option: ").strip()

        if not option.isdigit():
            print("Invalid input.")
            continue

        match option:
            case "1":
                if login():
                    admin_menu()
                break
            case "0":
                print("Goodbye!")
                break
            case _:
                print("Invalid option.")

if __name__ == "__main__":
    main_menu()