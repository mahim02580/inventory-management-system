import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import helpers
from utils.helpers import AutoCompleteEntry


class ProductsFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent, bg="white")
        self.configure(padx=20, pady=20)
        self.dbmanager = dbmanager

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_item)
        # Products Treeview Frame---------------------------------------------------------------------------------------------
        products_treeview_frame = tk.Frame(self)
        products_treeview_frame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
        columns = ("Code", "Product Name", "Stock", "Unit Type", "Unit Price")
        self.product_list_treeview = ttk.Treeview(products_treeview_frame, columns=columns, show="headings", height=21)
        for col in columns:
            self.product_list_treeview.heading(col, text=col)

        self.product_list_treeview.column("Code", width=115, stretch=False, anchor=tk.CENTER)
        self.product_list_treeview.column("Product Name", width=419, stretch=False)
        self.product_list_treeview.column("Stock", width=95, stretch=False)
        self.product_list_treeview.column("Unit Type", width=95, stretch=False)
        self.product_list_treeview.column("Unit Price", width=95, stretch=False)

        self.product_list_treeview.grid(row=0, column=0)
        self.product_list_treeview.bind("<Button-3>", self.show_menu)

        scrollbar = ttk.Scrollbar(products_treeview_frame, orient=tk.VERTICAL, command=self.product_list_treeview.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.product_list_treeview.configure(yscrollcommand=scrollbar.set)
        self.product_list_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.product_list_treeview.tag_configure("oddrow", background="#FFFFFF")

        self.product_list_treeview.bind("<Double-1>", self.edit_product)
        # Right Side Frame----------------------------------------------------------------------------------------------
        right_side_frame = tk.Frame(self)
        right_side_frame.grid(row=0, column=2, sticky=tk.NSEW)

        ## Stock Entry
        stock_entry_frame = tk.Frame(right_side_frame, highlightbackground="#2c3e50", highlightthickness=2)
        stock_entry_frame.grid(row=0, column=0, padx=20, sticky=tk.N)

        tk.Label(stock_entry_frame,
                 text="Update New Stock",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18), ).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(stock_entry_frame,
                 text="Select Product",
                 fg="white",
                 bg="#2c3e50",
                 width=25,
                 font=("Segoe UI", 12)).grid(row=1, column=0, padx=5, sticky=tk.NSEW)

        self.product_to_update_stock_entry = AutoCompleteEntry(stock_entry_frame, db_path="../database/database.db", font=("Arial", 12))
        self.product_to_update_stock_entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        tk.Label(stock_entry_frame,
                 text="New Stock",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.product_new_stock_entry = tk.Entry(stock_entry_frame, validate="key",
                                                validatecommand=(self.register(helpers.is_digit), "%P"),
                                                font=("Segoe UI", 12), )
        self.product_new_stock_entry.grid(row=4, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        ttk.Button(stock_entry_frame,
                   text="Update",
                   command=self.update_stock).grid(row=5, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        ## New Product Entry
        product_entry_frame = tk.Frame(right_side_frame, highlightbackground="#2c3e50", highlightthickness=2)
        product_entry_frame.grid(row=1, column=0, padx=20, pady=20, sticky=tk.N)

        tk.Label(product_entry_frame,
                 text="Add New Product",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18)).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(product_entry_frame,
                 text="Product Code",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.product_code_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12))
        self.product_code_entry.grid(row=2, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Product Name",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.product_name_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12))
        self.product_name_entry.grid(row=4, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Product Stock",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=5, column=0, padx=5, sticky=tk.NSEW)
        self.product_stock_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12), validate="key",
                                            validatecommand=(self.register(helpers.is_digit), "%P"), )
        self.product_stock_entry.grid(row=6, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Unit Type",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=7, column=0, padx=5, sticky=tk.NSEW)
        self.product_unit_type_combobox = ttk.Combobox(product_entry_frame, values=("PCS", "SFT", "KG", "LTR"),
                                                       font=("Segoe UI", 12))
        self.product_unit_type_combobox.current(0)
        self.product_unit_type_combobox.grid(row=8, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Unit Price",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12)).grid(row=9, column=0, padx=5, sticky=tk.NSEW)
        self.product_unit_price_entry = tk.Entry(product_entry_frame, validate="key",
                                                 validatecommand=(self.register(helpers.is_digit), "%P"),
                                                 font=("Segoe UI", 12), )
        self.product_unit_price_entry.grid(row=10, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        ttk.Button(product_entry_frame,
                   text="Add",
                   command=self.add_product).grid(row=11, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)
        self.refresh()

    def edit_product(self, event):
        # Detect row and column
        region = self.product_list_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_list_treeview.identify_row(event.y)
        column = self.product_list_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1

        if col_index == 0:
            return

        x, y, width, height = self.product_list_treeview.bbox(row_id, column)

        # Current value
        value = self.product_list_treeview.item(row_id)["values"][col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.product_list_treeview, font=("Segoe UI", 12))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit():
            column_map = {
                0: "id",
                1: "name",
                2: "unit_price",
                3: "stock",
            }

            new_val = entry.get()
            values = list(self.product_list_treeview.item(row_id, "values"))

            values[col_index] = new_val  # Implements Changes
            entry.destroy()
            # Update product in the database
            self.dbmanager.update_product(product_id=values[0], changed_column=column_map[col_index], new_value=new_val)

            # Update Product in the TreeView

            self.product_list_treeview.item(row_id, values=values)

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def delete_item(self):
        selected = self.product_list_treeview.selection()
        if not selected:
            return
        for item in selected:
            product_id_to_delete = self.product_list_treeview.item(item, "values")[0]
            self.dbmanager.delete_product(product_id_to_delete)  # Deletes in database
            self.product_list_treeview.delete(item)  # Deletes in Treeview

    def show_menu(self, event):
        iid = self.product_list_treeview.identify_row(event.y)
        if iid:
            self.product_list_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def add_product(self):
        product_code = int(self.product_code_entry.get())
        product_name = self.product_name_entry.get()
        product_stock = self.product_stock_entry.get()
        product_unit_type = self.product_unit_type_combobox.get()
        product_unit_price = self.product_unit_price_entry.get()

        if not all([product_code, product_name, product_stock, product_unit_type, product_unit_price]):
            messagebox.showerror(
                title="Missing Information",
                message="Product Name, Unit Price, and Stock must all be filled in."
            )
            return

        product_to_add = self.dbmanager.Product(
            code=product_code,
            name=product_name,
            stock=product_stock,
            unit_type=product_unit_type,
            unit_price=product_unit_price,
        )
        self.dbmanager.add_product(product_to_add)
        self.refresh()

    def update_stock(self):
        product_id_to_update_stock = self.product_to_update_stock_entry.get().split("-")[0]
        new_stock = self.product_new_stock_entry.get()
        if not new_stock:
            messagebox.showerror(
                title="Missing Information",
                message="New Stock must be filled in."
            )
            return

        self.dbmanager.update_stock_of_product(product_id_to_update_stock, new_stock)
        self.refresh()

    def refresh(self):
        # Clears Products Treeview
        self.product_list_treeview.delete(*self.product_list_treeview.get_children())

        # Gets all products(updated)
        for i, product in enumerate(self.dbmanager.get_all_products()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.product_list_treeview.insert("", tk.END,
                                              values=(product.code, product.name, product.stock, product.unit_type,
                                                      product.unit_price), tags=tag)


        # Clears all entries
        self.product_to_update_stock_entry.delete(0, tk.END)
        self.product_new_stock_entry.delete(0, tk.END)  # from Update New Stock
        self.product_code_entry.delete(0, tk.END)
        self.product_name_entry.delete(0, tk.END)
        self.product_unit_price_entry.delete(0, tk.END)
        self.product_stock_entry.delete(0, tk.END)
