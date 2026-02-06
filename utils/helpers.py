import re
import sqlite3
import tkinter as tk
import win32print
import win32ui

SHOP_NAME = "SHOP_NAME"
SHOP_ADDRESS = "SHOP_ADDRESS"
SHOP_PHONE = "Contact: SHOP_PHONE"


def make_invoice_for_purchase(invoice):
    ready_invoice = "=" * 40 + "\n"
    ready_invoice += f"{SHOP_NAME.center(40)}\n"
    ready_invoice += f"{SHOP_ADDRESS.center(40)}\n"
    ready_invoice += f"{SHOP_PHONE.center(40)}\n"
    ready_invoice += f"{"Sales Invoice".center(40)}\n"
    ready_invoice += "=" * 40 + "\n"
    ready_invoice += f"{"Invoice No".ljust(20)}:" + f"{str(invoice.id).rjust(19)}\n"
    ready_invoice += f"{"Date".ljust(20)}:" + f"{invoice.date.strftime('%d-%m-%Y').rjust(19)}\n"
    ready_invoice += f"{"Time".ljust(20)}:" + f"{invoice.time.strftime('%I:%M %p').rjust(19)}\n"
    ready_invoice += "-" * 40 + "\n"
    ready_invoice += "Item".ljust(15) + "Unit Price".rjust(10) + "Qty".rjust(5) + "Subtotal".rjust(10) + "\n"
    for item in invoice.items:
        ready_invoice += f"{item.product_name}"[:15].ljust(15) + f"{item.unit_price}".rjust(
            10) + f"{item.quantity}".rjust(
            5) + f"{item.subtotal}".rjust(10) + "\n"
    ready_invoice += "-" * 40 + "\n"
    ready_invoice += "MRP Total:".rjust(21) + f"{invoice.mrp_total}".rjust(19) + "\n"
    ready_invoice += "(-) Discount:".rjust(21) + f"{invoice.discount}".rjust(19) + "\n"
    ready_invoice += f"{"-" * 19}".rjust(40) + "\n"
    ready_invoice += "Total Payable:".rjust(21) + f"{invoice.total_payable}".rjust(19) + "\n"
    ready_invoice += "Paid:".rjust(21) + f"{invoice.paid}".rjust(19) + "\n"
    ready_invoice += f"{"-" * 19}".rjust(40) + "\n"
    ready_invoice += "Change:".rjust(21) + f"{invoice.change}".rjust(19) + "\n"
    ready_invoice += "Due:".rjust(21) + f"{invoice.due}".rjust(19) + "\n"
    ready_invoice += "-" * 40 + "\n\n"
    ready_invoice += f"Customer ID: {invoice.customer.phone}\n"
    ready_invoice += f"Name: {invoice.customer.name}\n"
    ready_invoice += f"Address: {invoice.customer.address}\n"
    ready_invoice += "Thank you for your purchase!".center(40) + "\n\n"
    ready_invoice += "     পণ্য ফেরতের জন্য রিসিপ্ট আবশ্যক।".center(40)

    print(ready_invoice)
    return ready_invoice


def print_out_invoice(invoice):
    printer_name = win32print.GetDefaultPrinter()

    hprinter = win32print.OpenPrinter(printer_name)
    printer_info = win32print.GetPrinter(hprinter, 2)

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    # ---- SET FONT ----
    font = win32ui.CreateFont({
        "name": "Courier New",
        "height": 20,
        "weight": 4000
    })
    hdc.SelectObject(font)

    # ---- START PRINT ----
    hdc.StartDoc("Invoice")
    hdc.StartPage()

    x = 10
    y = 10
    line_height = 24

    for line in invoice.split("\n"):
        hdc.TextOut(x, y, line)
        y += line_height

    hdc.EndPage()
    hdc.EndDoc()

    # ---- CLEANUP ----
    hdc.DeleteDC()
    win32print.ClosePrinter(hprinter)


def validate_phonenumber(phone_number):
    if phone_number == "":
        return True
    return phone_number.isdigit() and len(phone_number) <= 11


def is_digit(value):
    if value == "":
        return True
    return value.isdigit()

class AutoCompleteEntry(tk.Entry):
    def __init__(self, master, db_path, **kwargs):
        super().__init__(master, **kwargs)

        self.db_path = db_path
        self.var = tk.StringVar()
        self.config(textvariable=self.var)

        self.dropdown = None
        self.listbox = None
        self.results = []

        self.var.trace_add("write", self._on_type)

        self.bind("<Down>", self._move_down)
        self.bind("<Up>", self._move_up)
        self.bind("<Return>", self._select)
        self.bind("<Button-1>", self._select)
        self.bind("<Escape>", lambda e: self._hide())

    # ---------------- CORE ----------------

    def _on_type(self, *args):
        text = self.var.get().strip()

        # Barcode scanner support
        if len(text) >= 8 and text.isdigit():
            self._auto_pick(text)
            return

        if not text:
            self._hide()
            return

        self.results = self._search_db(text)
        if not self.results:
            self._hide()
            return

        self._show()

    def _search_db(self, keyword):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute("""
            SELECT code, name
            FROM products
            WHERE code LIKE ?
               OR name LIKE ?
            LIMIT 15
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cur.fetchall()
        con.close()

        return [f"{code} - {name}" for code, name in rows]

    # ---------------- DROPDOWN ----------------

    def _show(self):
        self._hide()

        self.dropdown = tk.Toplevel(self)
        self.dropdown.overrideredirect(True)
        self.dropdown.attributes("-topmost", True)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        w = self.winfo_width()
        h = min(200, len(self.results) * 24)

        self.dropdown.geometry(f"{w}x{h}+{x}+{y}")

        self.listbox = tk.Listbox(self.dropdown)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for item in self.results:
            self.listbox.insert(tk.END, item)

        self.listbox.selection_set(0)

        self.listbox.bind("<ButtonRelease-1>", self._select)


    def _hide(self):
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None

    # ---------------- SELECTION ----------------

    def _select(self, event=None):
        if not self.listbox:
            return

        value = self.listbox.get(tk.ACTIVE)
        self.var.set(value)
        self._hide()
        self.icursor(tk.END)

    def _move_down(self, event):
        if self.listbox:
            index = self.listbox.curselection()[0]
            if index < self.listbox.size() - 1:
                self.listbox.selection_clear(index)
                self.listbox.selection_set(index + 1)
                self.listbox.activate(index + 1)

    def _move_up(self, event):
        if self.listbox:
            index = self.listbox.curselection()[0]
            if index > 0:
                self.listbox.selection_clear(index)
                self.listbox.selection_set(index - 1)
                self.listbox.activate(index - 1)

    # ---------------- BARCODE ----------------

    def _auto_pick(self, code):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute("""
            SELECT code, name
            FROM products
            WHERE code = ?
        """, (code,))

        row = cur.fetchone()
        con.close()

        if row:
            self.var.set(f"{row[0]} — {row[1]}")
            self._hide()

class AutoCompleteEntryForSuppliers(AutoCompleteEntry):
    def _search_db(self, keyword):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute(f"""
            SELECT name
            FROM suppliers
            WHERE name LIKE ?
        """, (f"%{keyword}%",))

        rows = cur.fetchall()
        con.close()

        return [name for name in rows]

    def _auto_pick(self, id):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute("""
               SELECT name
               FROM suppliers
               WHERE id = ?
           """, id)

        row = cur.fetchone()
        con.close()

        if row:
            self.var.set(f"{row[0]} — {row[1]}")
            self._hide()
