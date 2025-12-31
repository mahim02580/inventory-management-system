import tkinter as tk
from tkinter import ttk
from dashboard import DashboardFrame
from product_management import ProductsFrame
from sales_management import SalesFrame
from customer_management import CustomersFrame
import database_management as db

SHOP_NAME = 'SHOP_NAME'
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(SHOP_NAME)
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
                   text="Products",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("products")).grid(row=2, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=3, column=0, sticky=tk.EW)


        ttk.Button(self.sidebar_frame,
                   text="Sales",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("sales")).grid(row=4, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=5, column=0, sticky=tk.EW)


        ttk.Button(self.sidebar_frame,
                   text="Customers",
                   style="Sidebar.TButton",
                   command=lambda: self.show_frame("customers")).grid(row=6, column=0, sticky=tk.EW)
        ttk.Separator(self.sidebar_frame, orient="horizontal").grid(row=7, column=0, sticky=tk.EW)

        # Frames for content
        self.frames = {}
        for name, frame_class in {
            "dashboard": DashboardFrame,
            "products": ProductsFrame,
            "sales": SalesFrame,
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
