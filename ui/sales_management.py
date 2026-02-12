import datetime
import math
import re
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk, messagebox

from pandas.core.tools.datetimes import should_cache
from sqlalchemy.testing.plugin.plugin_base import final_process_cleanup
from tkcalendar import DateEntry
from utils import helpers


class NewSaleFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.configure(padx=20, pady=20)
        self.parent = parent
        self.dbmanager = dbmanager

        # Product Selection Frame--------------------------------------------------------------------------------------------
        ## Upper Part
        product_selection_frame = tk.Frame(self)
        product_selection_frame.grid(row=0, column=0)

        tk.Label(product_selection_frame,
                 text="Select Product:",
                 font=("Arial", 15),).grid(row=0, column=0, sticky=tk.W)

        self.product_name_search_entry = helpers.AutoCompleteEntry(product_selection_frame, db_path="database/database.db", font=("Arial", 15), width=35)
        self.product_name_search_entry.grid(row=0, column=1)

        tk.Label(product_selection_frame,
                 text="Quantity:",
                 font=Font(size=15),).grid(row=0, column=2)

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


        columns = ("Code", "Category", "Product Name", "Qty", "Unit", "Base Qty", "Rate", "Subtotal")
        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=19,
                                                   style="Treeview")

        # Menu Options for Treeview
        self.menu = tk.Menu(product_selection_frame, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_item)
        self.product_entry_treeview.bind("<Button-3>", self.show_menu)
        self.product_entry_treeview.bind("<Double-1>", self.edit_unit_price)
        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)

        self.product_entry_treeview.column("Code", width=85, stretch=False, )
        self.product_entry_treeview.column("Category", width=80, stretch=False, )
        self.product_entry_treeview.column("Product Name", width=300, stretch=False, )
        self.product_entry_treeview.column("Qty", width=70, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Unit", width=50, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Base Qty", width=85, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Rate", width=60, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Subtotal", width=85, stretch=False, anchor=tk.CENTER)

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        # Invoice Making Frame--------------------------------------------------------------------------------------------
        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=0, column=1, sticky=tk.N, padx=(20, 0))

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


        # It has to be here because of self.update_total method.
        # In self.update_total method there is another method called self.calculate_change_due(called inside of self.update_total).
        # In self.calculate change due we referred self.payment_methods_treeview
        self.discount_entry.config(validate="key", validatecommand=(invoice_frame.register(self.update_total), "%P"))

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
        self.paid_entry = tk.Entry(invoice_frame,
            width=6,
            highlightbackground="#2c3e50",
            highlightthickness=1,
            highlightcolor="#2c3e50",
            font=("Segoe UI", 12),
            justify=tk.RIGHT,
        )
        self.paid_entry.grid(row=8, column=2, sticky=tk.NSEW)
        self.paid_entry.insert(tk.END, "0")
        self.paid_entry.config(validate="key", validatecommand=(invoice_frame.register(self.calculate_change_due), "%P"))


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
                   text="Make Sale",
                   command=self.make_sale).grid(row=6, column=0, columnspan=3, pady=(32, 0), sticky=tk.EW)

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
        if col_index == 0 or col_index == 1 or col_index == 2  or col_index == 4 or col_index == 6:
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
            values[-1] = str(int(values[3]) * int(values[5]))
            self.product_entry_treeview.item(row_id, values=values)
            entry.destroy()
            self.update_calculation()

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def add_item(self):
        product_code = self.product_name_search_entry.get().split("-")[0].strip()

        product = self.dbmanager.get_product_by_code(product_code)
        if not product:
            messagebox.showerror("Not Found", "This product doesn't exist!")

        if product.category == "Pipe":
            final_quantity, base_qty = helpers.calculate_base_stock_for_pipe(product, int(self.quantity.get()))
            subtotal = int(product.sell_unit_price) * final_quantity
            values = (product.code, product.category, product.name,final_quantity,product.sell_unit_type, base_qty,
                      product.sell_unit_price, subtotal)
        elif product.category == "Tiles":
            final_quantity, base_stock = helpers.calculate_base_stock_for_tiles(product, int(self.quantity.get()))
            subtotal = int(product.sell_unit_price) * final_quantity
            values = (product.code, product.category, product.name,
                      final_quantity, product.sell_unit_type, base_stock,
                      product.sell_unit_price, subtotal)
        else:
            quantity = int(self.quantity.get())
            subtotal = product.sell_unit_price * quantity
            values = (product.code, product.category, product.name,
                      quantity, product.sell_unit_type, quantity,
                      product.sell_unit_price, subtotal)




        try:
            self.product_entry_treeview.insert("", tk.END, iid=product.code,
                                               values=values,
                                               tags="product_entry_row")
        except tk.TclError:
            messagebox.showinfo("Duplicate Found", f"{product.name} already taken!")
        self.update_calculation()
        self.product_name_search_entry.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.quantity.insert(tk.END, "1")

    def update_calculation(self):
        # Update Total Items
        total_item = len(self.product_entry_treeview.get_children())
        self.total_items.set(total_item)
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
        self.calculate_change_due(self.paid_entry.get())
        return True

    def calculate_change_due(self, paid_amount):
        if paid_amount == "":
            paid_amount = "0"

        if not paid_amount.isdigit():
            return False  # block anything that's not a number

        paid_amount = int(paid_amount) # Converting str to int
        if self.total.get() < paid_amount:
            self.change.set(paid_amount - self.total.get())
            self.due.set(0)
        else:
            self.due.set(self.total.get() - paid_amount)
            self.change.set(0)

        return True

    def refresh(self):
        # Deletes all item in the Product Entry Treeview
        self.delete_item(self.product_entry_treeview.get_children())


        # Clears all entries
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        self.paid_entry.delete(0, tk.END)
        self.paid_entry.insert(0, "0")
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

    def make_sale(self):
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


        # Make Sale
        sale = self.dbmanager.Invoice(
            customer_id=current_customer.phone,
            mrp_total=self.mrp_total.get(),
            discount=self.discount_entry.get(),
            total_payable=self.total.get(),
            paid=self.paid_entry.get(),
            change=self.change.get(),
            due=self.due.get(),
        )

        # Add products to Sale
        for row_id in self.product_entry_treeview.get_children():
            code, category, product_name, quantity, unit_type, base_qty, unit_price, subtotal = self.product_entry_treeview.item(row_id, "values")

            # Male SaleItem for each product
            saleitem = self.dbmanager.SaleItem(
                product_code=int(code),
                product_category=category,
                product_name=product_name,
                quantity=int(quantity),
                unit_type=unit_type,
                base_qty=base_qty,
                unit_price=int(unit_price),
                subtotal=int(subtotal),
            )
            # Add SaleItem to invoice
            sale.items.append(saleitem)
            # Adjust stock while looping over through the TreeView
            self.dbmanager.adjust_stock_of_product(saleitem.product_code, saleitem.quantity)

        self.dbmanager.add_purchase(sale)

        should_print_invoice = messagebox.askyesno(title="Invoice Print", message="Do you want to print invoice?")
        if should_print_invoice:
            ready_invoice = helpers.make_invoice_for_purchase(sale)
            helpers.print_out_invoice(ready_invoice)
        self.refresh()

class RefundFrame:
    def __init__(self, parent, invoice, dbmanager):
        self.parent = parent
        self.invoice = invoice
        self.dbmanager = dbmanager

        product_selection_frame = tk.Frame(parent)
        product_selection_frame.grid(row=1, column=0)

        tk.Label(product_selection_frame, text=f"Invoice: {invoice.id}", font=("Arial", 15), ).grid(row=0, column=0,
                                                                                                    sticky=tk.W)
        tk.Label(product_selection_frame, text=f"Date: {invoice.date.strftime("%d-%m-%Y")}", font=("Arial", 15), ).grid(
            row=0, column=1, padx=20)
        tk.Label(product_selection_frame, text=f"Time: {invoice.time.strftime("%I:%M %p")}", font=("Arial", 15), ).grid(
            row=0, column=2, padx=20)
        tk.Label(product_selection_frame, text=f"Customer: {invoice.customer.name}-{invoice.customer.phone}",
                 font=("Arial", 15), ).grid(row=0, column=3)
        columns = ("Code", "Product Name", "Sold Qty","Unit Type", "Unit Price",  "Returned Qty(P)", "Returned Qty(N)", "Refund")
        product_entry_treeview_style = ttk.Style(product_selection_frame)
        product_entry_treeview_style.configure("Treeview",
                                                   font=("Segoe UI", 12),
                                                   rowheight=30,
                                                   borderwidth=0,
                                                   highlightthickness=0)
        product_entry_treeview_style.configure("Treeview.Heading",
                                                   background="#e0e0e0",
                                                   foreground="black",
                                                   font=("Segoe UI", 12, "bold"))


        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=10,
                                                   style="Treeview")
        self.product_entry_treeview.bind("<Double-1>", self.edit_cell)
        self.product_entry_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.product_entry_treeview.tag_configure("oddrow", background="#FFFFFF")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)
        self.product_entry_treeview.column("Code", width=85, stretch=False, )
        self.product_entry_treeview.column("Product Name", width=320, stretch=False, )
        self.product_entry_treeview.column("Sold Qty", width=85, stretch=False, )
        self.product_entry_treeview.column("Unit Type", width=85, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=85, stretch=False, )
        self.product_entry_treeview.column("Returned Qty(P)", width=140, stretch=False, )
        self.product_entry_treeview.column("Returned Qty(N)", width=140, stretch=False, )
        self.product_entry_treeview.column("Refund", width=85, stretch=False, )

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        total_items_frame = tk.Frame(product_selection_frame)
        total_items_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        total_items_frame = tk.Frame(product_selection_frame)
        total_items_frame.grid(row=2, column=2, columnspan=3, sticky=tk.E)
        tk.Label(total_items_frame, text="Total Refund Amount:", font=("Arial", 16, "bold"), ).grid(row=2, column=0,
                                                                                                        sticky=tk.W)
        self.total_refund_amount = tk.IntVar(value=0)
        tk.Label(total_items_frame, textvariable=self.total_refund_amount, font=("Arial", 16, "bold"), ).grid(row=2, column=1, sticky=tk.W)

        ttk.Button(product_selection_frame, text="Confirm", command=self.adjust_stocks_for_returned_products).grid(
            row=3, column=4, pady=(40, 0), sticky=tk.E)
        self.load_products()

    def load_products(self):
        for i, item in enumerate(self.invoice.items):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            previous_returns = sum([refund.refund_quantity for refund in item.refunds])
            self.product_entry_treeview.insert("", tk.END, iid=item.id,
                                               values=(item.product_code, item.product_name,item.quantity,item.unit_type,
                                                       item.unit_price, previous_returns, 0, 0), tags=tag)

    def edit_cell(self, event):
        # Detect row and column
        region = self.product_entry_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_entry_treeview.identify_row(event.y)
        column = self.product_entry_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1

        if not col_index == 6:
            return

        x, y, width, height = self.product_entry_treeview.bbox(row_id, column)

        # Current value
        value = self.product_entry_treeview.item(row_id, "values")[col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.product_entry_treeview, font=("Segoe UI", 12))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event=None):
            new_val = entry.get()
            values = list(self.product_entry_treeview.item(row_id, "values"))

            available_product_to_return = int(values[2]) - int(values[5])
            if int(new_val) > available_product_to_return:
                messagebox.showwarning(title="Return Limit Exceeded",
                                     message="The return quantity cannot exceed the sold quantity.")
                return
            values[col_index] = new_val  # Implements Changes

            # Update return subtotal
            values[-1] = str(int(values[4]) * int(values[col_index]))
            # Update Product in the TreeView
            self.product_entry_treeview.item(row_id, values=values)

            # Update total refund
            total_refund = 0
            for item in self.product_entry_treeview.get_children():
                total_refund += int(self.product_entry_treeview.item(item, "values")[-1])
            self.total_refund_amount.set(total_refund)


            entry.destroy()

        entry.bind("<Return>", save_edit)
        #entry.bind("<FocusOut>", save_edit)

    def adjust_stocks_for_returned_products(self):
        for row_id in self.product_entry_treeview.get_children():
            values = self.product_entry_treeview.item(row_id, "values")

            # Update product stock in the database
            product_code, refund_quantity = values[0], values[-2]
            self.dbmanager.update_stock_of_product(product_code, refund_quantity)

            # Add refund history to the SaleItem
            saleitem = self.dbmanager.get_saleitem(row_id)
            refund_history = self.dbmanager.Refund(
                refund_quantity=refund_quantity,
                refund_amount=saleitem.unit_price * int(refund_quantity),
            )
            saleitem.refunds.append(refund_history)
            self.dbmanager.update_changes()
        self.parent.destroy()

class SalesFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.dbmanager = dbmanager
        self.filter_var = tk.StringVar(value="all")
        # Options Frame ------------------------------------------------------------------------------------------------
        options_frame = tk.Frame(self, padx=20, pady=20)
        options_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.all_radio_button = tk.Radiobutton(options_frame, text="All", width=10, fg="white", bg="#3498db",
                                               command=self.all_invoices, font=("Arial", 15),
                                               activeforeground="white", activebackground="#1abc9c",
                                               selectcolor="#1abc9c",
                                               variable=self.filter_var, value="all", indicatoron=False, height=3)
        self.all_radio_button.grid(row=0, column=0, sticky=tk.NSEW)

        self.today_radio_button = tk.Radiobutton(options_frame, text="Today", width=10,
                                                 fg="white", bg="#3498db", command=self.today_invoices,
                                                 activeforeground="white", font=("Arial", 15),
                                                 activebackground="#1abc9c", selectcolor="#1abc9c",
                                                 variable=self.filter_var,
                                                 value="today", indicatoron=False, height=3)

        self.today_radio_button.grid(row=0, column=1, sticky=tk.NSEW)

        self.due_radio_button = tk.Radiobutton(options_frame, text="Due", width=10,
                                               fg="white", bg="#3498db", command=self.due_invoices,
                                               activeforeground="white", font=("Arial", 15),
                                               activebackground="#1abc9c", selectcolor="#1abc9c",
                                               variable=self.filter_var,
                                               value="due", indicatoron=False, height=3)
        self.due_radio_button.grid(row=0, column=2, sticky=tk.NSEW)
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

        self.search_filter = tk.StringVar(value="by_invoice")
        self.by_invoice_radiobutton = tk.Radiobutton(custom_search, text="Invoice", fg="white", bg="#3498db",
                                                     activeforeground="white", width=8, font=("Segoe UI", 10),
                                                     activebackground="#1abc9c", selectcolor="#1abc9c",
                                                     variable=self.search_filter,
                                                     value="by_invoice", command=self.search_by_invoice,
                                                     indicatoron=False)
        self.by_invoice_radiobutton.grid(row=1, column=1, pady=10, sticky=tk.W)
        self.by_phone_radiobutton = tk.Radiobutton(custom_search, text="Phone", fg="white", bg="#3498db",
                                                   activeforeground="white", width=8, font=("Segoe UI", 10),
                                                   activebackground="#1abc9c", selectcolor="#1abc9c",
                                                   variable=self.search_filter,
                                                   value="by_phone", command=self.search_by_phone, indicatoron=False)
        self.by_phone_radiobutton.grid(row=1, column=2, pady=10, sticky=tk.W)
        self.by_date_radiobutton = tk.Radiobutton(custom_search, text="Date", fg="white", bg="#3498db",
                                                  activeforeground="white", width=8, font=("Segoe UI", 10),
                                                  activebackground="#1abc9c", selectcolor="#1abc9c",
                                                  variable=self.search_filter,
                                                  value="by_date", command=self.search_by_date_range, indicatoron=False)
        self.by_date_radiobutton.grid(row=1, column=3, pady=10, padx=(0, 8), sticky=tk.W)
        self.option_label = tk.Label(custom_search, text="Invoice Number:", width=13, font=("Segoe UI", 10),
                                     anchor=tk.E, )
        self.option_label.grid(row=2, column=0, pady=(0, 10), padx=(7, 0), sticky=tk.E)

        self.invoice_or_phone_entry = tk.Entry(custom_search, width=10, font=("Segoe UI", 10), )
        self.invoice_or_phone_entry.grid(row=2, column=1, columnspan=2, pady=(0, 10), sticky=tk.EW)
        self.date_entry = DateEntry(
            custom_search,
            date_pattern="dd-mm-yyyy",
            width=18,
            showweeknumbers=False,
            background="#2c3e50",
            foreground="white",
            selectbackground="#1a252f",
        )
        self.date_entry.grid(row=2, column=1, pady=(0, 10), columnspan=2)
        self.date_entry.grid_remove()

        self.search_button = tk.Button(custom_search, text="Get", font=("Segoe UI", 8),
                                       command=self.get_invoice_by_search)
        self.search_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 8), sticky=tk.EW)

        # Sales Treeview Frame------------------------------------------------------------------------------------------
        self.sales_treeview_frame = tk.Frame(self)
        self.sales_treeview_frame.grid(row=1, column=0, sticky=tk.N)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)
        self.menu.add_command(label="Receive Payment", command=self.receive_payment)
        self.menu.add_command(label="Sales Return", command=self.sales_return)

        columns = ("Invoice", "Date", "Time", "Customer", "Amount", "Due")
        self.sales_treeview = ttk.Treeview(self.sales_treeview_frame, columns=columns, show="headings", height=16)

        self.sales_treeview.bind("<<TreeviewSelect>>", self.view_invoice)
        for col in columns:
            self.sales_treeview.heading(col, text=col)
        self.sales_treeview.column("Invoice", width=90, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Date", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Time", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Customer", width=300, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Amount", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Due", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.sales_treeview.tag_configure("oddrow", background="#FFFFFF")
        self.sales_treeview.grid(row=0, column=0, padx=(20, 0), sticky=tk.N)

        sales_treeview_scrollbar = ttk.Scrollbar(self.sales_treeview_frame, orient=tk.VERTICAL,
                                                 command=self.sales_treeview.yview)
        sales_treeview_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.sales_treeview.configure(yscrollcommand=sales_treeview_scrollbar.set)
        self.sales_treeview.bind("<Button-3>", self.show_menu)

        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=1, column=1, sticky=tk.NSEW)

        self.invoice_text = tk.Text(invoice_frame, width=55, height=55, font=("Courier New", 6), bd=2, )
        self.invoice_text.grid(row=0, column=0, padx=(20, 0))
        invoice_scrollbar = ttk.Scrollbar(invoice_frame, orient=tk.VERTICAL, command=self.invoice_text.yview)
        invoice_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.invoice_text.config(yscrollcommand=invoice_scrollbar.set)

        ttk.Button(invoice_frame, text="PRINT", command=self.print_invoice).grid(row=1, column=0, padx=(20, 0),
                                                                                 pady=(15, 0), sticky=tk.EW)

        self.all_radio_button.invoke()

    def show_menu(self, event):
        iid = self.sales_treeview.identify_row(event.y)
        if iid:
            self.sales_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def all_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        invoices = self.dbmanager.get_all_sales()[::-1]
        self.show_invoice(invoices)

    def today_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        invoices = self.dbmanager.get_today_sales()[::-1]
        self.show_invoice(invoices)

    def due_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        due_invoices = [invoice for invoice in self.dbmanager.get_all_sales()[::-1] if invoice.due > 0]
        self.show_invoice(due_invoices)

    def custom_search(self):
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        self.enable_search_mechanism()

    def enable_search_mechanism(self):
        self.search_label.config(fg="white")
        self.option_label.config(fg="black")
        self.search_by_label.config(fg="black")
        self.by_invoice_radiobutton.config(state=tk.NORMAL)
        self.by_phone_radiobutton.config(state=tk.NORMAL)
        self.by_date_radiobutton.config(state=tk.NORMAL)
        self.invoice_or_phone_entry.config(state=tk.NORMAL)
        self.search_button.config(state=tk.NORMAL)
        self.date_entry.config(state=tk.NORMAL)

    def disable_search_mechanism(self):
        self.search_label.config(fg="gray")
        self.option_label.config(fg="gray")
        self.search_by_label.config(fg="gray")
        self.by_invoice_radiobutton.config(state=tk.DISABLED)
        self.by_phone_radiobutton.config(state=tk.DISABLED)
        self.by_date_radiobutton.config(state=tk.DISABLED)
        self.invoice_or_phone_entry.config(state=tk.DISABLED)
        self.search_button.config(state=tk.DISABLED)
        self.date_entry.config(state=tk.DISABLED,)

    def view_invoice(self, event):
        selected_item = self.sales_treeview.selection()[0]
        invoice_id = self.sales_treeview.item(selected_item, "values")[0]
        invoice = self.dbmanager.get_invoice(invoice_id)
        ready_invoice = helpers.make_invoice_for_purchase(invoice)

        self.invoice_text.config(state=tk.NORMAL)
        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert("1.0", ready_invoice)
        self.invoice_text.config(state=tk.DISABLED)

    def print_invoice(self):
        invoice = self.invoice_text.get("1.0", tk.END)
        if invoice == "\n":
            messagebox.showerror(title="Error", message="Please select an invoice to print!")
            return

        helpers.print_out_invoice(invoice)

    def show_invoice(self, invoices):
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        for i, invoice in enumerate(invoices):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.sales_treeview.insert(
                "",
                tk.END,
                values=(invoice.id, invoice.date.strftime("%d-%m-%Y"), invoice.time.strftime("%I:%M %p"),
                        f"{invoice.customer.name} - {invoice.customer.phone}",
                        invoice.total_payable, invoice.due), tags=tag)

    def get_invoice_by_search(self):
        filter_option = self.search_filter.get()

        if filter_option == "by_invoice":
            invoice_no = self.invoice_or_phone_entry.get()
            invoice = self.dbmanager.get_invoice(invoice_no)
            if not invoice:
                messagebox.showerror(title="Not Found", message="No invoice found with this invoice number.")
                return
            self.show_invoice([invoice])

        elif filter_option == "by_phone":
            phone_number = self.invoice_or_phone_entry.get()
            customer = self.dbmanager.get_customer_by_phone(phone_number)
            if not customer:
                messagebox.showerror(title="Not Found", message="No invoices found with this phone number.")
                return
            purchases_of_the_customer = customer.purchases
            self.show_invoice(purchases_of_the_customer)

        elif filter_option == "by_date":
            date = self.date_entry.get()
            day, month, year = date.split("-")
            date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
            invoices = self.dbmanager.get_invoices_by_date(date_obj)
            if not invoices:
                messagebox.showerror(title="Not Found", message="No invoices found for this date.")
                return
            self.show_invoice(invoices)

    def receive_payment(self):
        selected_invoice_id = self.sales_treeview.selection()[0]
        selected_invoice = self.sales_treeview.item(selected_invoice_id, "values")
        due_amount = int(selected_invoice[-1])

        if due_amount == 0:
            messagebox.showinfo(title="No Due Payment", message="This invoice has no due payment.")
            return
        else:
            def update_invoice_with_new_payment():
                received_amount = int(payment_received_entry.get())
                if received_amount > invoice.due:
                    messagebox.showinfo(message="Received amount is greater than due amount. Check and try again!")
                    return
                invoice.paid += received_amount
                invoice.due -= received_amount
                self.dbmanager.update_changes()
                payment_win.destroy()
                self.refresh()

            payment_win = tk.Toplevel(self.sales_treeview_frame)
            payment_win.title("Receive Payment")
            payment_win.config(padx=20, pady=20)

            self.center_window(payment_win, 215, 260)

            invoice_id = selected_invoice[0]
            invoice = self.dbmanager.get_invoice(invoice_id)
            # Invoice No
            tk.Label(payment_win, text=f"Invoice No", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.id}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=2, sticky=tk.W)

            # Total Payable
            tk.Label(payment_win, text=f"Total Payable", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.total_payable}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=2, sticky=tk.W)

            # Total Payable
            tk.Label(payment_win, text=f"Paid", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.paid}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=2, sticky=tk.W)

            # Due
            tk.Label(payment_win, text=f"Due", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.due}", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=2, sticky=tk.W)

            tk.Label(payment_win, text="Payment Received", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4,
                                                                                                              column=0,
                                                                                                              sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4, column=1,
                                                                                               sticky=tk.W)
            payment_received_entry = tk.Entry(payment_win, width=6, font=("Segoe UI", 12))
            payment_received_entry.focus_set()
            payment_received_entry.grid(row=4, column=2)
            tk.Button(payment_win, text="Confirm", command=update_invoice_with_new_payment).grid(row=5, column=1,
                                                                                                 columnspan=2, pady=10,
                                                                                                 sticky=tk.NSEW)
            payment_win.transient()
            payment_win.grab_set()  # modal behavior
            payment_win.resizable(False, False)

    def center_window(self, win, custom_height, custom_width):
        win.update_idletasks()
        width = custom_width
        height = custom_height
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def sales_return(self):
        sales_return_window = tk.Toplevel(self.sales_treeview_frame)
        sales_return_window.title("Receive Payment")
        sales_return_window.config(padx=20, pady=20)
        self.center_window(sales_return_window, 550, 1085)
        sales_return_window.transient()
        sales_return_window.grab_set()  # modal behavior
        sales_return_window.resizable(False, False)
        selected_invoice_id = self.sales_treeview.selection()[0]
        invoice_id = self.sales_treeview.item(selected_invoice_id, "values")[0]
        invoice = self.dbmanager.get_invoice(invoice_id)
        RefundFrame(sales_return_window, invoice, self.dbmanager)

    def search_by_invoice(self):
        self.option_label.config(text="Invoice Number:")
        self.show_invoice_or_phone_entry_search()

    def search_by_phone(self):
        self.option_label.config(text="Phone Number:")
        self.show_invoice_or_phone_entry_search()

    def search_by_date_range(self):
        self.option_label.config(text="Date:")
        self.show_custom_date_search()

    def show_invoice_or_phone_entry_search(self):
        self.date_entry.grid_remove()
        self.invoice_or_phone_entry.grid()

    def show_custom_date_search(self):
        self.invoice_or_phone_entry.grid_remove()
        self.date_entry.grid()

    def refresh(self):
        filter_option = self.filter_var.get()
        if filter_option == "all":
            self.all_radio_button.invoke()
        elif filter_option == "today":
            self.today_radio_button.invoke()
        elif filter_option == "due":
            self.due_radio_button.invoke()
        elif filter_option == "custom_search":
            self.search_button.invoke()
