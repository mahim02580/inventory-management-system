import tkinter as tk

CARD_WIDTH = 17


class DashboardFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.configure(padx=20, pady=20)
        self.parent = parent
        self.dbmanager = dbmanager

        # Today Data ---------------------------------------------------------------------------------------------------
        today_data = tk.Frame(self)
        today_data.grid(row=0, column=0)

        # Today Sales
        today_sales = tk.Frame(today_data, bg="#2c3e50")
        today_sales.grid(row=0, column=0, padx=(0, 10))

        self.today_sales_count = tk.IntVar(value=0)
        tk.Label(today_sales, text="Today\nSales", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=0,
                                                    column=0)
        tk.Label(today_sales, textvariable=self.today_sales_count, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Sales Value
        today_sales_value = tk.Frame(today_data, bg="#2c3e50")
        today_sales_value.grid(row=0, column=1, padx=10)
        self.today_sales_value = tk.DoubleVar(value=0)
        tk.Label(today_sales_value, text="Today Sales\nValue", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_sales_value, textvariable=self.today_sales_value, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Due Received
        today_due_received = tk.Frame(today_data, bg="#2c3e50")
        today_due_received.grid(row=0, column=2, padx=10)
        self.today_due_received = tk.DoubleVar(value=0)
        tk.Label(today_due_received, text="Today Due\nReceived", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_due_received, textvariable=self.today_due_received, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Due Sales Value
        today_due_sales_value = tk.Frame(today_data, bg="#2c3e50")
        today_due_sales_value.grid(row=0, column=3, padx=10)
        self.today_due_sales_value = tk.DoubleVar(value=0)
        tk.Label(today_due_sales_value, text="Today Due\nSales Value", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_due_sales_value, textvariable=self.today_due_sales_value, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Sales Return Value
        today_sales_return_value = tk.Frame(today_data, bg="#2c3e50")
        today_sales_return_value.grid(row=1, column=0, padx=(0, 10))
        self.today_sales_return_value = tk.DoubleVar(value=0)
        tk.Label(today_sales_return_value, text="Today Sales\nReturn Value", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_sales_return_value, textvariable=self.today_sales_return_value, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Purchases Value
        today_purchases_value = tk.Frame(today_data, bg="#2c3e50")
        today_purchases_value.grid(row=1, column=1, padx=10)
        self.today_purchases_value = tk.DoubleVar(value=0)
        tk.Label(today_purchases_value, text="Today Purchases\nValue", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_purchases_value, textvariable=self.today_purchases_value, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Supplier Due Payment
        today_supplier_due_payment = tk.Frame(today_data, bg="#2c3e50")
        today_supplier_due_payment.grid(row=1, column=2, padx=10, pady=20)
        self.today_supplier_due_payment = tk.DoubleVar(value=0)
        tk.Label(today_supplier_due_payment, text="Today Supplier\nDue Payment", width=CARD_WIDTH, bg="#2c3e50",
                 fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_supplier_due_payment, textvariable=self.today_supplier_due_payment, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Expenses Value
        today_expenses_value = tk.Frame(today_data, bg="#2c3e50")
        today_expenses_value.grid(row=1, column=3, padx=10, pady=20)
        self.today_expenses_value = tk.DoubleVar(value=0)
        tk.Label(today_expenses_value, text="Today Expenses\nValue", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_expenses_value, textvariable=self.today_expenses_value, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Balance
        today_balance = tk.Frame(today_data, bg="#2c3e50")
        today_balance.grid(row=2, column=0, padx=(0, 10), pady=(0, 20))
        self.today_balance = tk.DoubleVar(value=0)
        tk.Label(today_balance, text="Today\nBalance", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(
            row=0, column=0)
        tk.Label(today_balance, textvariable=self.today_balance, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)

        # Today Data ---------------------------------------------------------------------------------------------------
        business_data = tk.Frame(self)
        business_data.grid(row=1, column=0)

        # Today Sales
        total_product_valuation = tk.Frame(business_data, bg="#2c3e50")
        total_product_valuation.grid(row=0, column=0, pady=10, padx=(0, 10))

        self.total_product_valuation = tk.IntVar(value=0)
        tk.Label(total_product_valuation, text="Total Products\nValuation", width=CARD_WIDTH, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=0,
                                                    column=0)
        tk.Label(total_product_valuation, textvariable=self.total_product_valuation, bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold"), ).grid(row=1, column=0)
        self.refresh()

    def refresh(self):
        self.today_sales_count.set(self.get_today_sale_count())
        self.today_sales_value.set(self.get_today_sales_value())
        self.today_due_received.set(self.get_today_due_received())
        self.today_due_sales_value.set(self.get_today_due_sales_value())
        self.today_sales_return_value.set(self.get_today_sales_return_value())
        self.today_purchases_value.set(self.get_today_purchases_value())
        self.today_supplier_due_payment.set(self.get_today_supplier_due_payment())
        self.today_expenses_value.set(self.get_today_expenses_value())
        self.total_product_valuation.set(self.get_total_products_valuation())

    def get_today_sale_count(self):
        today_sales = self.dbmanager.get_today_sales()
        return len(today_sales)

    def get_today_sales_value(self):
        today_sales_value = 0
        today_sales = self.dbmanager.get_today_sales()
        for today_sale in today_sales:
            today_sales_value += today_sale.total_payable

        return today_sales_value

    def get_today_due_received(self):
        today_due_received_obj = self.dbmanager.today_due_received()
        received_due_payment = 0
        for obj in today_due_received_obj:
            received_due_payment += obj.amount

        return received_due_payment

    def get_today_due_sales_value(self):
        today_due_sales_value = 0
        today_sales = self.dbmanager.get_today_sales()
        for today_sale in today_sales:
            today_due_sales_value += today_sale.due

        return today_due_sales_value

    def get_today_sales_return_value(self):
        refund_amount = 0
        today_sales_returns = self.dbmanager.today_sales_returns()
        for sales_return in today_sales_returns:
            refund_amount += sales_return.refund_amount
        return refund_amount

    def get_today_purchases_value(self):
        purchases_value = 0
        today_purchases = self.dbmanager.today_purchases()
        for today_purchase in today_purchases:
            purchases_value += today_purchase.paid

        return purchases_value

    def get_today_supplier_due_payment(self):
        today_paid = 0
        today_payments = self.dbmanager.today_supplier_payments()
        for today_payment in today_payments:
            today_paid += today_payment.amount

        return today_payments

    def get_today_expenses_value(self):
        today_expenses_amount = 0
        today_expenses_obj = self.dbmanager.today_expenses()
        for today_expense in today_expenses_obj:
            today_expenses_amount += today_expense.amount

        return today_expenses_amount

    def get_total_products_valuation(self):
        products_valuation = 0
        all_products = self.dbmanager.get_all_products()
        for product in all_products:
            product_valuation = product.sell_unit_price * product.current_stock
            products_valuation += product_valuation

        return round(products_valuation, 2)
