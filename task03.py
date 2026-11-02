import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

# Create CSV file if it does not exist
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])


# Add expense
def add_expense():
    print("\n===== ADD EXPENSE =====")

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
        category = input("Enter category (Food/Travel/Shopping/Bills): ")
        description = input("Enter description: ")
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

        with open(FILE_NAME, "r", newline="") as file:
            expenses = list(csv.reader(file))
            expense_id = len(expenses)

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                expense_id, date, category, description, amount
            ])

        print("\nExpense added successfully!")

    except ValueError:
        print("Invalid date or amount!")


# View all expenses
def view_expenses():
    print("\n===== ALL EXPENSES =====")

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)

        found = False

        for row in reader:
            if row:
                print(
                    f"ID: {row[0]} | Date: {row[1]} | "
                    f"Category: {row[2]} | Description: {row[3]} | "
                    f"Amount: Rs. {float(row[4]):.2f}"
                )
                found = True

        if not found:
            print("No expenses found.")


# Calculate total expenses
def total_expenses():
    total = 0

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += float(row["Amount"])

    print("\nTotal Expenses: Rs.", round(total, 2))


# Search by category
def search_category():
    category = input("\nEnter category to search: ").strip().lower()
    found = False

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        print("\n===== SEARCH RESULTS =====")

        for row in reader:
            if row["Category"].lower() == category:
                print(row)
                found = True

    if not found:
        print("No expenses found in this category.")


# Monthly expense report
def monthly_report():
    month = input("Enter month (YYYY-MM): ")
    total = 0
    found = False

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format!")
        return

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                total += float(row["Amount"])
                found = True

    print("\n===== MONTHLY REPORT =====")

    if found:
        print("Month:", month)
        print("Total Expenses: Rs.", round(total, 2))
    else:
        print("No expenses found for this month.")


# Delete expense
def delete_expense():
    expense_id = input("Enter expense ID to delete: ")

    with open(FILE_NAME, "r", newline="") as file:
        rows = list(csv.DictReader(file))

    new_rows = [row for row in rows if row["ID"] != expense_id]

    if len(new_rows) == len(rows):
        print("Expense ID not found!")
        return

    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["ID", "Date", "Category", "Description", "Amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)

    print("Expense deleted successfully!")


# Main program
create_file()

while True:

    print("\n================================")
    print("     PERSONAL EXPENSE TRACKER")
    print("================================")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Total Expenses")
    print("4. Search by Category")
    print("5. Monthly Report")
    print("6. Delete Expense")
    print("7. Exit")

    choice = input("\nEnter your choice (1-7): ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        total_expenses()

    elif choice == "4":
        search_category()

    elif choice == "5":
        monthly_report()

    elif choice == "6":
        delete_expense()

    elif choice == "7":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice! Please try again.")