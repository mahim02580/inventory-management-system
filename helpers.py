import re

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


def print_out_invoice(invoice: str):
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

