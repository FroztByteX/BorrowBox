# BorrowBox
# Final Project Prototype

from datetime import date

"""=========================
            DATA
========================="""

equipment = [
    {
        "id": "EQ001",
        "name": "Projector",
        "category": "Electronics",
        "quantity": 3,
        "available": 3
    },
    {
        "id": "EQ002",
        "name": "Camera",
        "category": "Photography",
        "quantity": 2,
        "available": 2
    },
    {
        "id": "EQ003",
        "name": "Tripod",
        "category": "Accessories",
        "quantity": 5,
        "available": 5
    }
]

borrow_records = []

"""=========================
      DISPLAY FUNCTIONS
========================="""


def display_title(title):
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def display_menu():
    display_title("BorrowBOX")
    print("[1] View Equipments\n"
          "[2] Add Equipment\n"
          "[3] Search Equipment\n"
          "[4] Borrow Equipment\n"
          "[5] Return Equipment\n"
          "[6] View Borrowing Records\n"
          "[7] Dashboard\n"
          "[8] EXIT")
    print("=" * 60)


"""=========================
    VALIDATION FUNCTIONS
========================="""


def validate_quantity(prompt):
    while True:
        try:
            value = int(input(prompt).strip())

            if value < 0:
                print("[X]INVALID INPUT: Please enter a positive integer.")
            else:
                return value
            
        except ValueError:
            print("[X]INVALID INPUT: Please enter a whole number.")



def find_equipment(equipment_id):
    for item in equipment:
        if item["id"].lower() == equipment_id.lower():
            return item

    return None


def find_transaction(transaction_id):
    for record in borrow_records:
        if record["transaction_id"].lower() == transaction_id.lower():
            return record

    return None


def generate_transaction_id():
    number = len(borrow_records) + 1
    transaction_id = f"BR{number:03d}"

    # Prevents duplicate IDs if records were removed in the future
    while find_transaction(transaction_id) is not None:
        number += 1
        transaction_id = f"BR{number:03d}"

    return transaction_id


"""=========================
    EQUIPMENT MANAGEMENT
========================="""


def view_equipment():
    display_title("EQUIPMENT LIST")

    if not equipment:
        print(f"{'[No equipment available]':^60}")
        return

    print(f"{'ID':<10}"
          f"{'NAME':<20}"
          f"{'CATEGORY':<18}"
          f"{'TOTAL':<8}"
          f"{'AVAILABLE':<10}")

    print("-" * 66)

    for item in equipment:
        print(f"{item['id']:<10}"
              f"{item['name']:<20}"
              f"{item['category']:<18}"
              f"{item['quantity']:<8}"
              f"{item['available']:<10}")

    print("=" * 66)


def add_equipment():
    display_title("ADD EQUIPMENT")

    while True:
        equipment_id = input("Equipment ID: ").strip().upper()

        if not equipment_id:
            print(f"{'[X]Equipment ID cannot be empty.':^60}")
        elif find_equipment(equipment_id):
            print(f"{'[X]ERROR: Equipment ID already exists.':^60}")
        else:
            break

    while True:
        name = input("Equipment Name: ").strip()

        if name: break
        print(f"{'[X]Equipment name cannot be empty.':^60}")

    while True:
        category = input("Category: ").strip()

        if category: break
        print(f"{'[X]Category cannot be empty.':^60}")

    quantity = validate_quantity("Quantity: ")

    new_equipment = {
        "id": equipment_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "available": quantity
    }

    equipment.append(new_equipment)

    print(f"{'[Equipment ADDED successfully!]':^60}")
    print(f"Equipment ID: {equipment_id}\n"
          f"Equipment Name: {name}\n"
          f"Quantity: {quantity}")


def search_equipment():
    display_title("SEARCH EQUIPMENT")

    while True:
        keyword = input("Enter equipment ID, name, or category: ").strip().lower()

        if not keyword:
            print(f"{'[X]Search input cannot be empty.':^60}")
            continue

        break

    results = []

    for item in equipment:
        if (keyword in item['id'].lower()
                or keyword in item['name'].lower()
                or keyword in item['category'].lower()):
            results.append(item)

    if not results:
        print(f"{'[No equipment found.]':^60}")
        return

    print("\n SEARCH RESULTS:")
    print("-" * 60)

    for item in results:
        status = "Available" if item['available'] > 0 else "Borrowed"

        print(f"ID\t\t: {item['id']}\n"
              f"Name\t\t: {item['name']}\n"
              f"Category\t: {item['category']}\n"
              f"Quantity\t: {item['quantity']}\n"
              f"Available\t: {item['available']}\n"
              f"Status\t\t: {status}")
        print("-" * 60)


"""=========================
    BORROWING MANAGEMENT
========================="""


def borrow_equipment():
    display_title("BORROW EQUIPMENT")

    equipment_id = input("Equipment ID: ")
    item = find_equipment(equipment_id)

    if item is None:
        print(f"{'[Equipment not found.]':^60}")
        return

    print(f"Equipment: {item['name']}\n"
          f"Category: {item['category']}\n"
          f"Available Quantity: {item['available']}")

    if item['available'] == 0:
        print(f"{'[This equipment is currently unavailable.]':^60}")
        return

    quantity = validate_quantity("Quantity to borrow: ")

    if quantity > item['available']:
        print(f"{'[Insufficient equipment]':^60}")
        print(f"Only {item['available']} item(s) are available.")
        return

    while True:
        borrower = input("Borrower Name: ")

        if not borrower:
            print(f"{'[X]Borrower name cannot be empty.':^60}")
            continue
        break

    transaction_id = generate_transaction_id()
    item['available'] -= quantity

    record = {
        "transaction_id": transaction_id,
        "equipment_id": item['id'],
        "equipment_name": item['name'],
        "borrower": borrower,
        "quantity": quantity,
        "date_borrowed": str(date.today()),
        "date_returned": None,
        "status": "Borrowed"
    }

    borrow_records.append(record)

    display_title("BORROWING SUCCESSFUL")
    print(f"Transaction ID\t\t: {transaction_id}\n"
          f"Equipment\t\t: {item['name']}\n"
          f"Quantity\t\t: {quantity}\n"
          f"Borrower\t\t: {borrower}\n"
          f"Date Borrowed\t\t: {record['date_borrowed']}\n"
          f"Status\t\t\t: {record['status']}")
    print("=" * 60)


def return_equipment():
    display_title("RETURN EQUIPMENT")
    transaction_id = input("Transaction ID: ").strip()
    record = find_transaction(transaction_id)

    if record is None:
        print(f"{'[Transaction not found.]':^60}")
        return

    if record['status'] == "Returned":
        print(f"{'[This equipment has already been returned.]':^60}")
        return

    item = find_equipment(record['equipment_id'])

    if item is None:
        print(f"{'[The equipment associated with this transaction no longer exists.]':^60}")
        return

    print(f"\nTransaction ID\t\t: {record['transaction_id']}\n"
          f"Equipment\t\t: {record['equipment_name']}\n"
          f"Borrower\t\t: {record['borrower']}\n"
          f"Quantity\t\t: {record['quantity']}\n"
          f"Date Borrowed\t\t: {record['date_borrowed']}\n"
          f"Status\t\t\t: {record['status']}")

    while True:
        confirmation = input("\nReturn this equipment? (Y/N): ").strip().upper()

        if confirmation == "Y":
            break
        elif confirmation == "N":
            print(f"{'[Return cancelled]':^60}")
            return
        else:
            print(f"{'[X]INVALID CHOICE: Please enter Y or N.':^60}")

    item['available'] += record['quantity']
    record['date_returned'] = str(date.today())
    record['status'] = "Returned"

    print(f"{'[Equipment RETURNED successfully!]':^60}")
    print(f"Equipment: {item['name']}\n"
          f"Available Quantity: {item['available']}")


def view_records():
    display_title("BORROWING RECORDS")

    if not borrow_records:
        print(f"{'[No borrowing records found.]':^60}")
        return

    print(f"{'ID':<10}"
          f"{'EQUIPMENT':<18}"
          f"{'BORROWER':<18}"
          f"{'QTY':<6}"
          f"{'STATUS':<12}")

    print("=" * 64)

    for record in borrow_records:
        print(f"{record['transaction_id']:<10}"
              f"{record['equipment_name']:<18}"
              f"{record['borrower']:<18}"
              f"{record['quantity']:<6}"
              f"{record['status']:<12}")

    print("=" * 64)

"""=========================
        DASHBOARD
========================="""

def dashboard():
    display_title("BORROWBOX DASHBOARD")
    
    total_equipment = sum(item['quantity'] for item in equipment)
    available_equipment = sum(item['available'] for item in equipment)
    borrowed_equipment = total_equipment - available_equipment
    
    active_transactions = 0
    completed_transactions = 0
    
    for record in borrow_records:
        if record['status'] == "Borrowed":
            active_transactions += 1
        elif record['status'] == "Returned":
            completed_transactions += 1

    print(f"Total Equipment Units\t: {total_equipment}")
    print(f"Available Units\t\t: {available_equipment}")
    print(f"Borrowed Units\t\t: {borrowed_equipment}")
    print(f"Active Transactions\t: {active_transactions}")
    print(f"Completed Transactions\t: {completed_transactions}")

"""=========================
        MAIN
========================="""

def main():
    while True:
        display_menu()

        while True:
            try:
                choice = int(input("Enter choice: "))

                if choice == 1:
                    view_equipment()
                elif choice == 2:
                    add_equipment()
                elif choice == 3:
                    search_equipment()
                elif choice == 4:
                    borrow_equipment()
                elif choice == 5:
                    return_equipment()
                elif choice == 6:
                    view_records()
                elif choice == 7:
                    dashboard()
                elif choice == 8:
                    display_title("[Thank you for using BorrowBOX!]")
                    return
                else:
                    print("[X]INVALID CHOICE: Choose a number from 1 to 8.")
                    continue

                print("=" * 60)
                input("Press 'Enter' to go back to the main menu...")
                break

            except ValueError:
                print("[X]INVALID INPUT: Please enter a numeric value.")


if __name__ == "__main__":
    main()