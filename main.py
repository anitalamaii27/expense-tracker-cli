import csv
import os
from datetime import datetime
import pandas as pd

# Colored text (for visual flair)
try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    Fore = Style = lambda x: ""

CSV_FILE = 'expenses.csv'
monthly_budget = None
yearly_budget = None

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["date", "description", "amount"])
            writer.writeheader()

def read_expenses():
    with open(CSV_FILE, 'r') as file:
        return list(csv.DictReader(file))

def write_expenses(expenses):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["date", "description", "amount"])
        writer.writeheader()
        writer.writerows(expenses)

def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    description = input("Enter description: ").strip()
    amount = input("Enter amount: ").strip()

    expenses = read_expenses()
    expenses.append({"date": date, "description": description, "amount": amount})
    write_expenses(expenses)
    print(Fore.GREEN + "✅ Expense added successfully!\n" + Style.RESET_ALL)

def view_expenses():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded.")
        return

    print(f"\n{Fore.CYAN}{'Index':<6}{'Date':<12}{'Description':<30}{'Amount':>10}{Style.RESET_ALL}")
    print("-" * 60)
    for i, exp in enumerate(expenses):
        print(f"{i:<6}{exp['date']:<12}{exp['description']:<30}{exp['amount']:>10}")
    print()

def delete_expense():
    view_expenses()
    index = int(input("Enter the index of the expense to delete: "))
    expenses = read_expenses()
    if 0 <= index < len(expenses):
        del expenses[index]
        write_expenses(expenses)
        print(Fore.RED + "❌ Expense deleted." + Style.RESET_ALL)
    else:
        print("Invalid index.")

def export_csv():
    expenses = read_expenses()
    filename = input("Enter export filename (e.g., 'my_expenses.csv'): ").strip()
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["date", "description", "amount"])
        writer.writeheader()
        writer.writerows(expenses)
    print(Fore.GREEN + f"✅ Exported to {filename}\n" + Style.RESET_ALL)

def monthly_summary():
    expenses = pd.read_csv(CSV_FILE)
    expenses['date'] = pd.to_datetime(expenses['date'])
    expenses['amount'] = pd.to_numeric(expenses['amount'])

    month = datetime.today().strftime('%Y-%m')
    current_month_expenses = expenses[expenses['date'].dt.strftime('%Y-%m') == month]
    total = current_month_expenses['amount'].sum()

    print(f"\n📆 {Fore.MAGENTA}Monthly Summary - {month}{Style.RESET_ALL}")
    print(f"Total spent: {Fore.YELLOW}${total:.2f}{Style.RESET_ALL}")
    if monthly_budget:
        print(f"Budget: ${monthly_budget:.2f}")
        print(f"{'Remaining:' if total <= monthly_budget else 'Over budget by:'} {Fore.GREEN if total <= monthly_budget else Fore.RED}${abs(monthly_budget - total):.2f}{Style.RESET_ALL}")

def yearly_summary():
    expenses = pd.read_csv(CSV_FILE)
    expenses['date'] = pd.to_datetime(expenses['date'])
    expenses['amount'] = pd.to_numeric(expenses['amount'])

    year = datetime.today().year
    this_year = expenses[expenses['date'].dt.year == year]
    total = this_year['amount'].sum()

    print(f"\n📅 {Fore.MAGENTA}Yearly Summary - {year}{Style.RESET_ALL}")
    print(f"Total spent: {Fore.YELLOW}${total:.2f}{Style.RESET_ALL}")
    if yearly_budget:
        print(f"Budget: ${yearly_budget:.2f}")
        print(f"{'Remaining:' if total <= yearly_budget else 'Over budget by:'} {Fore.GREEN if total <= yearly_budget else Fore.RED}${abs(yearly_budget - total):.2f}{Style.RESET_ALL}")

def set_budgets():
    global monthly_budget, yearly_budget
    try:
        monthly_budget_input = input("Set a monthly budget (or leave blank): ").strip()
        yearly_budget_input = input("Set a yearly budget (or leave blank): ").strip()
        if monthly_budget_input:
            monthly_budget = float(monthly_budget_input)
        if yearly_budget_input:
            yearly_budget = float(yearly_budget_input)
    except ValueError:
        print("Invalid input. Budgets not set.")

def main():
    init_csv()
    print(Fore.CYAN + "\n📘 Welcome to the Python CLI Expense Tracker\n" + Style.RESET_ALL)
    set_budgets()

    while True:
        print(Fore.BLUE + "\n==== Main Menu ====" + Style.RESET_ALL)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary")
        print("5. Yearly Summary")
        print("6. Export to CSV")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            monthly_summary()
        elif choice == '5':
            yearly_summary()
        elif choice == '6':
            export_csv()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
