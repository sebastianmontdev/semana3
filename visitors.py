import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "csvs", "visitors.csv")
HEADER = ["id", "name", "species", "status"]

def ensure_csv():
    if not os.path.isdir(os.path.join(BASE_DIR, "csvs")):
        os.makedirs(os.path.join(BASE_DIR, "csvs"), exist_ok=True)
    if not os.path.isfile(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

def read_all_rows():
    ensure_csv()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def write_all_rows(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in HEADER})

def register_visitor():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "csvs", "visitors.csv")

    name = input("Name: ").strip()

    print("Species options:")
    print("1 = human")
    print("2 = android")
    print("3 = other")

    species_input = input("Select species: ").strip()

    if species_input == "1":
        species = "human"
    elif species_input == "2":
        species = "android"
    elif species_input == "3":
        species = input("Enter species: ").strip()
    else:
        print("Invalid species option.")
        return

    status_input = input("Status (1 = active, 2 = retired): ").strip()

    if status_input == "1":
        status = "active"
    elif status_input == "2":
        status = "retired"
    else:
        print("Invalid status option.")
        return

    if not name or not species:
        print("All fields are required.")
        return

    new_id = 1
    if os.path.isfile(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row["id"]) for row in reader if row.get("id", "").isdigit()]
            if ids:
                new_id = max(ids) + 1

    write_header = not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0

    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow(["id", "name", "species", "status"])

        writer.writerow([new_id, name, species, status])

    print(f"Visitor registered with ID: {new_id}")

def list_visitors():
    rows = read_all_rows()
    tuples = []
    for r in rows:
        t = (r.get("id", ""), r.get("name", ""), r.get("species", ""), r.get("status", ""))
        tuples.append(t)
    if not tuples:
        print("No visitors found.")
        return
    for t in tuples:
        print(t)

def find_visitor_by_id():
    vid = input("Enter visitor ID: ").strip()
    rows = read_all_rows()
    for r in rows:
        if r.get("id", "") == vid:
            t = (r.get("id", ""), r.get("name", ""), r.get("species", ""), r.get("status", ""))
            print(t)
            return r
    print("Visitor not found.")
    return None

def update_visitor_status():
    vid = input("Enter visitor ID to update status: ").strip()
    rows = read_all_rows()
    found = False
    for r in rows:
        if r.get("id", "") == vid:
            found = True
            current = r.get("status", "").lower()
            if current == "active":
                new = "retired"
            elif current == "retired":
                new = "active"
            else:
                choice = input("Current status is not active/retired. Set to (1) active or (2) retired: ").strip()
                if choice == "1":
                    new = "active"
                elif choice == "2":
                    new = "retired"
                else:
                    print("Invalid option. Aborting.")
                    return
            r["status"] = new
            break
    if not found:
        print("Visitor not found.")
        return
    write_all_rows(rows)
    print("Status updated.")

def delete_visitor():
    vid = input("Enter visitor ID to delete: ").strip()
    rows = read_all_rows()
    for r in rows:
        if r.get("id", "") == vid:
            print("Choose delete option:")
            print("A - Remove row permanently")
            print("B - Mark as deleted (status = deleted)")
            opt = input("Option (A/B): ").strip().upper()
            if opt == "A":
                new_rows = [x for x in rows if x.get("id", "") != vid]
                write_all_rows(new_rows)
                print("Visitor removed.")
                return
            elif opt == "B":
                r["status"] = "deleted"
                write_all_rows(rows)
                print("Visitor marked as deleted.")
                return
            else:
                print("Invalid option. Aborting.")
                return
    print("Visitor not found.")

def statistics_visitors():
    rows = read_all_rows()
    total = 0
    species_counts = {}
    species_set = set()
    status_counts = {"active": 0, "retired": 0, "deleted": 0, "other": 0}
    for r in rows:
        status = (r.get("status") or "").lower()
        if status == "deleted":
            status_counts["deleted"] += 1
            continue
        total += 1
        species = (r.get("species") or "").lower()
        if not species:
            species = "unknown"
        species_set.add(species)
        species_counts[species] = species_counts.get(species, 0) + 1
        if status == "active":
            status_counts["active"] += 1
        elif status == "retired":
            status_counts["retired"] += 1
        else:
            status_counts["other"] += 1
    print(f"Total visitors (excluding deleted): {total}")
    print("Visitors by species:")
    for sp, cnt in species_counts.items():
        print(f"  {sp}: {cnt}")
    print("Species set:", species_set)
    print("Active vs Retired vs Other:")
    print(f"  Active: {status_counts['active']}")
    print(f"  Retired: {status_counts['retired']}")
    print(f"  Deleted: {status_counts['deleted']}")
    print(f"  Other: {status_counts['other']}")