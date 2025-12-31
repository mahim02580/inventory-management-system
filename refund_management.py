import tkinter as tk
from tkinter import ttk, messagebox


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
        columns = ("PID", "Product Name", "Unit Price", "Sold Qty", "Returned Qty(P)", "Returned Qty(N)", "Refund")
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
        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)
        self.product_entry_treeview.column("PID", width=60, stretch=False, )
        self.product_entry_treeview.column("Product Name", width=424, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=90, stretch=False, )
        self.product_entry_treeview.column("Sold Qty", width=80, stretch=False, )
        self.product_entry_treeview.column("Returned Qty(P)", width=140, stretch=False, )
        self.product_entry_treeview.column("Returned Qty(N)", width=140, stretch=False, )
        self.product_entry_treeview.column("Refund", width=90, stretch=False, )

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
        for item in self.invoice.items:
            previous_returns = sum([refund.refund_quantity for refund in item.refunds])
            self.product_entry_treeview.insert("", tk.END, iid=item.id,
                                               values=(item.product_id, item.product_name, item.unit_price,
                                                       item.quantity, previous_returns, 0, 0), tags="product_entry_row")
            print(item.id)

    def edit_cell(self, event):
        # Detect row and column
        region = self.product_entry_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_entry_treeview.identify_row(event.y)
        column = self.product_entry_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1

        if not col_index == 5:
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

            available_product_to_return = int(values[3]) - int(values[4])
            if int(new_val) > available_product_to_return:
                messagebox.showwarning(title="Return Limit Exceeded",
                                     message="The return quantity cannot exceed the sold quantity.")
                return
            values[col_index] = new_val  # Implements Changes

            # Update return subtotal
            values[-1] = str(int(values[2]) * int(values[col_index]))
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
            product_name, refund_quantity = values[1], values[5]
            self.dbmanager.update_stock_of_product(product_name, refund_quantity)

            # Add refund history to the SaleItem
            saleitem = self.dbmanager.get_saleitem(row_id)
            refund_history = self.dbmanager.Refund(
                refund_quantity=refund_quantity,
                refund_amount=saleitem.unit_price * int(refund_quantity),
            )
            saleitem.refunds.append(refund_history)
            self.dbmanager.update_changes()
        self.parent.destroy()
