import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from utils import helpers


class ExpensesFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.dbmanager = dbmanager
        self.filter_var = tk.StringVar(value="all_expenses")
        # Options Frame ------------------------------------------------------------------------------------------------
        options_frame = tk.Frame(self,  )
        options_frame.grid(row=0, column=0,padx=20, pady=(20, 0), sticky=tk.NSEW)

        self.all_expenses_radio_button = tk.Radiobutton(options_frame, text="All\nExpenses", width=10, fg="white",
                                                        bg="#3498db",
                                                        command=self.all_expenses, font=("Arial", 15),
                                                        activeforeground="white", activebackground="#1abc9c",
                                                        selectcolor="#1abc9c",
                                                        variable=self.filter_var, value="all_expenses",
                                                        indicatoron=False,
                                                        height=3)
        self.all_expenses_radio_button.grid(row=0, column=0, sticky=tk.NSEW)

        self.today_expenses_radio_button = tk.Radiobutton(options_frame, text="Today\nExpenses", width=10,
                                                          fg="white", bg="#3498db", command=self.today_expenses,
                                                          activeforeground="white", font=("Arial", 15),
                                                          activebackground="#1abc9c", selectcolor="#1abc9c",
                                                          variable=self.filter_var,
                                                          value="today_expenses", indicatoron=False, height=3)

        self.today_expenses_radio_button.grid(row=0, column=1, sticky=tk.NSEW)

        self.custom_search_button = tk.Radiobutton(options_frame, text="Custom\nSearch", width=10, fg="white",
                                                   bg="#3498db",
                                                   command=self.custom_search, font=("Arial", 15),
                                                   activeforeground="white", activebackground="#1abc9c",
                                                   selectcolor="#1abc9c",
                                                   variable=self.filter_var, value="custom_search", indicatoron=False,
                                                   height=3)
        self.custom_search_button.grid(row=0, column=2, sticky=tk.NSEW)

        custom_search = tk.Frame(options_frame, highlightbackground="#2c3e50", highlightthickness=2)
        custom_search.grid(row=0, column=3, sticky=tk.NSEW)

        self.search_label = tk.Label(custom_search,
                                     text="Search",
                                     fg="white",
                                     bg="#2c3e50",
                                     width=15,
                                     font=("Segoe UI", 14), )
        self.search_label.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)
        self.search_by_label = tk.Label(custom_search, text="Search by:", font=("Segoe UI", 10), )
        self.search_by_label.grid(row=1, column=0, pady=10, sticky=tk.E)

        self.search_filter = tk.StringVar(value="by_date")
        self.by_date_radiobutton = tk.Radiobutton(custom_search, text="Date", fg="white", bg="#3498db",
                                                  activeforeground="white", width=8, font=("Segoe UI", 10),
                                                  activebackground="#1abc9c", selectcolor="#1abc9c",
                                                  variable=self.search_filter,
                                                  value="by_date", command=self.search_by_date,
                                                  indicatoron=False)
        self.by_date_radiobutton.grid(row=1, column=1, pady=10, sticky=tk.EW)

        self.option_label = tk.Label(custom_search, text="Date:", width=13, font=("Segoe UI", 10),
                                     anchor=tk.E, )
        self.option_label.grid(row=2, column=0, pady=(0, 10), padx=(7, 0), sticky=tk.E)

        self.date_entry = DateEntry(
            custom_search,
            date_pattern="dd-mm-yyyy",
            width=10,
            showweeknumbers=False,
            background="#2c3e50",
            foreground="white",
            selectbackground="#1a252f",
        )
        self.date_entry.grid(row=2, column=1, pady=(0, 10))

        self.search_button = tk.Button(custom_search, text="Get", font=("Segoe UI", 8),
                                       command=self.get_expenses_by_search)
        self.search_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 8), sticky=tk.EW)
        # Add New Expense
        new_expense_entry_frame = tk.Frame(self, highlightbackground="#2c3e50", highlightthickness=2)
        new_expense_entry_frame.grid(row=1, column=1, padx=20, pady=20, sticky=tk.N)

        tk.Label(new_expense_entry_frame,
                 text="Add New Expense",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18)).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(new_expense_entry_frame,
                 text="Purpose",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.purpose_entry = tk.Entry(new_expense_entry_frame, font=("Segoe UI", 12))
        self.purpose_entry.grid(row=2, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(new_expense_entry_frame,
                 text="Amount",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12)).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.amount_entry = tk.Entry(new_expense_entry_frame, validate="key", validatecommand=(self.register(
            helpers.is_digit), "%P"), font=("Segoe UI", 12), )
        self.amount_entry.grid(row=4, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        ttk.Button(new_expense_entry_frame,
                   text="Add", command=self.add_new_expense,
                   ).grid(row=5, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        # Expenses Frame----------------------------------------------------------------------------------
        self.expenses_treeview_frame = tk.Frame(self)
        self.expenses_treeview_frame.grid(row=1, column=0, sticky=tk.N)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)

        columns = ("Date", "Time", "Purpose", "Amount",)
        self.expenses_treeview = ttk.Treeview(self.expenses_treeview_frame, columns=columns, show="headings",
                                              height=16)

        for col in columns:
            self.expenses_treeview.heading(col, text=col)
        self.expenses_treeview.column("Date", width=150, stretch=False, anchor=tk.W)
        self.expenses_treeview.column("Time", width=180, stretch=False, anchor=tk.W)
        self.expenses_treeview.column("Purpose", width=350, stretch=False, anchor=tk.W)
        self.expenses_treeview.column("Amount", width=150, stretch=False, anchor=tk.W)
        self.expenses_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.expenses_treeview.tag_configure("oddrow", background="#FFFFFF")
        self.expenses_treeview.grid(row=0, column=0, padx=(20, 0), pady=20, sticky=tk.N)

        sales_treeview_scrollbar = ttk.Scrollbar(self.expenses_treeview_frame, orient=tk.VERTICAL,
                                                 command=self.expenses_treeview.yview)
        sales_treeview_scrollbar.grid(row=0, column=1, pady=20, sticky=tk.NS)
        self.expenses_treeview.configure(yscrollcommand=sales_treeview_scrollbar.set)
        self.expenses_treeview.bind("<Button-3>", self.show_menu)

        self.all_expenses_radio_button.invoke()

    def show_menu(self, event):
        iid = self.expenses_treeview.identify_row(event.y)
        if iid:
            self.expenses_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def add_new_expense(self):
        purpose = self.purpose_entry.get()
        amount = self.amount_entry.get()
        new_expense = self.dbmanager.Expense(purpose=purpose, amount=amount)
        self.dbmanager.add_new_expense(new_expense)
        self.refresh()

    def refresh(self):
        self.purpose_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        filter_option = self.filter_var.get()
        if filter_option == "all_expenses":
            self.all_expenses_radio_button.invoke()
        elif filter_option == "today_expenses":
            self.today_expenses_radio_button.invoke()

    def all_expenses(self):
        self.disable_search_mechanism()
        all_expenses = self.dbmanager.get_all_expenses()[::-1]
        self.insert_expenses_to_treeview(all_expenses)

    def today_expenses(self):
        self.disable_search_mechanism()
        today_expenses = self.dbmanager.get_today_expenses()[::-1]
        self.insert_expenses_to_treeview(today_expenses)

    def custom_search(self):
        self.expenses_treeview.delete(*self.expenses_treeview.get_children())
        self.enable_search_mechanism()

    def search_by_date(self):
        self.option_label.config(text="Date:")

    def enable_search_mechanism(self):
        self.search_label.config(fg="white")
        self.option_label.config(fg="black")
        self.search_by_label.config(fg="black")
        self.by_date_radiobutton.config(state=tk.NORMAL)
        self.search_button.config(state=tk.NORMAL)
        self.date_entry.config(state=tk.NORMAL)

    def disable_search_mechanism(self):
        self.search_label.config(fg="gray")
        self.option_label.config(fg="gray")
        self.search_by_label.config(fg="gray")
        self.by_date_radiobutton.config(state=tk.DISABLED)
        self.search_button.config(state=tk.DISABLED)
        self.date_entry.config(state=tk.DISABLED)

    def get_expenses_by_search(self):
        date = self.date_entry.get()
        day, month, year = date.split("-")
        date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
        expenses = self.dbmanager.get_expenses_by_date(date_obj)
        self.insert_expenses_to_treeview(expenses)

    def insert_expenses_to_treeview(self, expenses):
        self.expenses_treeview.delete(*self.expenses_treeview.get_children())
        for i, expense in enumerate(expenses):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.expenses_treeview.insert(
                "",
                tk.END, iid=expense.id,
                values=(expense.date.strftime("%d-%m-%Y"), expense.time.strftime("%I:%M %p"), expense.purpose,
                        expense.amount), tags=tag)
