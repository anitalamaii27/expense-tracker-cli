import csv
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
