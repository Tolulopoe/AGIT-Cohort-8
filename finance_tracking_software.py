import tkinter as tk
from tkinter import ttk, messagebox
import csv

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("600x500")
        self.root.configure(bg="#2C3E50")

        self.transactions = []
        self.budget_limit = 2250000
        
        # Header Frame
        header_frame = tk.Frame(root, bg="#1ABC9C", padx=10, pady=10)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Personal Finance Tracker", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack()
        
        # Input Frame
        input_frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
        input_frame.pack(fill="x", pady=5)
        
        tk.Label(input_frame, text="Category:", font=("Arial", 10, "bold"), bg="#34495E", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Amount:", font=("Arial", 10, "bold"), bg="#34495E", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Type:", font=("Arial", 10, "bold"), bg="#34495E", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.transaction_type = tk.StringVar(value="Income")
        ttk.Radiobutton(input_frame, text="Income", variable=self.transaction_type, value="Income").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="Expense", variable=self.transaction_type, value="Expense").grid(row=2, column=2, sticky="w")
        
        # Buttons Frame
        button_frame = tk.Frame(root, bg="#2C3E50", pady=5)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_transaction).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Filter Category", command=self.filter_category).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save Transactions", command=self.save_transactions).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load Transactions", command=self.load_transactions).pack(side="left", padx=5)
        
        # Transactions List
        self.tree = ttk.Treeview(root, columns=("Category", "Amount", "Type"), show="headings")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Summary Labels
        self.income_label = tk.Label(root, text="Total Income: $0", font=("Arial", 10, "bold"), bg="#27AE60", fg="white")
        self.income_label.pack(fill="x")
        
        self.expense_label = tk.Label(root, text="Total Expenses: $0", font=("Arial", 10, "bold"), bg="#C0392B", fg="white")
        self.expense_label.pack(fill="x")
        
        self.balance_label = tk.Label(root, text="Balance: $0", font=("Arial", 10, "bold"), bg="#F39C12", fg="white")
        self.balance_label.pack(fill="x")
    
    def add_transaction(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        t_type = self.transaction_type.get()
        
        if not category or not amount:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")
            return
        
        self.transactions.append((category, amount, t_type))
        self.tree.insert("", tk.END, values=(category, amount, t_type))
        
        self.update_summary()
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
    
    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No transaction selected!")
            return
        
        for item in selected_item:
            values = self.tree.item(item, "values")
            self.transactions.remove(values)
            self.tree.delete(item)
        
        self.update_summary()
    
    def update_summary(self):
        total_income = sum(amount for category, amount, t_type in self.transactions if t_type == "Income")
        total_expense = sum(amount for category, amount, t_type in self.transactions if t_type == "Expense")
        balance = total_income - total_expense
        
        self.income_label.config(text=f"Total Income: ${total_income}")
        self.expense_label.config(text=f"Total Expenses: ${total_expense}")
        self.balance_label.config(text=f"Balance: ${balance}")
        
        if total_expense > self.budget_limit:
            messagebox.showwarning("Budget Alert", "Warning: Expenses exceed budget limit!")
    
    def filter_category(self):
        category_filter = self.category_entry.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for transaction in self.transactions:
            if transaction[0].lower() == category_filter or category_filter == "":
                self.tree.insert("", tk.END, values=transaction)
    
    def save_transactions(self):
        with open("transactions.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount", "Type"])
            writer.writerows(self.transactions)
        messagebox.showinfo("Success", "Transactions saved successfully!")
    
    def load_transactions(self):
        try:
            with open("transactions.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)
                self.transactions = [tuple(row) for row in reader]
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for transaction in self.transactions:
                    self.tree.insert("", tk.END, values=transaction)
                self.update_summary()
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved transactions found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()

