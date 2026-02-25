from datetime import date, time, datetime
from sqlalchemy import ForeignKey, Date, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ------------------------------------------Table Models------------------------------------------
class Product(Base):
    __tablename__ = "products"
    code: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    base_unit_type: Mapped[str] = mapped_column()
    sell_unit_type: Mapped[str] = mapped_column()
    sell_unit_price: Mapped[float] = mapped_column()
    conversion_factor: Mapped[float] = mapped_column()
    pcs_per_box: Mapped[int] = mapped_column()
    current_stock: Mapped[float] = mapped_column()
    low_stock_alert: Mapped[float] = mapped_column()




class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column()
    purchases = relationship("Invoice", back_populates="customer")

class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    orders = relationship("Purchase", back_populates="supplier")


class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="orders")
    purchase_date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_payable: Mapped[float] = mapped_column(nullable=False)
    paid: Mapped[float] = mapped_column(nullable=False)
    due: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    items = relationship("PurchaseItem", back_populates="purchase")
    payment_history = relationship("SupplierDuePayment", back_populates="purchase")

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"))
    product_code: Mapped[int] = mapped_column(ForeignKey("products.code"))
    product_category: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_type: Mapped[str] = mapped_column(nullable=False)
    base_qty: Mapped[str] = mapped_column()
    unit_price: Mapped[float] = mapped_column(nullable=False)
    subtotal: Mapped[float] = mapped_column(nullable=False)

    purchase = relationship("Purchase", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(),
                                       nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time(),
                                       nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.id))
    customer = relationship("Customer", back_populates="purchases")
    mrp_total: Mapped[float] = mapped_column(nullable=False)
    discount: Mapped[float] = mapped_column(nullable=False)
    total_payable: Mapped[float] = mapped_column(nullable=False)
    paid: Mapped[float] = mapped_column(nullable=False)
    change: Mapped[float] = mapped_column("Change", nullable=False)
    due: Mapped[float] = mapped_column("Due", nullable=False)

    items = relationship("SaleItem", back_populates="invoice")
    payment_history = relationship("CustomerDuePayment", back_populates="invoice")

class SaleItem(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    product_code: Mapped[int] = mapped_column(ForeignKey("products.code"))
    product_category: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_type: Mapped[str] = mapped_column(nullable=False)
    base_qty: Mapped[str] = mapped_column()
    unit_price: Mapped[float] = mapped_column(nullable=False)
    subtotal: Mapped[float] = mapped_column(nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    refunds = relationship("Refund", back_populates="sale_item")


class Refund(Base):
    __tablename__ = "refunds"
    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time())
    refund_quantity: Mapped[int] = mapped_column(nullable=False)
    refund_amount: Mapped[float] = mapped_column(nullable=False)
    # RELATION
    sale_item = relationship("SaleItem", back_populates="refunds")

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date())
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time())
    purpose: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column()

class CustomerDuePayment(Base):
    __tablename__ = "customerduepayments"
    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time())
    amount: Mapped[float] = mapped_column()

    invoice = relationship("Invoice", back_populates="payment_history")

class SupplierDuePayment(Base):
    __tablename__ = "supplierduepayments"
    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.today().date(), nullable=False)
    time: Mapped[time] = mapped_column(Time, default=lambda: datetime.today().time())
    amount: Mapped[float] = mapped_column()

    purchase = relationship("Purchase", back_populates="payment_history")
