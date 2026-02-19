import math
from datetime import date, time, datetime
from sqlalchemy import create_engine, select, ForeignKey, Date, Time
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from utils.dbmodels import *

# ------------------------------------------ Engine + Session ------------------------------------------
engine = create_engine("sqlite:///database/database.db")
Base.metadata.create_all(engine)
session = Session(engine)


# ------------------------------------------Functions------------------------------------------
# Product Management
def get_product_by_name(product_name):
    """Gets a specific product using product_name"""
    product = session.execute(select(Product).where(Product.name == product_name)).scalar()
    return product


def get_product_by_code(code):
    product = session.get(Product, int(code))
    return product


def get_all_products():
    products = session.execute(select(Product)).scalars().all()
    return products


def add_product(product):
    session.add(product)
    session.commit()


def update_product(product_id, changed_column, new_value):
    product_to_update = session.get(Product, product_id)
    product_to_update.__setattr__(changed_column, new_value)
    session.commit()


def delete_product(product_id):
    product_to_delete = session.get(Product, ident=product_id)
    session.delete(product_to_delete)
    session.commit()


def adjust_stock_of_product(product_id, quantity):
    product = session.get(Product, int(product_id))
    product.current_stock -= quantity
    session.commit()


def update_stock_of_product(product_id, new_stock):
    product = session.get(Product, int(product_id))
    product.current_stock += int(new_stock)
    session.commit()


# Customer Management
def get_customer_by_phone(customer_phone):
    customer = session.execute(select(Customer).where(Customer.phone == customer_phone)).scalar()
    return customer


def add_customer(customer):
    session.add(customer)
    session.commit()


def get_all_customers():
    customers = session.execute(select(Customer)).scalars().all()
    return customers


# Sales Management
def add_sale(purchase):
    session.add(purchase)
    session.commit()


def get_today_sales():
    today = datetime.today().date()
    today_sales = session.execute(select(Invoice).where(Invoice.date == today)).scalars().all()
    return today_sales


def get_all_sales():
    all_sales = session.execute(select(Invoice)).scalars().all()
    return all_sales


def get_invoice(invoice_id):
    invoice = session.get(Invoice, invoice_id)
    return invoice


def get_invoices_by_date(date_obj):
    invoices = session.execute(select(Invoice).where(Invoice.date == date_obj)).scalars().all()
    return invoices


def update_changes():
    session.commit()


def get_saleitem(sale_id):
    saleitem = session.get(SaleItem, sale_id)
    return saleitem


# Purchase Management

def add_purchase(purchase):
    session.add(purchase)
    session.commit()


def get_purchase_by_id(id_no):
    purchase = session.get(Purchase, int(id_no))
    return purchase


def get_all_purchases():
    all_purchases = session.execute(select(Purchase)).scalars().all()
    return all_purchases


def get_due_purchases():
    due_purchases = session.execute(select(Purchase).where(Purchase.due > 0)).scalars().all()
    return due_purchases


def get_today_delivery_purchases():
    today = datetime.today().date()
    today_delivery_purchases = session.execute(select(Purchase).where(Purchase.delivery_date == today)).scalars().all()
    return today_delivery_purchases


def get_purchases_by_supplier_name(supplier_name):
    supplier = session.execute(select(Supplier).where(Supplier.name == supplier_name)).scalar()
    purchases_for_the_supplier = supplier.orders
    return purchases_for_the_supplier


def get_purchases_by_purchase_date(purchase_date):
    purchases = session.execute(select(Purchase).where(Purchase.purchase_date == purchase_date)).scalars().all()
    return purchases


def get_purchases_by_delivery_date(delivery_date):
    purchases = session.execute(select(Purchase).where(Purchase.delivery_date == delivery_date)).scalars().all()
    return purchases


# Supplier Management
def get_supplier_by_name(name):
    supplier = session.execute(select(Supplier).where(Supplier.name == name)).scalar()
    return supplier


def add_supplier(supplier):
    session.add(supplier)
    session.commit()


# Expense Management
def get_all_expenses():
    all_expenses = session.execute(select(Expense)).scalars().all()
    return all_expenses


def get_today_expenses():
    today = datetime.today().date()
    today_expenses = session.execute(select(Expense).where(Expense.date == today)).scalars().all()
    return today_expenses


def get_expenses_by_date(date_obj):
    expenses = session.execute(select(Expense).where(Expense.date == date_obj)).scalars().all()
    return expenses


def add_new_expense(new_expense):
    session.add(new_expense)
    session.commit()
