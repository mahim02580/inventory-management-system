import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils.helpers import AutoCompleteEntry, AutoCompleteEntryForSuppliers
from tkinter.font import Font
from utils import helpers


class NewPurchase(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.configure(padx=20, pady=20)
        self.parent = parent
        self.dbmanager = dbmanager

        # Product Selection Frame--------------------------------------------------------------------------------------------
        ## Upper Part
        product_selection_frame = tk.Frame(self)
        product_selection_frame.grid(row=0, column=0)

        tk.Label(product_selection_frame, text="Select Product:", font=("Arial", 15), ).grid(row=0, column=0,
                                                                                             sticky=tk.W)

        self.product_name_search_entry = AutoCompleteEntry(product_selection_frame, db_path="database/database.db", font=("Arial", 15),
                                                           width=35)
        self.product_name_search_entry.grid(row=0, column=1, sticky=tk.EW)

        tk.Label(product_selection_frame,
                 text="Quantity:",
                 font=Font(size=15), ).grid(row=0, column=2)

        self.quantity = tk.Spinbox(product_selection_frame, from_=1, to=100000, font=("Arial", 15), width=7,
                                   validate="key",
                                   validatecommand=(product_selection_frame.register(helpers.is_digit), "%P"))
        self.quantity.grid(row=0, column=3)

        ttk.Button(product_selection_frame, text="Add", command=self.add_item).grid(row=0, column=4)

        ## Lower Part

        treeview_style = ttk.Style(product_selection_frame)
        treeview_style.configure("Treeview",
                                 font=("Segoe UI", 12),
                                 rowheight=30,
                                 borderwidth=0,
                                 highlightthickness=0)
        treeview_style.configure("Treeview.Heading",
                                 background="#e0e0e0",
                                 foreground="black",
                                 font=("Segoe UI", 12, "bold"))

        self.menu = tk.Menu(product_selection_frame, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_item)
        columns = ("Code", "Category", "Product Name", "Quantity", "Unit Type", "Unit Price", "Subtotal")
        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=19,
                                                   style="Treeview")
        self.product_entry_treeview.bind("<Double-1>", self.edit_quantity_and_unit_price)
        self.product_entry_treeview.bind("<Button-3>", self.show_menu)

        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)

        self.product_entry_treeview.column("Code", width=85, stretch=False, )
        self.product_entry_treeview.column("Category", width=85, stretch=False, )
        self.product_entry_treeview.column("Product Name", width=310, stretch=False, )
        self.product_entry_treeview.column("Quantity", width=85, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Unit Type", width=85, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Unit Price", width=85, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Subtotal", width=85, stretch=False, anchor=tk.CENTER)

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        # Invoice Making Frame--------------------------------------------------------------------------------------------
        purchase_invoice_frame = tk.Frame(self)
        purchase_invoice_frame.grid(row=0, column=1, sticky=tk.N, padx=(20, 0))

        tk.Label(purchase_invoice_frame,
                 text="Total Items",
                 font=("Arial", 16, "bold"),
                 anchor=tk.W
                 ).grid(row=0, column=0, sticky=tk.W)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 font=("Arial", 16, "bold"),
                 anchor=tk.W
                 ).grid(row=0, column=1)
        self.total_items = tk.IntVar(value=0)

        tk.Label(purchase_invoice_frame,
                 textvariable=self.total_items,
                 fg="white",
                 bg="black",
                 font=("Arial", 16, "bold"),
                 anchor=tk.E, ).grid(row=0, column=2, sticky=tk.NSEW)

        self.mrp_total = tk.IntVar(value=0)
        self.total = tk.IntVar(value=0)

        # MRP Total
        ttk.Separator(purchase_invoice_frame, orient="horizontal").grid(row=1, column=0, columnspan=3, pady=(21, 0),
                                                                        sticky=tk.EW)
        tk.Label(purchase_invoice_frame,
                 text="MRP Total",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=2, column=0, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=2, column=1, sticky=tk.NSEW)

        tk.Label(purchase_invoice_frame,
                 textvariable=self.mrp_total,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 width=6,
                 anchor=tk.E).grid(row=2, column=2, sticky=tk.NSEW)

        # (-) Discount
        tk.Label(purchase_invoice_frame,
                 text="(-) Discount)",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W).grid(row=3, column=0, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 ).grid(row=3, column=1, sticky=tk.NSEW)

        self.discount_entry = tk.Entry(purchase_invoice_frame,
                                       width=6,
                                       highlightbackground="#2c3e50",
                                       highlightthickness=1,
                                       highlightcolor="#2c3e50",
                                       font=("Segoe UI", 12),
                                       justify=tk.RIGHT, )

        self.discount_entry.insert(tk.END, "0")
        self.discount_entry.grid(row=3, column=2, sticky=tk.EW)
        self.discount_entry.config(validate="key",
                                   validatecommand=(purchase_invoice_frame.register(self.update_total), "%P"))

        # Total Payable
        ttk.Separator(purchase_invoice_frame, orient="horizontal").grid(row=4, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(purchase_invoice_frame,
                 text="Total Payable",
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.W,
                 fg="white").grid(row=5, column=0, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=5, column=1, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 textvariable=self.total,
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.E,
                 width=6,
                 fg="white").grid(row=5, column=2, sticky=tk.NSEW)

        # Total Paid + Due-------------------------------------------------------------------------------------

        ## Total Paid
        ttk.Separator(purchase_invoice_frame, orient="horizontal").grid(row=7, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(purchase_invoice_frame,
                 text="Paid",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W,
                 fg="white").grid(row=8, column=0, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=8, column=1, sticky=tk.NSEW)
        self.paid_amount_entry = tk.Entry(purchase_invoice_frame, width=6,
                                          highlightbackground="#2c3e50",
                                          highlightthickness=1,
                                          highlightcolor="#2c3e50",
                                          font=("Segoe UI", 12),
                                          justify=tk.RIGHT, )
        self.paid_amount_entry.grid(row=8, column=2, sticky=tk.NSEW)
        self.paid_amount_entry.insert(0, "0")
        self.paid_amount_entry.config(validate="key",
                                      validatecommand=(purchase_invoice_frame.register(self.calculate_due), "%P"), )

        ## Due
        tk.Label(purchase_invoice_frame,
                 text="Due",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=10, column=0, sticky=tk.NSEW)
        tk.Label(purchase_invoice_frame,
                 text=":",
                 bg="#2c3e50", font=("Segoe UI", 12),
                 fg="white").grid(
            row=10, column=1, sticky=tk.NSEW)
        self.due = tk.IntVar(value=0)
        tk.Label(purchase_invoice_frame,
                 textvariable=self.due,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=10, column=2, sticky=tk.NSEW)

        # Customer Details Frame
        supplier_details_frame = tk.Frame(purchase_invoice_frame)
        supplier_details_frame.grid(row=11, column=0, columnspan=3, pady=20, sticky=tk.NSEW)

        tk.Label(supplier_details_frame,
                 text="Supplier",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12), ).grid(row=0, column=0, sticky=tk.NSEW)
        self.supplier_name_entry = AutoCompleteEntryForSuppliers(supplier_details_frame, db_path="database/database.db",
                                                                 width=28, font=("Segoe UI", 12))
        self.supplier_name_entry.grid(row=1, column=0, sticky=tk.EW)

        tk.Label(supplier_details_frame,
                 text="Delivery Date",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=2, column=0, pady=(10, 0), sticky=tk.NSEW)

        self.purchase_delivery_date_entry = DateEntry(
            supplier_details_frame,
            date_pattern="dd-mm-yyyy",
            width=40,
            showweeknumbers=False,
            background="#2c3e50",
            foreground="white",
            selectbackground="#1a252f",
        )
        self.purchase_delivery_date_entry.grid(row=3, column=0)

        ttk.Button(supplier_details_frame,
                   text="Make Purchase",
                   command=self.make_purchase).grid(row=4, column=0, pady=(32, 0), sticky=tk.EW)

        self.refresh()

    def delete_item(self, items=None):
        selected = items or self.product_entry_treeview.selection()
        if not selected:
            return

        for item in selected:
            self.product_entry_treeview.delete(item)

        # Update calculation after deleting an item
        self.update_calculation()

    def show_menu(self, event):
        iid = self.product_entry_treeview.identify_row(event.y)
        if iid:
            self.product_entry_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def edit_quantity_and_unit_price(self, event):
        # Detect row and column
        region = self.product_entry_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_entry_treeview.identify_row(event.y)
        column = self.product_entry_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1
        # Return, if column is not Amount Column
        if col_index == 0 or col_index == 1 or col_index == 2 or col_index == 4 or col_index== 6:
            return

        x, y, width, height = self.product_entry_treeview.bbox(row_id, column)

        # Current value
        value = self.product_entry_treeview.item(row_id, "values")[col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.product_entry_treeview, font=("Segoe UI", 12), justify=tk.CENTER)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit():
            new_val = entry.get()
            values = list(self.product_entry_treeview.item(row_id, "values"))
            values[col_index] = new_val
            values[-1] = str(int(values[-4]) * int(values[-2]))
            self.product_entry_treeview.item(row_id, values=values)
            entry.destroy()
            self.update_calculation()

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def add_item(self):
        product_code = self.product_name_search_entry.get().split("-")[0].strip()
        quantity = int(self.quantity.get())

        product = self.dbmanager.get_product_by_code(product_code)
        if not product:
            messagebox.showerror("Not Found", "This product doesn't exist!")
            return

        subtotal = int(product.base_unit_price) * quantity
        try:
            self.product_entry_treeview.insert("", tk.END, iid=product.code,
                                               values=(product.code, product.category, product.name, quantity, product.base_unit_type,
                                                       product.base_unit_price, subtotal),
                                               tags="product_entry_row")
        except tk.TclError:
            messagebox.showinfo("Duplicate Found", f"{product.name} already taken!")
        self.update_calculation()
        self.product_name_search_entry.delete(0, tk.END)

    def update_calculation(self):
        # Update Total Items
        total_items = len(self.product_entry_treeview.get_children())
        self.total_items.set(total_items)

        # Update MRP Total
        mrp_total_list = [int(self.product_entry_treeview.item(item, "values")[-1]) for item in
                          self.product_entry_treeview.get_children()]
        mrp_total = sum(mrp_total_list)
        self.mrp_total.set(mrp_total)

        # Update total after subtracting discount
        discount = self.discount_entry.get()
        self.update_total(discount)

    def update_total(self, new_value):
        if new_value == "":
            new_value = "0"

        if not new_value.isdigit():
            return False  # block anything that's not a number

        # Update total after subtracting discount
        mrp_total = self.mrp_total.get()
        discount = int(new_value)
        self.total.set(mrp_total - discount)
        self.calculate_due(self.paid_amount_entry.get())
        return True

    def calculate_due(self, paid):
        if paid == "":
            paid = "0"

        if not paid.isdigit():
            return False  # block anything that's not a number

        paid_amount = int(paid)
        total_payable = int(self.total.get())
        if paid_amount < total_payable:
            self.due.set(total_payable - paid_amount)
        else:
            self.due.set(0)
        return True

    def refresh(self):

        # Deletes all item in the Product Entry Treeview
        self.delete_item(self.product_entry_treeview.get_children())

        # Clears all entries
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        self.paid_amount_entry.delete(0, tk.END)
        self.paid_amount_entry.insert(0, "0")
        self.supplier_name_entry.delete(0, tk.END)

        # Set Quantity 1
        self.quantity.delete(0, tk.END)
        self.quantity.insert(0, "1")

    def make_purchase(self):
        if not self.product_entry_treeview.get_children():
            messagebox.showerror(title="Error", message="Please add products to make purchase.")
            return

        supplier_name = self.supplier_name_entry.get().replace(" ", "-")

        if supplier_name:
            supplier = self.dbmanager.get_supplier_by_name(supplier_name)
            if not supplier:
                # Make Supplier
                supplier = self.dbmanager.Supplier(
                    name=supplier_name,
                )
                # Add Supplier
                self.dbmanager.add_supplier(supplier)

        else:
            messagebox.showerror("Error", "Please provide a supplier name")
            return

        # Taking Delivery Date for the Purchase
        date = self.purchase_delivery_date_entry.get()
        day, month, year = date.split("-")
        date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
        # Make Purchase
        purchase = self.dbmanager.Purchase(
            supplier_id=supplier.id,
            total_payable=self.total.get(),
            paid=self.paid_amount_entry.get(),
            due=self.due.get(),
            delivery_date=date_obj,
            status="Pending" # Default Status
        )
        for row_id in self.product_entry_treeview.get_children():
            code, category, product_name, quantity, unit_type, unit_price, subtotal = self.product_entry_treeview.item(row_id,
                                                                                                             "values")

            # Male SaleItem for each product
            purchase_item = self.dbmanager.PurchaseItem(
                product_code=code,
                product_category=category,
                product_name=product_name,
                quantity=int(quantity),
                unit_type=unit_type,
                unit_price=int(unit_price),
                subtotal=int(subtotal),
            )
            # Add PurchaseItem to Purchase
            purchase.items.append(purchase_item)

        self.dbmanager.add_purchase(purchase)
        self.refresh()


class PurchasesFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.dbmanager = dbmanager
        self.filter_var = tk.StringVar(value="all_purchases")
        # Options Frame ------------------------------------------------------------------------------------------------
        options_frame = tk.Frame(self, padx=20, pady=20)
        options_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.all_purchases_radio_button = tk.Radiobutton(options_frame, text="All\nPurchases", width=10, fg="white",
                                                         bg="#3498db",
                                                         command=self.all_purchases, font=("Arial", 15),
                                                         activeforeground="white", activebackground="#1abc9c",
                                                         selectcolor="#1abc9c",
                                                         variable=self.filter_var, value="all_purchases",
                                                         indicatoron=False,
                                                         height=3)
        self.all_purchases_radio_button.grid(row=0, column=0, sticky=tk.NSEW)

        self.today_delivery_radio_button = tk.Radiobutton(options_frame, text="Today\nDelivery", width=10,
                                                          fg="white", bg="#3498db", command=self.today_delivery,
                                                          activeforeground="white", font=("Arial", 15),
                                                          activebackground="#1abc9c", selectcolor="#1abc9c",
                                                          variable=self.filter_var,
                                                          value="today_delivery", indicatoron=False, height=3)

        self.today_delivery_radio_button.grid(row=0, column=1, sticky=tk.NSEW)

        self.due_purchases_radio_button = tk.Radiobutton(options_frame, text="Due\nPurchases", width=10,
                                                         fg="white", bg="#3498db", command=self.due_purchases,
                                                         activeforeground="white", font=("Arial", 15),
                                                         activebackground="#1abc9c", selectcolor="#1abc9c",
                                                         variable=self.filter_var,
                                                         value="due_purchases", indicatoron=False, height=3)
        self.due_purchases_radio_button.grid(row=0, column=2, sticky=tk.NSEW)
        self.custom_search_button = tk.Radiobutton(options_frame, text="Custom\nSearch", width=10, fg="white",
                                                   bg="#3498db",
                                                   command=self.custom_search, font=("Arial", 15),
                                                   activeforeground="white", activebackground="#1abc9c",
                                                   selectcolor="#1abc9c",
                                                   variable=self.filter_var, value="custom_search", indicatoron=False,
                                                   height=3)
        self.custom_search_button.grid(row=0, column=3, sticky=tk.NSEW)

        custom_search = tk.Frame(options_frame, highlightbackground="#2c3e50", highlightthickness=2)
        custom_search.grid(row=0, column=4, sticky=tk.NSEW)

        self.search_label = tk.Label(custom_search,
                                     text="Search",
                                     fg="white",
                                     bg="#2c3e50",
                                     width=15,
                                     font=("Segoe UI", 14), )
        self.search_label.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)
        self.search_by_label = tk.Label(custom_search, text="Search by:", font=("Segoe UI", 10), )
        self.search_by_label.grid(row=1, column=0, pady=10, sticky=tk.E)

        self.search_filter = tk.StringVar(value="by_supplier")
        self.by_supplier_radiobutton = tk.Radiobutton(custom_search, text="Supplier", fg="white", bg="#3498db",
                                                      activeforeground="white", width=8, font=("Segoe UI", 10),
                                                      activebackground="#1abc9c", selectcolor="#1abc9c",
                                                      variable=self.search_filter,
                                                      value="by_supplier", command=self.search_by_supplier,
                                                      indicatoron=False)
        self.by_supplier_radiobutton.grid(row=1, column=1, pady=10, sticky=tk.W)
        self.by_purchase_date_radiobutton = tk.Radiobutton(custom_search, text="Purchase Date", fg="white", bg="#3498db",
                                                           activeforeground="white", width=12, font=("Segoe UI", 10),
                                                           activebackground="#1abc9c", selectcolor="#1abc9c",
                                                           variable=self.search_filter,
                                                           value="by_purchase_date", command=self.search_by_purchase_date, indicatoron=False)
        self.by_purchase_date_radiobutton.grid(row=1, column=2, pady=10, sticky=tk.W)
        self.by_delivery_date_radiobutton = tk.Radiobutton(custom_search, text="Delivery Date", fg="white", bg="#3498db",
                                                           activeforeground="white", width=12, font=("Segoe UI", 10),
                                                           activebackground="#1abc9c", selectcolor="#1abc9c",
                                                           variable=self.search_filter,
                                                           value="by_delivery_date", command=self.search_by_date_range, indicatoron=False)
        self.by_delivery_date_radiobutton.grid(row=1, column=3, pady=10, padx=(0, 8), sticky=tk.W)
        self.option_label = tk.Label(custom_search, text="Supplier:", width=13, font=("Segoe UI", 10),
                                     anchor=tk.E, )
        self.option_label.grid(row=2, column=0, pady=(0, 10), padx=(7, 0), sticky=tk.E)

        self.supplier_name_entry = AutoCompleteEntryForSuppliers(custom_search, db_path="database/database.db", width=20, font=("Segoe UI", 10), )
        self.supplier_name_entry.grid(row=2, column=1, columnspan=2, pady=(0, 10), sticky=tk.EW)
        self.date_entry = DateEntry(
            custom_search,
            date_pattern="dd-mm-yyyy",
            width=23,
            showweeknumbers=False,
            background="#2c3e50",
            foreground="white",
            selectbackground="#1a252f",
        )
        self.date_entry.grid(row=2, column=1, pady=(0, 10), columnspan=2)
        self.date_entry.grid_remove()

        self.search_button = tk.Button(custom_search, text="Get", font=("Segoe UI", 8),
                                       command=self.get_purchases_by_search)
        self.search_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 8), sticky=tk.EW)

        # Purchases Frame----------------------------------------------------------------------------------
        self.purchases_treeview_frame = tk.Frame(self)
        self.purchases_treeview_frame.grid(row=1, column=0, sticky=tk.N)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)
        self.menu.add_command(label="View Items", command=self.view_purchases_items)
        self.menu.add_command(label="Order Received", command=self.order_received)
        self.menu.add_command(label="Pay Due Payment", command=self.pay_due_payment)

        columns = ("Supplier", "Purchase Date", "Delivery Date", "Total Payable", "Paid", "Due", "Status")
        self.purchases_treeview = ttk.Treeview(self.purchases_treeview_frame, columns=columns, show="headings",
                                               height=16)

        for col in columns:
            self.purchases_treeview.heading(col, text=col)
        self.purchases_treeview.column("Supplier", width=150, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Purchase Date", width=180, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Delivery Date", width=200, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Total Payable", width=150, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Paid", width=150, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Due", width=150, stretch=False, anchor=tk.W)
        self.purchases_treeview.column("Status", width=100, stretch=False, anchor=tk.W)
        self.purchases_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.purchases_treeview.tag_configure("oddrow", background="#FFFFFF")
        self.purchases_treeview.grid(row=0, column=0, padx=(20, 0), pady=20, sticky=tk.N)

        sales_treeview_scrollbar = ttk.Scrollbar(self.purchases_treeview_frame, orient=tk.VERTICAL,
                                                 command=self.purchases_treeview.yview)
        sales_treeview_scrollbar.grid(row=0, column=1, pady=20, sticky=tk.NS)
        self.purchases_treeview.configure(yscrollcommand=sales_treeview_scrollbar.set)
        self.purchases_treeview.bind("<Button-3>", self.show_menu)

        self.all_purchases_radio_button.invoke()

    def show_menu(self, event):
        iid = self.purchases_treeview.identify_row(event.y)
        if iid:
            self.purchases_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def all_purchases(self):
        self.disable_search_mechanism()
        all_purchases = self.dbmanager.get_all_purchases()
        self.insert_purchases_to_treeview(all_purchases)

    def today_delivery(self):
        self.disable_search_mechanism()
        today_delivery_purchases = self.dbmanager.get_today_delivery_purchases()
        self.insert_purchases_to_treeview(today_delivery_purchases)

    def due_purchases(self):
        self.disable_search_mechanism()
        due_purchases = self.dbmanager.get_due_purchases()
        self.insert_purchases_to_treeview(due_purchases)

    def insert_purchases_to_treeview(self, purchases):
        self.purchases_treeview.delete(*self.purchases_treeview.get_children())
        for i, purchase in enumerate(purchases):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.purchases_treeview.insert(
                "",
                tk.END,iid=purchase.id,
                values=(purchase.supplier.name, purchase.purchase_date.strftime("%d-%m-%Y"),
                        purchase.delivery_date.strftime("%d-%m-%Y"),
                        purchase.total_payable, purchase.paid, purchase.due, purchase.status), tags=tag)

    def get_purchases_by_search(self):
        filter_option = self.search_filter.get()

        if filter_option == "by_supplier":
            supplier_name = self.supplier_name_entry.get()
            purchases = self.dbmanager.get_purchases_by_supplier_name(supplier_name)
            if not purchases:
                messagebox.showerror(title="Not Found", message="No Purchase Found for This Supplier.")
                return
            self.insert_purchases_to_treeview(purchases)

        elif filter_option == "by_purchase_date":
            date = self.date_entry.get()
            day, month, year = date.split("-")
            delivery_date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
            purchases = self.dbmanager.get_purchases_by_purchase_date(delivery_date_obj)
            if not purchases:
                messagebox.showerror(title="Not Found", message="No Purchases Found for This Purchase Date")
                return
            self.insert_purchases_to_treeview(purchases)

        elif filter_option == "by_delivery_date":
            date = self.date_entry.get()
            day, month, year = date.split("-")
            delivery_date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
            purchases = self.dbmanager.get_purchases_by_delivery_date(delivery_date_obj)
            if not purchases:
                messagebox.showerror(title="Not Found", message="No Purchases Found for This Delivery Date.")
                return
            self.insert_purchases_to_treeview(purchases)

    def search_by_supplier(self):
        self.option_label.config(text="Supplier:")
        self.show_search_bar_entry_for_suppliers()

    def search_by_purchase_date(self):
        self.option_label.config(text="Purchase Date:")
        self.show_custom_date_search()

    def search_by_date_range(self):
        self.option_label.config(text="Delivery Date:")
        self.show_custom_date_search()

    def show_search_bar_entry_for_suppliers(self):
        self.date_entry.grid_remove()
        self.supplier_name_entry.grid()

    def show_custom_date_search(self):
        self.supplier_name_entry.grid_remove()
        self.date_entry.grid()

    def custom_search(self):
        self.purchases_treeview.delete(*self.purchases_treeview.get_children())
        self.enable_search_mechanism()

    def enable_search_mechanism(self):
        self.search_label.config(fg="white")
        self.option_label.config(fg="black")
        self.search_by_label.config(fg="black")
        self.by_supplier_radiobutton.config(state=tk.NORMAL)
        self.by_purchase_date_radiobutton.config(state=tk.NORMAL)
        self.by_delivery_date_radiobutton.config(state=tk.NORMAL)
        self.supplier_name_entry.config(state=tk.NORMAL)
        self.search_button.config(state=tk.NORMAL)
        self.date_entry.config(state=tk.NORMAL)

    def disable_search_mechanism(self):
        self.search_label.config(fg="gray")
        self.option_label.config(fg="gray")
        self.search_by_label.config(fg="gray")
        self.by_supplier_radiobutton.config(state=tk.DISABLED)
        self.by_purchase_date_radiobutton.config(state=tk.DISABLED)
        self.by_delivery_date_radiobutton.config(state=tk.DISABLED)
        self.supplier_name_entry.config(state=tk.DISABLED)
        self.search_button.config(state=tk.DISABLED)
        self.date_entry.config(state=tk.DISABLED)

    def view_purchases_items(self):
        purchased_products_toplevel = tk.Toplevel(self.purchases_treeview_frame)
        purchased_products_toplevel.resizable(False, False)
        self.center_window(purchased_products_toplevel, 500, 885)
        columns = ("Code", "Category", "Product Name", "Quantity", "Unit Type", "Unit Price", "Subtotal")
        purchased_products_list_treeview = ttk.Treeview(purchased_products_toplevel,
                                                   columns=columns,
                                                   show="headings",
                                                   height=14,
                                                   style="Treeview")

        purchased_products_list_treeview.tag_configure("evenrow", background="#f0f0f0")
        purchased_products_list_treeview.tag_configure("oddrow", background="#FFFFFF")

        for col in columns:
            purchased_products_list_treeview.heading(col, text=col)

        purchased_products_list_treeview.column("Code", width=85, stretch=False, )
        purchased_products_list_treeview.column("Category", width=85, stretch=False, )
        purchased_products_list_treeview.column("Product Name", width=310, stretch=False, )
        purchased_products_list_treeview.column("Quantity", width=85, stretch=False, anchor=tk.CENTER)
        purchased_products_list_treeview.column("Unit Type", width=85, stretch=False, anchor=tk.CENTER)
        purchased_products_list_treeview.column("Unit Price", width=85, stretch=False, anchor=tk.CENTER)
        purchased_products_list_treeview.column("Subtotal", width=85, stretch=False, anchor=tk.CENTER)

        purchased_products_list_treeview.grid(row=0, column=0, padx=(20, 0), pady=20)

        scrollbar = ttk.Scrollbar(purchased_products_toplevel, orient=tk.VERTICAL,
                                  command=purchased_products_list_treeview.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=(0, 20), pady=20)
        purchased_products_list_treeview.configure(yscrollcommand=scrollbar.set)

        purchase_id = self.purchases_treeview.selection()[0]
        purchase = self.dbmanager.get_purchase_by_id(purchase_id)
        for i, purchase_item in enumerate(purchase.items):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            purchased_products_list_treeview.insert("", tk.END, values=(purchase_item.product_code, purchase_item.product_category, purchase_item.product_name, purchase_item.quantity, purchase_item.unit_type, purchase_item.unit_price, purchase_item.subtotal), tags=tag)



    def pay_due_payment(self):
        selected_purchase_id = self.purchases_treeview.selection()[0]
        selected_invoice = self.purchases_treeview.item(selected_purchase_id, "values")
        due_amount = int(selected_invoice[-2])

        if due_amount == 0:
            messagebox.showinfo(title="No Due Payment", message="This invoice has no due payment.")
            return
        else:
            def update_purchase_with_due_payment():
                received_amount = int(payment_received_entry.get())
                if received_amount > purchase.due:
                    messagebox.showinfo(message="Received amount is greater than due amount. Check and try again!")
                    return
                purchase.paid += received_amount
                purchase.due -= received_amount
                self.dbmanager.update_changes()
                due_pay_win.destroy()
                self.refresh()

            due_pay_win = tk.Toplevel(self.purchases_treeview_frame)
            due_pay_win.title("Pay Due Payment")
            due_pay_win.config(padx=20, pady=20)

            self.center_window(due_pay_win, 215, 260)

            purchase_id = selected_purchase_id
            purchase = self.dbmanager.get_purchase_by_id(purchase_id)



            # Total Payable
            tk.Label(due_pay_win, text=f"Total Payable", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=0, sticky=tk.W)
            tk.Label(due_pay_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=1, sticky=tk.W)
            tk.Label(due_pay_win, text=f"{purchase.total_payable}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=2, sticky=tk.W)

            # Paid
            tk.Label(due_pay_win, text=f"Paid", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=0, sticky=tk.W)
            tk.Label(due_pay_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=1, sticky=tk.W)
            tk.Label(due_pay_win, text=f"{purchase.paid}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=2, sticky=tk.W)

            # Due
            tk.Label(due_pay_win, text=f"Due", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=0, sticky=tk.W)
            tk.Label(due_pay_win, text=":", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=1, sticky=tk.W)
            tk.Label(due_pay_win, text=f"{purchase.due}", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=2, sticky=tk.W)

            tk.Label(due_pay_win, text="Due Pay Amount", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4,
                                                                                                              column=0,
                                                                                                              sticky=tk.W)
            tk.Label(due_pay_win, text=":", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4, column=1,
                                                                                               sticky=tk.W)
            payment_received_entry = tk.Entry(due_pay_win, width=6, font=("Segoe UI", 12))
            payment_received_entry.focus_set()
            payment_received_entry.grid(row=4, column=2)
            tk.Button(due_pay_win, text="Confirm", command=update_purchase_with_due_payment).grid(row=5, column=1,
                                                                                                 columnspan=2,
                                                                                                 pady=10,
                                                                                                 sticky=tk.NSEW)
            due_pay_win.transient()
            due_pay_win.grab_set()  # modal behavior
            due_pay_win.resizable(False, False)

    def order_received(self):
        purchase_id = self.purchases_treeview.selection()[0]
        purchase = self.dbmanager.get_purchase_by_id(purchase_id)
        if not purchase.status == "Pending":
            messagebox.showinfo(title="Already Received", message="This Order has been Received")
            return

        purchase.status = "Received"
        for item in purchase.items:
            self.dbmanager.update_stock_of_product(item.product_code, item.quantity)
        messagebox.showinfo(title="Successful", message="Order Received Successfully!")
        self.refresh()


    def center_window(self, win, custom_height, custom_width):
        win.update_idletasks()
        width = custom_width
        height = custom_height
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def refresh(self):
        filter_option = self.filter_var.get()
        if filter_option == "all_purchases":
            self.all_purchases_radio_button.invoke()
        elif filter_option == "today_delivery":
            self.today_delivery_radio_button.invoke()
        elif filter_option == "due_purchases":
            self.due_purchases_radio_button.invoke()
        elif filter_option == "custom_search":
            self.search_button.invoke()
