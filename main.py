import tkinter as tk
from tkinter import ttk
from ui.dashboard import DashboardFrame
from ui.sales_management import NewSaleFrame, SalesFrame
from ui.purchases_management import NewPurchase, PurchasesFrame
from ui.expenses_management import ExpensesFrame
from ui.product_management import ProductsFrame
from ui.customer_management import CustomersFrame
from utils import database_management as db

TITLE = "Sanitary & Tiles Shop Digital Hisab Khata and Stock Manager"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.state('zoomed')
        # Allows custom styles
        style = ttk.Style(self)
        style.theme_use("clam")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = tk.Frame(self, bg="#2c3e50", width=200, height=500)
        self.sidebar_frame.grid(row=0, column=0, sticky=tk.NS)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Content area
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_propagate(False)

        # Sidebar button style
        style.configure("Sidebar.TButton",
                        font=("Arial", 15),
                        foreground="white",
                        background="#2c3e50",
                        borderwidth=0,
                        relief="solid",
                        padding=10)
        style.map("Sidebar.TButton",
                  background=[("active", "#1a252f")],
                  relief=[("pressed", "sunken")])

        # Sidebar buttons
        ttk.Button(self.sidebar_frame,
                   text="Dashboard",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("dashboard")).grid(row=0, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=1, column=0, sticky=tk.EW)

        ttk.Button(self.sidebar_frame,
                   text="New Sale",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("new_sale")).grid(row=2, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=3, column=0, sticky=tk.EW)

        ttk.Button(self.sidebar_frame,
                   text="Sales",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("sales")).grid(row=4, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=5, column=0, sticky=tk.EW)

        ttk.Button(self.sidebar_frame,
                   text="New Purchase",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("new_purchase")).grid(row=6, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=7, column=0, sticky=tk.EW)

        ttk.Button(self.sidebar_frame,
                   text="Purchases",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("purchases")).grid(row=8, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=9, column=0, sticky=tk.EW)

        ttk.Button(self.sidebar_frame,
                   text="Expenses",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("expenses")).grid(row=10, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=11, column=0, sticky=tk.EW)


        ttk.Button(self.sidebar_frame,
                   text="Products",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("products")).grid(row=12, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=13, column=0, sticky=tk.EW)



        ttk.Button(self.sidebar_frame,
                   text="Customers",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("customers")).grid(row=14, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=15, column=0, sticky=tk.EW)

        # Frames for content
        self.frames = {}
        for name, frame_class in {
            "dashboard": DashboardFrame,
            "new_sale": NewSaleFrame,
            "sales": SalesFrame,
            "new_purchase": NewPurchase,
            "purchases": PurchasesFrame,
            "expenses": ExpensesFrame,
            "products": ProductsFrame,
            "customers": CustomersFrame,
        }.items():
            frame = frame_class(self.content_frame, db)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_frame("dashboard")

    def show_frame(self, name):
        self.frames[name].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
