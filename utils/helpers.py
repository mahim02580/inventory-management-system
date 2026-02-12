import math
import re
import sqlite3
import tkinter as tk
import win32print
import win32ui
from escpos.printer import Usb
import textwrap

SHOP_NAME = "SHOP_NAME"
SHOP_ADDRESS = "SHOP_ADDRESS"
SHOP_PHONE = "Contact: SHOP_PHONE"
INVOICE_WIDTH = 60

def make_invoice_for_purchase(invoice):
    # ready_invoice = "=" * INVOICE_WIDTH + "\n"
    # ready_invoice += f"{SHOP_NAME.center(INVOICE_WIDTH)}\n"
    # ready_invoice += f"{SHOP_ADDRESS.center(INVOICE_WIDTH)}\n"
    # ready_invoice += f"{SHOP_PHONE.center(INVOICE_WIDTH)}\n"
    # ready_invoice += f"{"Sales Invoice".center(INVOICE_WIDTH)}\n"
    # ready_invoice += "=" * INVOICE_WIDTH + "\n"
    # ready_invoice += f"{"Invoice No".ljust(INVOICE_WIDTH // 2)}:" + f"{str(invoice.id).rjust((INVOICE_WIDTH // 2) -1)}\n"
    # ready_invoice += f"{"Date".ljust(INVOICE_WIDTH // 2)}:" + f"{invoice.date.strftime('%d-%m-%Y').rjust((INVOICE_WIDTH // 2) - 1)}\n"
    # ready_invoice += f"{"Time".ljust(INVOICE_WIDTH // 2)}:" + f"{invoice.time.strftime('%I:%M %p').rjust((INVOICE_WIDTH // 2) - 1)}\n"
    # ready_invoice += "-" * INVOICE_WIDTH + "\n"
    # ready_invoice += "Code".ljust(5) + "Item".ljust(15) + "Qty".ljust(6) + "Unit".ljust(6) + "Rate".ljust(5) + "Base Qty".ljust(15) + "Subtotal".rjust(12) + "\n"
    # for item in invoice.items:
    #     ready_invoice += f"{item.product_code}".ljust(5) + f"{item.product_name}"[:15].ljust(15) + f"{item.quantity}".rjust(
    #         5) + f"{item.unit_price}".rjust(
    #         5) + f"{item.base_qty}".ljust(15) + f"{item.subtotal}".rjust(10)+ "\n"
    # ready_invoice += "-" * INVOICE_WIDTH + "\n"
    # ready_invoice += "MRP Total:".rjust(INVOICE_WIDTH + 1) + f"{invoice.mrp_total}".rjust(INVOICE_WIDTH - 1) + "\n"
    # ready_invoice += "(-) Discount:".rjust(INVOICE_WIDTH + 1) + f"{invoice.discount}".rjust(INVOICE_WIDTH - 1) + "\n"
    # ready_invoice += f"{"-" * int(INVOICE_WIDTH - 1)}".rjust(INVOICE_WIDTH) + "\n"
    # ready_invoice += "Total Payable:".rjust(INVOICE_WIDTH + 1) + f"{invoice.total_payable}".rjust(INVOICE_WIDTH -1) + "\n"
    # ready_invoice += "Paid:".rjust(INVOICE_WIDTH + 1) + f"{invoice.paid}".rjust(INVOICE_WIDTH - 1) + "\n"
    # ready_invoice += f"{"-" * int(INVOICE_WIDTH - 1)}".rjust(INVOICE_WIDTH) + "\n"
    # ready_invoice += "Change:".rjust(INVOICE_WIDTH + 1) + f"{invoice.change}".rjust(INVOICE_WIDTH - 1) + "\n"
    # ready_invoice += "Due:".rjust(INVOICE_WIDTH + 1) + f"{invoice.due}".rjust(INVOICE_WIDTH - 1) + "\n"
    # ready_invoice += "-" * INVOICE_WIDTH + "\n\n"
    # ready_invoice += f"Customer ID: {invoice.customer.phone}\n"
    # ready_invoice += f"Name: {invoice.customer.name}\n"
    # ready_invoice += f"Address: {invoice.customer.address}\n"
    # ready_invoice += "Thank you for your purchase!".center(INVOICE_WIDTH) + "\n\n"
    # ready_invoice += "     পণ্য ফেরতের জন্য রিসিপ্ট আবশ্যক।".center(INVOICE_WIDTH)




    WIDTH = 60  # change if needed

    def hr():
        return "-" * WIDTH

    def eq():
        return "=" * WIDTH

    def format_money(x):
        return f"{x:.0f}"

    def print_invoice(invoice):
        p = Usb(0x04b8, 0x0e15)  # change to your printer

        def line(txt=""):
            p.text(txt + "\n")

        # ================= HEADER =================
        p.set(align="center", bold=True)
        line(eq())
        line(SHOP_NAME)
        line(SHOP_ADDRESS)
        line(SHOP_PHONE)
        line("Sales Invoice")
        line(eq())
        p.set(bold=False)
        p.set(align="left")

        line(f"{'Invoice No'.ljust(30)}: {str(invoice.id).rjust(25)}")
        line(f"{'Date'.ljust(30)}: {invoice.date.strftime('%d-%m-%Y').rjust(25)}")
        line(f"{'Time'.ljust(30)}: {invoice.time.strftime('%I:%M %p').rjust(25)}")

        line(hr())
        line("Code Item              Qty  Rate    Base            Subtotal")
        line("                     Qty")
        line(hr())

        # ================= ITEMS =================
        for item in invoice.items:

            name_lines = textwrap.wrap(item.product_name, 20)

            qty_lines = [
                str(item.quantity),
                item.unit_type
            ]

            base_lines = []
            if item.base_qty:
                base_lines = textwrap.wrap(str(item.base_qty), 12)

            max_lines = max(len(name_lines), len(qty_lines), len(base_lines), 1)

            for i in range(max_lines):
                code = str(item.product_code) if i == 0 else ""
                name = name_lines[i] if i < len(name_lines) else ""
                qty = qty_lines[i] if i < len(qty_lines) else ""
                rate = format_money(item.unit_price) if i == 0 else ""
                base = base_lines[i] if i < len(base_lines) else ""
                sub = format_money(item.subtotal) if i == 0 else ""

                row = (
                        code.ljust(5) +
                        name.ljust(20) +
                        qty.rjust(6) +
                        rate.rjust(7) +
                        base.center(12) +
                        sub.rjust(10)
                )

                line(row)

            line("")

        # ================= TOTALS =================
        line(hr())
        line(f"{'MRP Total:'.rjust(45)}{format_money(invoice.mrp_total).rjust(15)}")
        line(f"{'(-) Discount:'.rjust(45)}{format_money(invoice.discount).rjust(15)}")
        line("-" * (WIDTH - 1))
        line(f"{'Total Payable:'.rjust(45)}{format_money(invoice.total_payable).rjust(15)}")
        line(f"{'Paid:'.rjust(45)}{format_money(invoice.paid).rjust(15)}")
        line("-" * (WIDTH - 1))
        line(f"{'Change:'.rjust(45)}{format_money(invoice.change).rjust(15)}")
        line(f"{'Due:'.rjust(45)}{format_money(invoice.due).rjust(15)}")

        line(hr())

        # ================= CUSTOMER =================
        line(f"Customer ID: {invoice.customer.phone}")
        line(f"Name: {invoice.customer.name}")
        line(f"Address: {invoice.customer.address}")

        p.set(align="center")
        line("")
        line("Thank you for your purchase!")
        line("")
        line("পণ্য ফেরতের জন্য রিসিপ্ট আবশ্যক।")

        p.cut()

    print_invoice(invoice)
    return "something"


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

def calculate_base_stock_for_tiles(tiles, sft_quantity):
    size = tiles.name.split(",")[0] # Taking Tiles size from product's name
    height, width = size.split("x") # Taking height and width from tiles
    sft_per_tiles = round(int(height) * int(width) / 144, 3) # Taking sft (Using round() for decimal rounding)
    final_quantity = round(math.ceil(int(sft_quantity) / sft_per_tiles) * sft_per_tiles)
    pcs_needed = final_quantity // sft_per_tiles
    box, pcs = divmod(pcs_needed, tiles.pcs_per_box)
    base_qty = f"{int(box)}B {int(pcs)}P"
    return final_quantity, base_qty

def calculate_base_stock_for_pipe(pipe, ft_quantity):
    final_quantity = round(int(ft_quantity) / int(pipe.conversion_factor)) * int(pipe.conversion_factor)
    base_qty = f"{final_quantity // int(pipe.conversion_factor)} {pipe.base_unit_type}"
    return final_quantity, base_qty
