import tkinter as tk
from tkinter import ttk, messagebox

from utils import helpers


class CustomersFrame(tk.Frame):
    def __init__(self, parent, dbms):
        super().__init__(parent)
        self.dbmanager = dbms



        columns = ("Customer Name", "Customer Phone", "Customer Address")
        self.customer_details_treeview = ttk.Treeview(self, columns=columns, show="headings", height=21)
        for col in columns:
            self.customer_details_treeview.heading(col, text=col)

        self.customer_details_treeview.column("Customer Name", width=314, stretch=False)
        self.customer_details_treeview.column("Customer Phone", width=150, stretch=False)
        self.customer_details_treeview.column("Customer Address", width=360, stretch=False)
        self.customer_details_treeview.grid(row=0, column=0, padx=(20, 0), pady=20)

        # Menu Options for Treeview
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)
        self.customer_details_treeview.bind("<Button-3>", self.show_menu)

        self.customer_details_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.customer_details_treeview.tag_configure("oddrow", background="#FFFFFF")

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.customer_details_treeview.yview)
        scrollbar.grid(row=0, column=1, pady=20, sticky=tk.NS)
        self.customer_details_treeview.config(yscrollcommand=scrollbar.set)

        # New Customer Entry
        new_customer_entry_frame = tk.Frame(self, highlightbackground="#2c3e50", highlightthickness=2)
        new_customer_entry_frame.grid(row=0, column=2, padx=20, pady=20, sticky=tk.N)

        tk.Label(new_customer_entry_frame,
                 text="Add New Customer",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18)).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(new_customer_entry_frame,
                 text="Customer Name",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.customer_name_entry = tk.Entry(new_customer_entry_frame, font=("Segoe UI", 12))
        self.customer_name_entry.grid(row=2, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(new_customer_entry_frame,
                 text="Customer Phone",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12)).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.customer_phone_entry = tk.Entry(new_customer_entry_frame, validate="key", validatecommand=(self.register(
            helpers.is_digit), "%P"), font=("Segoe UI", 12), )
        self.customer_phone_entry.grid(row=4, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(new_customer_entry_frame,
                 text="Customer Address",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=5, column=0, padx=5, sticky=tk.NSEW)
        self.customer_address_entry = tk.Entry(new_customer_entry_frame, font=("Segoe UI", 12))
        self.customer_address_entry.grid(row=6, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        ttk.Button(new_customer_entry_frame,
                   text="Add Customer", command=self.add_customer,
                   ).grid(row=7, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        self.refresh()

    def add_customer(self):
        customer = self.dbmanager.Customer(name=self.customer_name_entry.get(),
                                           phone=self.customer_phone_entry.get(),
                                           address=self.customer_address_entry.get()
                                           )
        does_exist = bool(self.dbmanager.get_customer_by_phone(customer.phone))
        if does_exist:
            messagebox.showerror(
                title="Duplicate Found",
                message="Customer already exists!"
            )
            return

        if not all([customer.name, customer.phone, customer.address]):
            messagebox.showerror(
                title="Missing Information",
                message="Customer's name, phone, address must all be filled in."
            )
            return

        self.dbmanager.add_customer(customer)
        self.refresh()

    def refresh(self):
        self.customer_details_treeview.delete(*self.customer_details_treeview.get_children())
        for i, customer in enumerate(self.dbmanager.get_all_customers()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.customer_details_treeview.insert("", tk.END,
                                                  values=(customer.name, customer.phone, customer.address),
                                                  tags=tag)
        self.customer_name_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_address_entry.delete(0, tk.END)

    def show_menu(self, event):
        iid = self.customer_details_treeview.identify_row(event.y)
        if iid:
            self.customer_details_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)