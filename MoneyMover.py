import tkinter as tk
from tkinter import Menu, messagebox, Listbox, Scrollbar, SINGLE, END, Radiobutton, StringVar, simpledialog
import json
from datetime import datetime  # Import datetime module
import csv
from tkinter import filedialog
from fpdf import FPDF
import matplotlib.pyplot as plt


class AccountingApp:
    def __init__(self, root):
        # Initialize the application
        self.root = root
        root.title("Accounting Tool")

        # Initialize balance and transactions
        self.balance = 0.0
        self.transactions = []

        # Initialize currency
        self.currency_symbol = "$"  # Default currency is the dollar sign

        # Create Labels
        self.balance_label = tk.Label(root, text=f"Balance: {self.currency_symbol}0.00", font=("Helvetica", 18))
        self.balance_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="n")

        self.income_label = tk.Label(root, text=f"Income: {self.currency_symbol}0.00", font=("Helvetica", 14))
        self.income_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        self.expenses_label = tk.Label(root, text=f"Expenses: {self.currency_symbol}0.00", font=("Helvetica", 14))
        self.expenses_label.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="n")

        # Create Entry Fields
        self.amount_label = tk.Label(root, text="Amount:", font=("Helvetica", 12))
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.description_label = tk.Label(root, text="Description:", font=("Helvetica", 12))
        self.description_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create Radio Buttons for Income and Expense
        self.transaction_type_var = StringVar()
        self.transaction_type_var.set("Income")  # Default selection
        self.income_radio = Radiobutton(root, text="Income", variable=self.transaction_type_var, value="Income", font=("Helvetica", 12))
        self.income_radio.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.expense_radio = Radiobutton(root, text="Expense", variable=self.transaction_type_var, value="Expense", font=("Helvetica", 12))
        self.expense_radio.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Create Category Dropdown
        self.categories = ["Groceries", "Utilities", "Entertainment", "Salary", "Rent",  "Transportation", "Healthcare", "Education", "Shopping", "Dining", "Travel" , "Others"]

        self.category_label = tk.Label(root, text="Category:", font=("Helvetica", 12))
        self.category_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0])
        self.category_dropdown = tk.OptionMenu(root, self.category_var, *self.categories)
        self.category_dropdown.grid(row=4, column=1, padx=10, pady=10)

        # Create Date Entry
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):", font=("Helvetica", 12))
        self.date_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=5, column=1, padx=10, pady=10)

        # Create Buttons
        self.add_transaction_button = tk.Button(root, text="Add Transaction", command=self.add_transaction, font=("Helvetica", 12))
        self.add_transaction_button.grid(row=6, column=1, padx=10, pady=10)

        # Create Menu Bar
        menubar = Menu(root)
        root.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_transactions)
        file_menu.add_command(label="Load", command=self.load_transactions)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
                 
                # Create View Menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Add "Graphical Representation" option
        view_menu.add_command(label="Graphical Representation", command=self.generate_graphical_representation)
        
        # Add a separator
        view_menu.add_separator()
        
        # Sorting Submenu
        sorting_menu = Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Transaction Sorting", menu=sorting_menu)
        sorting_menu.add_command(label="Sort by Date (Ascending)", command=self.sort_transactions_by_date_asc)
        sorting_menu.add_command(label="Sort by Date (Descending)", command=self.sort_transactions_by_date_desc)
        sorting_menu.add_command(label="Sort by Amount (Ascending)", command=self.sort_transactions_by_amount_asc)
        sorting_menu.add_command(label="Sort by Amount (Descending)", command=self.sort_transactions_by_amount_desc)
        
        # Filtering Submenu
        filtering_menu = Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Transaction Filtering", menu=filtering_menu)
        filtering_menu.add_command(label="Filter by Category", command=self.filter_transactions_by_category)
        

        # Transactions Menu
        transactions_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="Show Transactions", command=self.show_all_transactions)
        transactions_menu.add_command(label="Clear All Transactions", command=self.clear_all_transactions)
        transactions_menu.add_command(label="Calculate Income and Expenses", command=self.calculate_income_expenses)
        transactions_menu.add_separator()
        transactions_menu.add_command(label="Search by Category", command=self.search_transactions_by_category)
        transactions_menu.add_command(label="Delete Selected Transaction", command=self.delete_selected_transaction)

        # Currency Menu
        currency_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Currency", menu=currency_menu)
        currency_menu.add_command(label="Change Currency Symbol", command=self.change_currency_symbol)
        currency_menu.add_separator()
        currency_menu.add_command(label="Convert to New Currency", command=self.convert_to_new_currency)
        
        # Export Menu
        export_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Export", menu=export_menu)
        export_menu.add_command(label="Export Reports as CSV", command=self.export_reports_csv)
        export_menu.add_command(label="Export Reports as PDF", command=self.export_reports_pdf)

        # Create Transactions Listbox and Scrollbar
        self.transactions_listbox = Listbox(root, selectmode=SINGLE, width=50, height=10)
        self.transactions_listbox.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        scrollbar = Scrollbar(root, orient="vertical")
        scrollbar.config(command=self.transactions_listbox.yview)
        scrollbar.grid(row=7, column=3, sticky="ns")
        self.transactions_listbox.config(yscrollcommand=scrollbar.set)

    def add_transaction(self):
        # Add a transaction with user input
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get()
            transaction_type = self.transaction_type_var.get()
            date_str = self.date_entry.get()
            
            # Convert date string to a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            if transaction_type == "Expense":
                amount = -amount  # Convert to negative for expenses

            self.balance += amount
            self.transactions.append({"Amount": amount, "Category": category, "Description": description, "Date": date_obj})
            self.update_balance_label()
            
            # Clear input fields
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount or date in YYYY-MM-DD format.")

    def update_balance_label(self):
        # Update the balance label
        self.balance_label.config(text=f"Balance: {self.currency_symbol}{self.balance:.2f}")

    def save_transactions(self):
        # Save transactions to a JSON file
        data = {
            "balance": self.balance,
            "transactions": self.transactions
        }
        with open("transactions.json", "w") as file:
            json.dump(data, file)
        messagebox.showinfo("Save", "Transactions saved successfully.")

    def load_transactions(self):
        # Load transactions from a JSON file
        try:
            with open("transactions.json", "r") as file:
                data = json.load(file)
                self.balance = data["balance"]
                self.transactions = data["transactions"]
                self.update_balance_label()
                messagebox.showinfo("Load", "Transactions loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved transactions found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load transactions. File format is incorrect.")

    def show_all_transactions(self):
        # Display all stored transactions in the listbox
        self.transactions_listbox.delete(0, END)
        for transaction in self.transactions:
            self.transactions_listbox.insert(END, f"Date: {transaction['Date'].strftime('%Y-%m-%d')}, Amount: {self.currency_symbol}{transaction['Amount']:.2f}, Category: {transaction['Category']}, Description: {transaction['Description']}")

    def calculate_income_expenses(self):
        # Calculate and display income and expenses
        income = sum(transaction['Amount'] for transaction in self.transactions if transaction['Amount'] > 0)
        expenses = sum(transaction['Amount'] for transaction in self.transactions if transaction['Amount'] < 0)

        self.income_label.config(text=f"Income: {self.currency_symbol}{income:.2f}")
        self.expenses_label.config(text=f"Expenses: {self.currency_symbol}{-expenses:.2f}")

    def clear_all_transactions(self):
        # Clear all stored transactions
        self.balance = 0.0
        self.transactions = []
        self.update_balance_label()
        self.income_label.config(text=f"Income: {self.currency_symbol}0.00")
        self.expenses_label.config(text=f"Expenses: {self.currency_symbol}0.00")
        self.transactions_listbox.delete(0, END)
        messagebox.showinfo("Clear Transactions", "All transactions have been cleared.")

    def search_transactions_by_category(self):
        # Search and display transactions by selected category
        selected_category = self.category_var.get()
        self.transactions_listbox.delete(0, END)
        for transaction in self.transactions:
            if transaction['Category'] == selected_category:
                self.transactions_listbox.insert(END, f"Date: {transaction['Date'].strftime('%Y-%m-%d')}, Amount: {self.currency_symbol}{transaction['Amount']:.2f}, Category: {transaction['Category']}, Description: {transaction['Description']}")

    def delete_selected_transaction(self):
        # Delete the selected transaction from the listbox and transactions list
        selected_index = self.transactions_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            deleted_transaction = self.transactions.pop(index)
            self.balance -= deleted_transaction['Amount']
            self.update_balance_label()
            self.transactions_listbox.delete(index)
            messagebox.showinfo("Delete Transaction", "Transaction deleted successfully.")
        else:
            messagebox.showerror("Error", "No transaction selected.")

    def change_currency_symbol(self):
        # Change the currency symbol
        new_symbol = simpledialog.askstring("Change Currency Symbol", "Enter a new currency symbol:")
        if new_symbol:
            self.currency_symbol = new_symbol
            self.update_balance_label()
            self.calculate_income_expenses()

    def convert_to_new_currency(self):
        # Convert all transaction amounts to a new currency
        new_currency = simpledialog.askstring("Convert to New Currency", "Enter a new currency symbol:")
        if new_currency:
            conversion_rate = simpledialog.askfloat("Convert to New Currency", f"Enter the conversion rate from {self.currency_symbol} to {new_currency}:")
            if conversion_rate is not None:
                self.currency_symbol = new_currency
                for transaction in self.transactions:
                    transaction['Amount'] *= conversion_rate
                self.update_balance_label()
                self.calculate_income_expenses()
                
    def export_reports_csv(self):
        # Export reports as a CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="") as csvfile:
                    fieldnames = ["Date", "Amount", "Category", "Description"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for transaction in self.transactions:
                        writer.writerow({
                            "Date": transaction["Date"].strftime("%Y-%m-%d"),
                            "Amount": transaction["Amount"],
                            "Category": transaction["Category"],
                            "Description": transaction["Description"]
                        })
                messagebox.showinfo("Export Reports", "Reports exported as CSV successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export reports: {str(e)}")

    def export_reports_pdf(self):
        # Export reports as a PDF file
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Transaction Reports", ln=True, align="C")
                pdf.ln(10)
                pdf.cell(30, 10, txt="Date", border=1)
                pdf.cell(30, 10, txt="Amount", border=1)
                pdf.cell(40, 10, txt="Category", border=1)
                pdf.cell(90, 10, txt="Description", border=1)
                pdf.ln()
                for transaction in self.transactions:
                    pdf.cell(30, 10, txt=transaction["Date"].strftime("%Y-%m-%d"), border=1)
                    pdf.cell(30, 10, txt=str(transaction["Amount"]), border=1)
                    pdf.cell(40, 10, txt=transaction["Category"], border=1)
                    pdf.cell(90, 10, txt=transaction["Description"], border=1)
                    pdf.ln()
                pdf.output(file_path)
                messagebox.showinfo("Export Reports", "Reports exported as PDF successfully.")
            except Exception as e:
        
                messagebox.showerror("Error", f"Failed to export reports: {str(e)}")
                
    def generate_graphical_representation(self):
        # Extract transaction amounts and categories
        amounts = [transaction['Amount'] for transaction in self.transactions]
        categories = [transaction['Category'] for transaction in self.transactions]
    
        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel(f'Amount ({self.currency_symbol})')
        plt.title('Graphical Representation of Transactions')
        plt.xticks(rotation=45, ha='right')  # Rotate category labels for readability
        plt.tight_layout()
    
        # Display the chart
        plt.show()
        
        # Transaction Sorting and Filtering
    def sort_transactions_by_date_asc(self):
        # Sort transactions by date in ascending order
        self.transactions.sort(key=lambda x: x['Date'])
        self.show_all_transactions()

    def sort_transactions_by_date_desc(self):
        # Sort transactions by date in descending order
        self.transactions.sort(key=lambda x: x['Date'], reverse=True)
        self.show_all_transactions()

    def sort_transactions_by_amount_asc(self):
        # Sort transactions by amount in ascending order
        self.transactions.sort(key=lambda x: x['Amount'])
        self.show_all_transactions()

    def sort_transactions_by_amount_desc(self):
        # Sort transactions by amount in descending order
        self.transactions.sort(key=lambda x: x['Amount'], reverse=True)
        self.show_all_transactions()

    def filter_transactions_by_category(self):
        # Filter transactions by selected category
        selected_category = self.category_var.get()
        self.transactions_listbox.delete(0, END)
        for transaction in self.transactions:
            if transaction['Category'] == selected_category:
                self.transactions_listbox.insert(END, f"Date: {transaction['Date'].strftime('%Y-%m-%d')}, Amount: {self.currency_symbol}{transaction['Amount']:.2f}, Category: {transaction['Category']}, Description: {transaction['Description']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()
