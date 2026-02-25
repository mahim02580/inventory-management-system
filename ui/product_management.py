import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import helpers

CODE_COL_INDEX = 0
CATEGORY_COL_INDEX = 1
PRODUCT_NAME_COL_INDEX = 2
STOCK_COL_INDEX = 3
UNIT_COL_INDEX = 4
BASE_QTY_COL_INDEX = 5
RATE_COL_INDEX = 6


class ProductsFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent, bg="white")
        self.configure(padx=20, pady=20)
        self.dbmanager = dbmanager

        # Products Treeview Frame---------------------------------------------------------------------------------------------
        products_treeview_frame = tk.Frame(self)
        products_treeview_frame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)

        columns = ("Code", "Category", "Product Name", "Stock", "Unit", "Base Qty", "Rate")
        self.product_list_treeview = ttk.Treeview(products_treeview_frame, columns=columns, show="headings", height=21)
        for col in columns:
            self.product_list_treeview.heading(col, text=col)

        self.product_list_treeview.column("Code", width=90, stretch=False, anchor=tk.CENTER)
        self.product_list_treeview.column("Category", width=100, stretch=False)
        self.product_list_treeview.column("Product Name", width=320, stretch=False)
        self.product_list_treeview.column("Stock", width=90, stretch=False, anchor=tk.E)
        self.product_list_treeview.column("Unit", width=50, stretch=False)
        self.product_list_treeview.column("Base Qty", width=90, stretch=False)
        self.product_list_treeview.column("Rate", width=90, stretch=False)

        self.product_list_treeview.grid(row=0, column=0)

        # Menu Options for Treeview
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)
        self.product_list_treeview.bind("<Button-3>", self.show_menu)

        scrollbar = ttk.Scrollbar(products_treeview_frame, orient=tk.VERTICAL, command=self.product_list_treeview.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.product_list_treeview.configure(yscrollcommand=scrollbar.set)
        self.product_list_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.product_list_treeview.tag_configure("oddrow", background="#FFFFFF")
        self.product_list_treeview.tag_configure("low_stock", background="#F9BFBF")

        self.product_list_treeview.bind("<Double-1>", self.edit_product)

        # Right Side Frame----------------------------------------------------------------------------------------------
        product_entry_frame = tk.Frame(self, highlightbackground="#2c3e50", highlightthickness=2)
        product_entry_frame.grid(row=0, column=1, padx=20, sticky=tk.N)

        tk.Label(product_entry_frame,
                 text="Add New Product",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18)).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(product_entry_frame,
                 text="Product Code",
                 fg="white",
                 bg="#2c3e50",
                 width=5,
                 font=("Segoe UI", 12)).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.product_code_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12), validate="key", validatecommand=(
                                                 product_entry_frame.register(helpers.is_float),
                                                 "%P",) )
        self.product_code_entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Category",
                 bg="#2c3e50",
                 width=5,
                 fg="white", font=("Segoe UI", 12), ).grid(row=1, column=1, columnspan=2, padx=5, sticky=tk.NSEW)
        self.product_category_combobox = ttk.Combobox(product_entry_frame, width=5, font=("Segoe UI", 11),
                                                      values=("Tiles", "Sanitary", "Pipe", "Fittings", "Door", "Bathware", "Water Tank", "Accessories"))
        self.product_category_combobox.current(0)
        self.product_category_combobox.grid(row=2, column=1, columnspan=2, pady=(0, 10), padx=5, sticky=tk.EW)
        self.product_category_combobox.bind("<<ComboboxSelected>>", self.check_category)

        tk.Label(product_entry_frame,
                 text="Product Name",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=3, column=0, columnspan=2, padx=5, sticky=tk.NSEW)
        self.product_name_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12))
        self.product_name_entry.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Base Unit Type",
                 bg="#2c3e50",
                 width=5,
                 fg="white", font=("Segoe UI", 12), ).grid(row=5, column=0, padx=5, sticky=tk.NSEW)
        product_units = ("PCS", "BOX", "SFT", "FT", "MTR", "LTR", "KG")
        self.product_base_unit_combobox = ttk.Combobox(product_entry_frame, width=5, font=("Segoe UI", 11),
                                                       values=product_units)
        self.product_base_unit_combobox.current(0)
        self.product_base_unit_combobox.grid(row=6, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        self.pcs_per_box_label = tk.Label(product_entry_frame,
                                          text="PCS Per Box",
                                          fg="white",
                                          bg="#2c3e50",
                                          width=5,
                                          font=("Segoe UI", 12))
        self.pcs_per_box_label.grid(row=5, column=1, padx=5, sticky=tk.NSEW)
        self.pcs_per_box_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12), validate="key",
                                          validatecommand=(self.register(helpers.is_digit), "%P"), )
        self.pcs_per_box_entry.grid(row=6, column=1, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Sell Unit Type",
                 bg="#2c3e50",
                 width=5,
                 fg="white", font=("Segoe UI", 12), ).grid(row=7, column=0, padx=5, sticky=tk.NSEW)

        self.product_sell_unit_combobox = ttk.Combobox(product_entry_frame, width=5, font=("Segoe UI", 11),
                                                       values=product_units)
        self.product_sell_unit_combobox.current(0)
        self.product_sell_unit_combobox.grid(row=8, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Unit Price",
                 fg="white",
                 bg="#2c3e50",
                 width=5,
                 font=("Segoe UI", 12)).grid(row=7, column=1, padx=5, sticky=tk.NSEW)
        self.product_sell_unit_price_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12),
                                                      validate="key", validatecommand=(
                product_entry_frame.register(helpers.is_float),
                "%P",) )
        self.product_sell_unit_price_entry.grid(row=8, column=1, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Unit Conversion Factor",
                 fg="white",
                 bg="#2c3e50",
                 width=5,
                 font=("Segoe UI", 12)).grid(row=9, column=0, columnspan=2, padx=5, sticky=tk.NSEW)
        self.unit_conversion_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12), validate="key", validatecommand=(
                                                 product_entry_frame.register(helpers.is_float),
                                                 "%P",))
        self.unit_conversion_entry.grid(row=10, column=0, columnspan=2, padx=5, pady=(0, 10), sticky=tk.EW)

        self.unit_conversion_entry.insert("end", "1")
        tk.Label(product_entry_frame,
                 text="Stock (Sell Unit)",
                 fg="white",
                 bg="#2c3e50",
                 width=5,
                 font=("Segoe UI", 12)).grid(row=11, column=0, padx=5, sticky=tk.NSEW)
        self.product_current_stock_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12), validate="key", validatecommand=(
                                                 product_entry_frame.register(helpers.is_float),
                                                 "%P",))
        self.product_current_stock_entry.grid(row=12, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Low Stock Alert",
                 fg="white",
                 bg="#2c3e50",
                 width=5,
                 font=("Segoe UI", 12)).grid(row=11, column=1, padx=5, sticky=tk.NSEW)
        self.product_low_stock_alert_entry = tk.Entry(product_entry_frame, width=5, font=("Segoe UI", 12),
                                                      validate="key", validatecommand=(
                product_entry_frame.register(helpers.is_float),
                "%P",))
        self.product_low_stock_alert_entry.grid(row=12, column=1, padx=5, pady=(0, 10), sticky=tk.EW)

        ttk.Button(product_entry_frame,
                   text="Add",
                   command=self.add_product).grid(row=13, column=0, columnspan=2, padx=5, pady=(0, 10), sticky=tk.NSEW)
        self.refresh()
    # Main Methods ----------------------------------------------------------------------------------------------------
    def add_product(self):

        # Get all values from all Entries
        product_code = int(self.product_code_entry.get())
        product_category = self.product_category_combobox.get()
        product_name = self.product_name_entry.get()
        product_base_unit = self.product_base_unit_combobox.get()
        pcs_per_box = self.pcs_per_box_entry.get()  # only for tiles
        product_sell_unit = self.product_sell_unit_combobox.get()
        product_sell_unit_price = float(self.product_sell_unit_price_entry.get())
        unit_conversion = float(self.unit_conversion_entry.get())
        product_current_stock = float(self.product_current_stock_entry.get())
        product_low_stock_alert = float(self.product_low_stock_alert_entry.get())

        if product_category == "Sanitary" and not all([product_code, product_category, product_name, product_base_unit, product_sell_unit,
                    product_sell_unit_price, unit_conversion, product_current_stock, product_low_stock_alert]):
            messagebox.showerror(
                title="Missing Information",
                message="All fields must be filled in."
            )
            return

        product_to_add = self.dbmanager.Product(
            code=product_code,
            category=product_category,
            name=product_name,
            base_unit_type=product_base_unit,
            pcs_per_box=pcs_per_box,  # only for tiles
            sell_unit_type=product_sell_unit,
            sell_unit_price=product_sell_unit_price,
            conversion_factor=unit_conversion,
            current_stock=product_current_stock,
            low_stock_alert=product_low_stock_alert

        )
        self.dbmanager.add_product(product_to_add)
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

        # Prevents column E
        if col_index != PRODUCT_NAME_COL_INDEX:
            if col_index != STOCK_COL_INDEX:
                if col_index != RATE_COL_INDEX:
                    return

        x, y, width, height = self.product_list_treeview.bbox(row_id, column)

        # Current value
        value = self.product_list_treeview.item(row_id)["values"][col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.product_list_treeview, font=("Segoe UI", 12))

        if col_index == STOCK_COL_INDEX:
            entry.config(justify=tk.RIGHT)  # Stock is aligned to right side

        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit():
            # Editable columns only
            column_map = {
                2: "name",
                3: "current_stock",
                6: "sell_unit_price",
            }

            new_val = entry.get()
            values = list(self.product_list_treeview.item(row_id, "values"))

            if values[CATEGORY_COL_INDEX] == "Tiles" and col_index == STOCK_COL_INDEX:
                product = self.dbmanager.get_product_by_code(values[CODE_COL_INDEX])
                final_quantity, base_qty = helpers.calculate_base_stock_for_tiles(product,
                                                                                  new_val)  # Prevents Wrong SFTs
                values[col_index], values[BASE_QTY_COL_INDEX] = final_quantity, base_qty

            elif values[CATEGORY_COL_INDEX] == "Pipe" and col_index == STOCK_COL_INDEX:
                product = self.dbmanager.get_product_by_code(values[CODE_COL_INDEX])
                final_quantity, base_qty = helpers.calculate_base_stock_for_pipe(product,
                                                                                 new_val)  # Prevents Wrong PCS
                values[col_index], values[BASE_QTY_COL_INDEX] = final_quantity, base_qty

            else:
                values[col_index] = new_val  # Implements Changes for other products
            entry.destroy()
            # Update product in the database
            self.dbmanager.update_product(product_id=values[CODE_COL_INDEX], changed_column=column_map[col_index],
                                          new_value=values[col_index])

            # Update Product in the TreeView
            self.product_list_treeview.item(row_id, values=values)

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def refresh(self):
        # Clears Products Treeview
        self.product_list_treeview.delete(*self.product_list_treeview.get_children())

        # Gets all products(updated)
        for i, product in enumerate(self.dbmanager.get_all_products()):
            tag = "low_stock" if product.current_stock <= product.low_stock_alert else "evenrow" if i % 2 == 0 else "oddrow"

            if product.category == "Tiles":
                final_quantity, base_qty = helpers.calculate_base_stock_for_tiles(product, product.current_stock)

                self.product_list_treeview.insert("", tk.END,
                                                  values=(product.code, product.category, product.name,
                                                          final_quantity,
                                                          product.sell_unit_type, base_qty, product.sell_unit_price),
                                                  tags=tag)
            elif product.category == "Pipe":
                final_quantity, base_qty = helpers.calculate_base_stock_for_pipe(product, product.current_stock)
                self.product_list_treeview.insert("", tk.END,
                                                  values=(product.code, product.category, product.name, final_quantity,
                                                          product.sell_unit_type, base_qty, product.sell_unit_price),
                                                  tags=tag)

            else:
                self.product_list_treeview.insert("", tk.END,
                                                  values=(product.code, product.category, product.name,
                                                          product.current_stock,
                                                          product.sell_unit_type, "N/A", product.sell_unit_price),
                                                  tags=tag)

        # Clears all entries
        self.product_code_entry.delete(0, tk.END)
        self.product_category_combobox.current(0)
        self.product_name_entry.delete(0, tk.END)
        self.product_base_unit_combobox.current(0)
        self.product_sell_unit_combobox.current(0)
        self.product_sell_unit_price_entry.delete(0, tk.END)
        self.unit_conversion_entry.delete(0, tk.END)
        self.pcs_per_box_entry.delete(0, tk.END)
        self.product_current_stock_entry.delete(0, tk.END)
        self.product_low_stock_alert_entry.delete(0, tk.END)


    # Helper Methods-----------------------------------------------------------------------------------------------------
    def show_menu(self, event):
        iid = self.product_list_treeview.identify_row(event.y)
        if iid:
            self.product_list_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)
    def check_category(self, event):
        category = self.product_category_combobox.get()
        if category == "Tiles":
            self.pcs_per_box_label.config(fg="white")
            self.pcs_per_box_entry.config(state=tk.NORMAL)
        else:
            self.pcs_per_box_label.config(fg="gray")
            self.pcs_per_box_entry.config(state=tk.DISABLED)


