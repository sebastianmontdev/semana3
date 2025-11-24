import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "csvs")
CSV_PATH = os.path.join(CSV_DIR, "artifacts.csv")
HEADER = ["code", "description", "rarity", "status"]
RARITY_OPTIONS = ["Low", "Medium", "High", "Forbidden"]
STATUS_OPTIONS = ["Stored", "Under Study", "Destroyed"]

def ensure_csv_artifacts():
    os.makedirs(CSV_DIR, exist_ok=True)
    if not os.path.isfile(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

def read_all_rows():
    ensure_csv_artifacts()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def write_all_rows(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in HEADER})

def _next_generated_code(rows):
    prefix = "ART"
    nums = []
    for r in rows:
        c = r.get("code", "")
        if c.startswith(prefix):
            tail = c[len(prefix):]
            if tail.isdigit():
                nums.append(int(tail))
    return f"{prefix}{(max(nums) + 1) if nums else 1}"

def register_artifact():
    rows = read_all_rows()
    code = input("Code (leave empty to auto-generate): ").strip()
    if not code:
        code = _next_generated_code(rows)
    else:
        for r in rows:
            if r.get("code", "") == code:
                print("Code already exists.")
                return

    description = input("Description: ").strip()
    print("Rarity options:")
    for i, r in enumerate(RARITY_OPTIONS, start=1):
        print(f"{i} = {r}")
    r_input = input("Select rarity (1-4): ").strip()
    if r_input in ("1","2","3","4"):
        rarity = RARITY_OPTIONS[int(r_input)-1]
    else:
        print("Invalid rarity option.")
        return

    print("Status options:")
    for i, s in enumerate(STATUS_OPTIONS, start=1):
        print(f"{i} = {s}")
    s_input = input("Select status (1-3): ").strip()
    if s_input in ("1","2","3"):
        status = STATUS_OPTIONS[int(s_input)-1]
    else:
        print("Invalid status option.")
        return

    if not code or not description:
        print("Code and description are required.")
        return

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([code, description, rarity, status])

    print(f"Artifact registered with code: {code}")

def list_artifacts():
    rows = read_all_rows()
    if not rows:
        print("No artifacts found.")
        return
    for r in rows:
        t = (r.get("code",""), r.get("description",""), r.get("rarity",""), r.get("status",""))
        print(t)

def find_artifact_by_code():
    code = input("Enter artifact code: ").strip()
    rows = read_all_rows()
    for r in rows:
        if r.get("code","") == code:
            t = (r.get("code",""), r.get("description",""), r.get("rarity",""), r.get("status",""))
            print(t)
            return r
    print("Artifact not found.")
    return None

def classify_by_rarity():
    print("\nRarity mapping:")
    print("  1 = Low")
    print("  2 = Medium")
    print("  3 = High")
    print("  4 = Forbidden\n")
    print("Choice mapping for each rarity:")
    print("  1 = include")
    print("  2 = exclude\n")

    raw = input("Enter pairs separated by commas (e.g. 1=1,2=2,3=1,4=2): ").strip()
    if not raw:
        print("No input provided.")
        return

    parts = [p.strip() for p in raw.split(",") if p.strip()]
    rarities = RARITY_OPTIONS[:]  # ["Low","Medium","High","Forbidden"]
    # default: exclude everything
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

    # ensure csv exists
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

def statistics():
    rows = read_all_rows()
    total = len(rows)
    rarity_counts = {}
    status_counts = {}
    rarity_set = set()
    for r in rows:
        rarity = (r.get("rarity") or "Unknown").strip()
        status = (r.get("status") or "Unknown").strip()
        rarity_set.add(rarity)
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"Total artifacts: {total}")
    print("Artifacts by rarity:")
    for k, v in rarity_counts.items():
        print(f"  {k}: {v}")
    print("Rarity set:", rarity_set)
    print("Status counts:")
    for k, v in status_counts.items():
        print(f"  {k}: {v}")

def delete_artifact():
    code = input("Enter artifact code to delete: ").strip()
    rows = read_all_rows()
    for r in rows:
        if r.get("code","") == code:
            print("A - Remove row permanently")
            print("B - Mark as Destroyed (status = Destroyed)")
            opt = input("Option (A/B): ").strip().upper()
            if opt == "A":
                new_rows = [x for x in rows if x.get("code","") != code]
                write_all_rows(new_rows)
                print("Artifact removed.")
                return
            elif opt == "B":
                r["status"] = "Destroyed"
                write_all_rows(rows)
                print("Artifact marked as Destroyed.")
                return
            else:
                print("Invalid option.")
                return
    print("Artifact not found.")