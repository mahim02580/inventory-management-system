from datetime import date, time, datetime
from sqlalchemy import create_engine, select, ForeignKey, Date, Time
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ------------------------------------------Table Models------------------------------------------
class Product(Base):
    __tablename__ = "products"
    code: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    unit_type: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[int] = mapped_column(nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    phone: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column()
    purchases = relationship("Invoice", back_populates="customer")


class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="orders")
    items = relationship("PurchaseItem", back_populates="purchase")
    purchase_date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_payable: Mapped[int] = mapped_column(nullable=False)
    paid: Mapped[int] = mapped_column(nullable=False)
    due: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    orders = relationship(Purchase, back_populates="supplier")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"), nullable=False)
    product_code: Mapped[int] = mapped_column(ForeignKey("products.code"))
    product_name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_type: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[int] = mapped_column(nullable=False)
    subtotal: Mapped[int] = mapped_column(nullable=False)

    purchase = relationship("Purchase", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(),
                                       nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time(),
                                       nullable=False)
    items = relationship("SaleItem", back_populates="invoice")
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.phone))
    customer = relationship("Customer", back_populates="purchases")
    mrp_total: Mapped[int] = mapped_column(nullable=False)
    discount: Mapped[int] = mapped_column(nullable=False)
    total_payable: Mapped[int] = mapped_column(nullable=False)
    paid: Mapped[int] = mapped_column(nullable=False)
    change: Mapped[int] = mapped_column("Change", nullable=False)
    due: Mapped[int] = mapped_column("Due", nullable=False)


class SaleItem(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.code"))
    product_name: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    subtotal: Mapped[int] = mapped_column(nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    refunds = relationship("Refund", back_populates="sale_item")


class Refund(Base):
    __tablename__ = "refunds"
    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), nullable=False)
    refund_quantity: Mapped[int] = mapped_column(nullable=False)
    refund_amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time())
    # RELATION
    sale_item = relationship("SaleItem", back_populates="refunds")


# ------------------------------------------ Engine + Session ------------------------------------------
engine = create_engine("sqlite:///database.db")
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


def get_all_products_name():
    """Gets all products name available in the products table"""
    return session.execute(select(Product.name)).scalars().all()


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
    product.stock -= quantity
    session.commit()


def update_stock_of_product(product_id, new_stock):
    product = session.get(Product, int(product_id))
    product.stock += int(new_stock)
    session.commit()


# Customer Management
def get_customer_by_phone(customer_phone):
    customer = session.get(Customer, customer_phone)
    return customer


def add_customer(customer):
    session.add(customer)
    session.commit()


def get_all_customers():
    customers = session.execute(select(Customer)).scalars().all()
    return customers


# Sales Management
def add_purchase(purchase):
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
