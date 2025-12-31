import re
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import helpers

SHOP_NAME = "SHOP\nNAME"


class DashboardFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.configure(padx=20, pady=20)
        self.parent = parent
        self.dbmanager = dbmanager

        # Sales Today + Revenue Today + Total Due-----------------------------------------------------------------------
        self.sales_today = tk.IntVar(value=0)
        self.revenue_today = tk.IntVar(value=0)
        self.due_today = tk.IntVar(value=0)
        self.refund_today = tk.IntVar(value=0)
        self.balance = tk.IntVar(value=0)

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky=tk.W)
        tk.Label(top_frame,
                 text="Sales",
                 bg="#3498db",
                 fg="white",
                 width=10,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=0)
        tk.Label(top_frame,
                 textvariable=self.sales_today,
                 bg="#3498db",
                 fg="white",
                 height=1,
                 font=("Arial", 18, "bold"),
                 ).grid(row=1, column=0, sticky=tk.NSEW)

        tk.Label(top_frame,
                 text=f"Revenue",
                 bg="#C9A227",
                 fg="white",
                 width=10,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=1, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#C9A227",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.revenue_today,
                 bg="#C9A227",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=2, sticky=tk.NSEW)

        tk.Label(top_frame,
                 text=f"Due",
                 bg="#9b59b6",
                 fg="white",
                 width=10,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=3, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#9b59b6",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=3, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.due_today,
                 bg="#9b59b6",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=4, sticky=tk.NSEW)

        tk.Label(top_frame,
                 text=f"Return",
                 bg="#1abc9c",
                 fg="white",
                 width=10,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=5, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#1abc9c",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=5, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.refund_today,
                 bg="#1abc9c",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=6, sticky=tk.NSEW)

        tk.Label(top_frame,
                 text=f"Balance",
                 bg="#2c3e50",
                 fg="white",
                 width=13,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=7, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#2c3e50",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=7, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.balance,
                 bg="#2c3e50",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=8, sticky=tk.NSEW)

        # Product Selection Frame--------------------------------------------------------------------------------------------
        ## Upper Part
        product_selection_frame = tk.Frame(self, pady=20)
        product_selection_frame.grid(row=1, column=0)

        tk.Label(product_selection_frame,
                 text="Select Product:",
                 font=("Arial", 15),).grid(row=0, column=0, sticky=tk.W)

        self.product_name_combobox = ttk.Combobox(product_selection_frame, width=35, font=("Arial", 15))
        self.product_name_combobox.grid(row=0, column=1)

        tk.Label(product_selection_frame,
                 text="Quantity:",
                 font=Font(size=15),).grid(row=0, column=2)

        self.quantity = tk.Spinbox(product_selection_frame, from_=1, to=100000, font=("Arial", 15), width=7,
                                   validate="key",
                                   validatecommand=(product_selection_frame.register(helpers.is_digit), "%P"))
        self.quantity.grid(row=0, column=3)

        ttk.Button(product_selection_frame, text="Add", command=self.add_item).grid(row=0, column=4)

        ## Lower Part
        columns = ("Product Name", "Unit Price", "Quantity", "Subtotal")
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

        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=16,
                                                   style="Treeview")
        self.product_entry_treeview.bind("<Double-1>", self.edit_unit_price)
        self.product_entry_treeview.bind("<Button-3>", self.show_menu)

        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)

        self.product_entry_treeview.column("Product Name", width=524, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=100, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Quantity", width=100, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Subtotal", width=100, stretch=False, anchor=tk.CENTER)

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        # Logo Frame----------------------------------------------------------------------------------------------------
        logo_frame = tk.Frame(self, highlightbackground="black", highlightthickness=2)
        logo_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=(20, 0))

        tk.Label(logo_frame,
                 text=SHOP_NAME,
                 font=("Arial Black", 15, "bold"), padx=70, anchor=tk.CENTER).grid(row=0, column=0, sticky=tk.NSEW)

        # Invoice Making Frame--------------------------------------------------------------------------------------------
        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=1, column=1, sticky=tk.N, padx=(20, 0), pady=(20, 0))

        tk.Label(invoice_frame,
                 text="Total Items",
                 font=("Arial", 16, "bold"),
                 anchor=tk.W
                 ).grid(row=0, column=0, sticky=tk.W)
        tk.Label(invoice_frame,
                 text=":",
                 font=("Arial", 16, "bold"),
                 anchor=tk.W
                 ).grid(row=0, column=1)
        self.total_items = tk.IntVar(value=0)

        tk.Label(invoice_frame,
                 textvariable=self.total_items,
                 fg="white",
                 bg="black",
                 font=("Arial", 16, "bold"),
                 anchor=tk.E, ).grid(row=0, column=2, sticky=tk.NSEW)

        self.mrp_total = tk.IntVar(value=0)
        self.total = tk.IntVar(value=0)

        # MRP Total
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=1, column=0, columnspan=3, pady=(21, 0),
                                                               sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="MRP Total",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=2, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=2, column=1, sticky=tk.NSEW)

        tk.Label(invoice_frame,
                 textvariable=self.mrp_total,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 width=6,
                 anchor=tk.E).grid(row=2, column=2, sticky=tk.NSEW)

        # (-) Discount
        tk.Label(invoice_frame,
                 text="(-) Discount)",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W).grid(row=3, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 ).grid(row=3, column=1, sticky=tk.NSEW)

        self.discount_entry = tk.Entry(invoice_frame,
                                       width=6,
                                       highlightbackground="#2c3e50",
                                       highlightthickness=1,
                                       highlightcolor="#2c3e50",
                                       font=("Segoe UI", 12),
                                       justify=tk.RIGHT, )

        self.discount_entry.insert(tk.END, "0")
        self.discount_entry.grid(row=3, column=2, sticky=tk.EW)

        # Total Payable
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=4, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="Total Payable",
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.W,
                 fg="white").grid(row=5, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=5, column=1, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 textvariable=self.total,
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.E,
                 width=6,
                 fg="white").grid(row=5, column=2, sticky=tk.NSEW)

        self.payment_methods_treeview = ttk.Treeview(invoice_frame,
                                                     columns=("Payment Method", "Amount"),
                                                     show="headings",
                                                     height=1)
        data = [("Cash Received", 0), ("Bkash", 0), ("Nagad", 0), ("Card/Bank", 0)]
        for item in data:
            self.payment_methods_treeview.insert("", tk.END, values=item)
        self.payment_methods_treeview.grid(row=6, column=0, columnspan=3)
        self.payment_methods_treeview.bind("<Double-1>", self.edit_payment_amount)

        # It has to be here because of self.update_total method.
        # In self.update_total method there is another method called self.calculate_change_due(called inside of self.update_total).
        # In self.calculate change due we referred self.payment_methods_treeview
        self.discount_entry.config(validate="key", validatecommand=(invoice_frame.register(self.update_total), "%P"))

        self.payment_methods_treeview.column("Payment Method", width=158, stretch=tk.NO)
        self.payment_methods_treeview.column("Amount", width=96, stretch=tk.NO, anchor=tk.E)
        self.payment_methods_treeview.heading("Payment Method", text="Payment Type")
        self.payment_methods_treeview.heading("Amount", text="Amount")
        # Total Paid + Change + Due-------------------------------------------------------------------------------------

        ## Total Paid
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=7, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="Paid",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W,
                 fg="white").grid(row=8, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=8, column=1, sticky=tk.NSEW)
        self.paid = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.paid,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E, ).grid(row=8, column=2, sticky=tk.NSEW)

        ## Change
        tk.Label(invoice_frame,
                 text="Change",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W).grid(row=9, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=9, column=1, sticky=tk.NSEW)
        self.change = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.change,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=9, column=2, sticky=tk.NSEW)

        ## Due
        tk.Label(invoice_frame,
                 text="Due",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=10, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50", font=("Segoe UI", 12),
                 fg="white").grid(
            row=10, column=1, sticky=tk.NSEW)
        self.due = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.due,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=10, column=2, sticky=tk.NSEW)

        # Customer Details Frame
        customer_details_frame = tk.Frame(invoice_frame)
        customer_details_frame.grid(row=11, column=0, columnspan=3, pady=20, sticky=tk.NSEW)

        tk.Label(customer_details_frame,
                 text="Customer Phone",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.customer_phone_entry = tk.Entry(customer_details_frame, validate="key",
                                             validatecommand=(
                                                 customer_details_frame.register(helpers.validate_phonenumber),
                                                 "%P",),
                                             font=("Segoe UI", 12))
        self.customer_phone_entry.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        ttk.Button(customer_details_frame,
                   text="Search",
                   width=7,
                   command=self.search_customer).grid(row=0, column=2, rowspan=2, padx=(15, 0), sticky=tk.NS)

        tk.Label(customer_details_frame,
                 text="Customer Name",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12), ).grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=tk.NSEW)
        self.customer_name_entry = tk.Entry(customer_details_frame, font=("Segoe UI", 12))
        self.customer_name_entry.grid(row=3, column=0, columnspan=3, sticky=tk.EW)

        tk.Label(customer_details_frame,
                 text="Customer Address",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=4, column=0, columnspan=3, pady=(10, 0), sticky=tk.NSEW)
        self.customer_address_entry = tk.Text(customer_details_frame, height=2, width=20, font=("Segoe UI", 12))
        self.customer_address_entry.grid(row=5, column=0, columnspan=3, sticky=tk.EW)

        ttk.Button(customer_details_frame,
                   text="PRINT",
                   command=self.print_invoice).grid(row=6, column=0, columnspan=3, pady=(32, 0), sticky=tk.EW)

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

    def edit_payment_amount(self, event):
        # Detect row and column
        region = self.payment_methods_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.payment_methods_treeview.identify_row(event.y)
        column = self.payment_methods_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1
        # Return, if column is not Amount Column
        if not col_index == 1:
            return

        x, y, width, height = self.payment_methods_treeview.bbox(row_id, column)

        # Current value
        value = self.payment_methods_treeview.item(row_id, "values")[col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.payment_methods_treeview, font=("Segoe UI", 12), justify=tk.RIGHT)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit():
            new_val = entry.get()
            values = list(self.payment_methods_treeview.item(row_id, "values"))
            values[col_index] = new_val
            self.payment_methods_treeview.item(row_id, values=values)
            entry.destroy()
            self.calculate_change_due()

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def edit_unit_price(self, event):
        # Detect row and column
        region = self.product_entry_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_entry_treeview.identify_row(event.y)
        column = self.product_entry_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1
        # Return, if column is not Amount Column
        if not col_index == 1:
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
            values[-1] = str(int(values[col_index]) * int(values[2]))
            self.product_entry_treeview.item(row_id, values=values)
            entry.destroy()
            self.update_calculation()

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def add_item(self):
        product_to_add = self.product_name_combobox.get()
        quantity = int(self.quantity.get())

        product = self.dbmanager.get_product_by_name(product_to_add)
        if not product:
            messagebox.showerror("Not Found", "This product doesn't exist!")

        if product.stock < quantity:
            messagebox.showinfo(title="Insufficient Stock",
                                message=f"Current stock of {product.name} is {product.stock}! ")
            return

        subtotal = int(product.unit_price) * quantity
        try:
            self.product_entry_treeview.insert("", tk.END, iid=product.id,
                                               values=(product.name, product.unit_price, quantity, subtotal),
                                               tags="product_entry_row")
        except tk.TclError:
            messagebox.showinfo("Duplicate Found", f"{product.name} already taken!")
        self.update_calculation()

    def update_calculation(self):
        # Update Total Items
        total_item = len(self.product_entry_treeview.get_children())
        self.total_items.set(total_item)
        # Update MRP Total
        mrp_total_list = [int(self.product_entry_treeview.item(item, "values")[3]) for item in
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
        self.calculate_change_due()
        return True

    def calculate_change_due(self):
        payment_from_all_methods = [int(self.payment_methods_treeview.item(item, "values")[1]) for item in
                                    self.payment_methods_treeview.get_children()]
        total_amount_has_given = sum(payment_from_all_methods)

        self.paid.set(total_amount_has_given)

        if self.total.get() < total_amount_has_given:
            self.change.set(total_amount_has_given - self.total.get())
            self.due.set(0)
        else:
            self.due.set(self.total.get() - total_amount_has_given)
            self.change.set(0)

    def refresh(self):
        # Updates amounts in Dashboard
        all_sales = self.dbmanager.get_all_sales()
        today_sales = self.dbmanager.get_today_sales()

        revenue_today = 0
        due_today = 0
        refund_today = 0
        for sale in today_sales:
            revenue_today += sale.total_payable
            due_today += sale.due
            for item in sale.items:
                for refund in item.refunds:
                    refund_today += refund.refund_amount

        self.sales_today.set(len(today_sales))
        self.revenue_today.set(revenue_today)
        self.due_today.set(due_today)
        self.refund_today.set(int(refund_today)) # Fix it in the database(pending)
        self.balance.set(self.revenue_today.get() - (self.due_today.get() + self.refund_today.get()))

        # Resets Product Name List
        self.product_name_combobox.config(values=self.dbmanager.get_all_products_name())
        try:
            self.product_name_combobox.current(0)
        except tk.TclError:
            pass

        # Deletes all item in the Product Entry Treeview
        self.delete_item(self.product_entry_treeview.get_children())

        # Resets Payment Methods Treeview Amounts
        # It has to be before clearing discount_entry
        for row_id in self.payment_methods_treeview.get_children():
            values = list(self.payment_methods_treeview.item(row_id, "values"))
            values[1] = "0"
            self.payment_methods_treeview.item(row_id, values=values)

        # Clears all entries
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        self.customer_phone_entry.config(bg="white")
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.customer_address_entry.delete("1.0", tk.END)

    def search_customer(self):
        customer_phone = self.customer_phone_entry.get()
        is_valid_phone_number = bool(re.fullmatch(r'^01[3-9]\d{8}$', customer_phone))
        if not is_valid_phone_number:
            messagebox.showerror("Error", "Provide a valid phone number!")
            return

        if customer_phone:
            customer = self.dbmanager.get_customer_by_phone(customer_phone)
            if customer:
                self.customer_phone_entry.config(bg="green")

                self.customer_name_entry.delete(0, tk.END)  # Removes everything if previously exists anything
                self.customer_name_entry.insert(tk.END, customer.name)

                self.customer_address_entry.delete("1.0", tk.END)
                self.customer_address_entry.insert(tk.END, customer.address)
            else:
                self.customer_phone_entry.config(bg="red")
                self.customer_name_entry.delete(0, tk.END)
                self.customer_address_entry.delete("1.0", tk.END)

    def print_invoice(self):
        if not self.product_entry_treeview.get_children():
            messagebox.showerror(title="Error", message="Please add products to print invoice.")
            return
        current_customer_phone = self.customer_phone_entry.get()
        if current_customer_phone:
            current_customer = self.dbmanager.get_customer_by_phone(current_customer_phone)
            if not current_customer:
                # Make Customer
                current_customer = self.dbmanager.Customer(
                    name=self.customer_name_entry.get(),
                    phone=self.customer_phone_entry.get(),
                    address=self.customer_address_entry.get("1.0", tk.END),
                )
                # Add Customer
                self.dbmanager.add_customer(current_customer)
        else:
            current_customer = self.dbmanager.get_customer_by_phone("01700000000")

        # Make Invoice
        # Add products to invoice
        invoice = self.dbmanager.Invoice(
            customer_id=current_customer.phone,
            mrp_total=self.mrp_total.get(),
            discount=self.discount_entry.get(),
            total_payable=self.total.get(),
            paid=self.paid.get(),
            change=self.change.get(),
            due=self.due.get(),
        )
        for row_id in self.product_entry_treeview.get_children():
            product_name, unit_price, quantity, subtotal = self.product_entry_treeview.item(row_id, "values")

            # Male SaleItem for each product
            saleitem = self.dbmanager.SaleItem(
                product_id=row_id,
                product_name=product_name,
                unit_price=int(unit_price),
                quantity=int(quantity),
                subtotal=int(subtotal),
            )
            # Add SaleItem to invoice
            invoice.items.append(saleitem)
            # Adjust stock while looping over through the TreeView
            self.dbmanager.adjust_stock_of_product(saleitem.product_id, saleitem.quantity)

        self.dbmanager.add_purchase(invoice)
        ready_invoice = helpers.make_invoice_for_purchase(invoice)
        helpers.print_out_invoice(ready_invoice)
        self.refresh()
