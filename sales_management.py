import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from refund_management import RefundFrame
import helpers


class SalesFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent)
        self.dbmanager = dbmanager
        self.filter_var = tk.StringVar(value="all")
        # Options Frame ------------------------------------------------------------------------------------------------
        options_frame = tk.Frame(self, padx=20, pady=20)
        options_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.all_radio_button = tk.Radiobutton(options_frame, text="All", width=10, fg="white", bg="#3498db",
                                               command=self.all_invoices, font=("Arial", 15),
                                               activeforeground="white", activebackground="#1abc9c",
                                               selectcolor="#1abc9c",
                                               variable=self.filter_var, value="all", indicatoron=False, height=3)
        self.all_radio_button.grid(row=0, column=0, sticky=tk.NSEW)

        self.today_radio_button = tk.Radiobutton(options_frame, text="Today", width=10,
                                                 fg="white", bg="#3498db", command=self.today_invoices,
                                                 activeforeground="white", font=("Arial", 15),
                                                 activebackground="#1abc9c", selectcolor="#1abc9c",
                                                 variable=self.filter_var,
                                                 value="today", indicatoron=False, height=3)

        self.today_radio_button.grid(row=0, column=1, sticky=tk.NSEW)

        self.due_radio_button = tk.Radiobutton(options_frame, text="Due", width=10,
                                               fg="white", bg="#3498db", command=self.due_invoices,
                                               activeforeground="white", font=("Arial", 15),
                                               activebackground="#1abc9c", selectcolor="#1abc9c",
                                               variable=self.filter_var,
                                               value="due", indicatoron=False, height=3)
        self.due_radio_button.grid(row=0, column=2, sticky=tk.NSEW)
        self.custom_search_button = tk.Radiobutton(options_frame, text="Custom\nSearch", width=10, fg="white",
                                                   bg="#3498db",
                                                   command=self.custom_search, font=("Arial", 15),
                                                   activeforeground="white", activebackground="#1abc9c",
                                                   selectcolor="#1abc9c",
                                                   variable=self.filter_var, value="custom_search", indicatoron=False,
                                                   height=3)
        self.custom_search_button.grid(row=0, column=3, sticky=tk.NSEW)

        custom_search = tk.Frame(options_frame, highlightbackground="#2c3e50", highlightthickness=2)
        custom_search.grid(row=0, column=4, sticky=tk.NSEW)

        self.search_label = tk.Label(custom_search,
                 text="Search",
                 fg="white",
                 bg="#2c3e50",
                 width=15,
                 font=("Segoe UI", 14), )
        self.search_label.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)
        self.search_by_label = tk.Label(custom_search, text="Search by:", font=("Segoe UI", 10), )
        self.search_by_label.grid(row=1, column=0, pady=10, sticky=tk.E)

        self.search_filter = tk.StringVar(value="by_invoice")
        self.by_invoice_radiobutton = tk.Radiobutton(custom_search, text="Invoice", fg="white", bg="#3498db",
                                                     activeforeground="white", width=8, font=("Segoe UI", 10),
                                                     activebackground="#1abc9c", selectcolor="#1abc9c",
                                                     variable=self.search_filter,
                                                     value="by_invoice", command=self.search_by_invoice,
                                                     indicatoron=False)
        self.by_invoice_radiobutton.grid(row=1, column=1, pady=10, sticky=tk.W)
        self.by_phone_radiobutton = tk.Radiobutton(custom_search, text="Phone", fg="white", bg="#3498db",
                                                   activeforeground="white", width=8, font=("Segoe UI", 10),
                                                   activebackground="#1abc9c", selectcolor="#1abc9c",
                                                   variable=self.search_filter,
                                                   value="by_phone", command=self.search_by_phone, indicatoron=False)
        self.by_phone_radiobutton.grid(row=1, column=2, pady=10, sticky=tk.W)
        self.by_date_radiobutton = tk.Radiobutton(custom_search, text="Date", fg="white", bg="#3498db",
                                                  activeforeground="white", width=8, font=("Segoe UI", 10),
                                                  activebackground="#1abc9c", selectcolor="#1abc9c",
                                                  variable=self.search_filter,
                                                  value="by_date", command=self.search_by_date_range, indicatoron=False)
        self.by_date_radiobutton.grid(row=1, column=3, pady=10, padx=(0, 8), sticky=tk.W)
        self.option_label = tk.Label(custom_search, text="Invoice Number:", width=13, font=("Segoe UI", 10),
                                     anchor=tk.E, )
        self.option_label.grid(row=2, column=0, pady=(0, 10), padx=(7, 0), sticky=tk.E)

        self.invoice_or_phone_entry = tk.Entry(custom_search, width=10, font=("Segoe UI", 10), )
        self.invoice_or_phone_entry.grid(row=2, column=1, columnspan=2, pady=(0, 10), sticky=tk.EW)
        self.date_entry = DateEntry(
            custom_search,
            date_pattern="dd-mm-yyyy",
            width=18,
            showweeknumbers=False,
            background="#2c3e50",
            foreground="white",
            selectbackground="#1a252f",
        )
        self.date_entry.grid(row=2, column=1, pady=(0, 10), columnspan=2)
        self.date_entry.grid_remove()

        self.search_button = tk.Button(custom_search, text="Get", font=("Segoe UI", 8),
                                       command=self.get_invoice_by_search)
        self.search_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 8), sticky=tk.EW)

        # Sales Treeview Frame------------------------------------------------------------------------------------------
        self.sales_treeview_frame = tk.Frame(self)
        self.sales_treeview_frame.grid(row=1, column=0, sticky=tk.N)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Receive Payment", command=self.receive_payment)
        self.menu.add_command(label="Sales Return", command=self.sales_return)

        columns = ("Invoice", "Date", "Time", "Customer", "Amount", "Due")
        self.sales_treeview = ttk.Treeview(self.sales_treeview_frame, columns=columns, show="headings", height=16)

        self.sales_treeview.bind("<<TreeviewSelect>>", self.view_invoice)
        for col in columns:
            self.sales_treeview.heading(col, text=col)
        self.sales_treeview.column("Invoice", width=90, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Date", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Time", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Customer", width=300, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Amount", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.column("Due", width=100, stretch=False, anchor=tk.W)
        self.sales_treeview.tag_configure("evenrow", background="#f0f0f0")
        self.sales_treeview.tag_configure("oddrow", background="#FFFFFF")
        self.sales_treeview.grid(row=0, column=0, padx=(20, 0), sticky=tk.N)

        sales_treeview_scrollbar = ttk.Scrollbar(self.sales_treeview_frame, orient=tk.VERTICAL,
                                                 command=self.sales_treeview.yview)
        sales_treeview_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.sales_treeview.configure(yscrollcommand=sales_treeview_scrollbar.set)
        self.sales_treeview.bind("<Button-3>", self.show_menu)

        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=1, column=1, sticky=tk.NSEW)

        self.invoice_text = tk.Text(invoice_frame, width=40, height=33, font=("Courier New", 8), bd=2, )
        self.invoice_text.grid(row=0, column=0, padx=(20, 0))
        invoice_scrollbar = ttk.Scrollbar(invoice_frame, orient=tk.VERTICAL, command=self.invoice_text.yview)
        invoice_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.invoice_text.config(yscrollcommand=invoice_scrollbar.set)

        ttk.Button(invoice_frame, text="PRINT", command=self.print_invoice).grid(row=1, column=0, padx=(20, 0),
                                                                                 pady=(15, 0), sticky=tk.EW)

        self.all_radio_button.invoke()

    def show_menu(self, event):
        iid = self.sales_treeview.identify_row(event.y)
        if iid:
            self.sales_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def all_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        invoices = self.dbmanager.get_all_sales()[::-1]
        self.show_invoice(invoices)

    def today_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        invoices = self.dbmanager.get_today_sales()[::-1]
        self.show_invoice(invoices)

    def due_invoices(self):
        self.disable_search_mechanism()
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        due_invoices = [invoice for invoice in self.dbmanager.get_all_sales()[::-1] if invoice.due > 0]
        self.show_invoice(due_invoices)

    def custom_search(self):
        self.enable_search_mechanism()

    def enable_search_mechanism(self):
        self.search_label.config(fg="white")
        self.option_label.config(fg="black")
        self.search_by_label.config(fg="black")
        self.by_invoice_radiobutton.config(state=tk.NORMAL)
        self.by_phone_radiobutton.config(state=tk.NORMAL)
        self.by_date_radiobutton.config(state=tk.NORMAL)
        self.invoice_or_phone_entry.config(state=tk.NORMAL)
        self.search_button.config(state=tk.NORMAL)
        self.date_entry.config(state=tk.NORMAL)

    def disable_search_mechanism(self):
        self.search_label.config(fg="gray")
        self.option_label.config(fg="gray")
        self.search_by_label.config(fg="gray")
        self.by_invoice_radiobutton.config(state=tk.DISABLED)
        self.by_phone_radiobutton.config(state=tk.DISABLED)
        self.by_date_radiobutton.config(state=tk.DISABLED)
        self.invoice_or_phone_entry.config(state=tk.DISABLED)
        self.search_button.config(state=tk.DISABLED)
        self.date_entry.config(state=tk.DISABLED,)

    def view_invoice(self, event):
        selected_item = self.sales_treeview.selection()[0]
        invoice_id = self.sales_treeview.item(selected_item, "values")[0]
        invoice = self.dbmanager.get_invoice(invoice_id)
        ready_invoice = helpers.make_invoice_for_purchase(invoice)

        self.invoice_text.config(state=tk.NORMAL)
        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert("1.0", ready_invoice)
        self.invoice_text.config(state=tk.DISABLED)

    def print_invoice(self):
        invoice = self.invoice_text.get("1.0", tk.END)
        if invoice == "\n":
            messagebox.showerror(title="Error", message="Please select an invoice to print!")
            return

        helpers.print_out_invoice(invoice)

    def show_invoice(self, invoices):
        self.sales_treeview.delete(*self.sales_treeview.get_children())
        for i, invoice in enumerate(invoices):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.sales_treeview.insert(
                "",
                tk.END,
                values=(invoice.id, invoice.date.strftime("%d-%m-%Y"), invoice.time.strftime("%I:%M %p"),
                        f"{invoice.customer.name} - {invoice.customer.phone}",
                        invoice.total_payable, invoice.due), tags=tag)

    def get_invoice_by_search(self):
        filter_option = self.search_filter.get()

        if filter_option == "by_invoice":
            invoice_no = self.invoice_or_phone_entry.get()
            invoice = self.dbmanager.get_invoice(invoice_no)
            if not invoice:
                messagebox.showerror(title="Not Found", message="No invoice found with this invoice number.")
                return
            self.show_invoice([invoice])

        elif filter_option == "by_phone":
            phone_number = self.invoice_or_phone_entry.get()
            customer = self.dbmanager.get_customer_by_phone(phone_number)
            if not customer:
                messagebox.showerror(title="Not Found", message="No invoices found with this phone number.")
                return
            purchases_of_the_customer = customer.purchases
            self.show_invoice(purchases_of_the_customer)

        elif filter_option == "by_date":
            date = self.date_entry.get()
            day, month, year = date.split("-")
            date_obj = datetime.date(day=int(day), month=int(month), year=int(year))
            invoices = self.dbmanager.get_invoices_by_date(date_obj)
            if not invoices:
                messagebox.showerror(title="Not Found", message="No invoices found for this date.")
                return
            self.show_invoice(invoices)

    def receive_payment(self):
        selected_invoice_id = self.sales_treeview.selection()[0]
        selected_invoice = self.sales_treeview.item(selected_invoice_id, "values")
        due_amount = int(selected_invoice[-1])
        print(due_amount)
        if due_amount == 0:
            messagebox.showinfo(title="No Due Payment", message="This invoice has no due payment.")
            return
        else:
            def update_invoice_with_new_payment():
                received_amount = int(payment_received_entry.get())
                if received_amount > invoice.due:
                    messagebox.showinfo(message="Received amount is greater than due amount. Check and try again!")
                    return
                invoice.paid += received_amount
                invoice.due -= received_amount
                self.dbmanager.update_changes()
                payment_win.destroy()
                self.all_radio_button.invoke()

            payment_win = tk.Toplevel(self.sales_treeview_frame)
            payment_win.title("Receive Payment")
            payment_win.config(padx=20, pady=20)

            self.center_window(payment_win, 215, 260)

            invoice_id = selected_invoice[0]
            invoice = self.dbmanager.get_invoice(invoice_id)
            # Invoice No
            tk.Label(payment_win, text=f"Invoice No", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.id}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=0, column=2, sticky=tk.W)

            # Total Payable
            tk.Label(payment_win, text=f"Total Payable", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.total_payable}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=1, column=2, sticky=tk.W)

            # Total Payable
            tk.Label(payment_win, text=f"Paid", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.paid}", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=2, column=2, sticky=tk.W)

            # Due
            tk.Label(payment_win, text=f"Due", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=0, sticky=tk.W)
            tk.Label(payment_win, text=":", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=1, sticky=tk.W)
            tk.Label(payment_win, text=f"{invoice.due}", fg="red", font=("Segoe UI", 12, "bold"),
                     anchor=tk.W, ).grid(row=3, column=2, sticky=tk.W)

            tk.Label(payment_win, text="Payment Received", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4,
                                                                                                              column=0,
                                                                                                              sticky=tk.W)
            tk.Label(payment_win, text=":", font=("Segoe UI", 12, "bold"), anchor=tk.W, ).grid(row=4, column=1,
                                                                                               sticky=tk.W)
            payment_received_entry = tk.Entry(payment_win, width=6, font=("Segoe UI", 12))
            payment_received_entry.focus_set()
            payment_received_entry.grid(row=4, column=2)
            tk.Button(payment_win, text="Confirm", command=update_invoice_with_new_payment).grid(row=5, column=1,
                                                                                                 columnspan=2, pady=10,
                                                                                                 sticky=tk.NSEW)
            payment_win.transient()
            payment_win.grab_set()  # modal behavior
            payment_win.resizable(False, False)

    def center_window(self, win, custom_height, custom_width):
        win.update_idletasks()
        width = custom_width
        height = custom_height
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def sales_return(self):
        sales_return_window = tk.Toplevel(self.sales_treeview_frame)
        sales_return_window.title("Receive Payment")
        sales_return_window.config(padx=20, pady=20)
        self.center_window(sales_return_window, 550, 1085)
        sales_return_window.transient()
        sales_return_window.grab_set()  # modal behavior
        sales_return_window.resizable(False, False)
        selected_invoice_id = self.sales_treeview.selection()[0]
        invoice_id = self.sales_treeview.item(selected_invoice_id, "values")[0]
        invoice = self.dbmanager.get_invoice(invoice_id)
        RefundFrame(sales_return_window, invoice, self.dbmanager)

    def search_by_invoice(self):
        self.option_label.config(text="Invoice Number:")
        self.show_invoice_or_phone_entry_search()

    def search_by_phone(self):
        self.option_label.config(text="Phone Number:")
        self.show_invoice_or_phone_entry_search()

    def search_by_date_range(self):
        self.option_label.config(text="Date:")
        self.show_custom_date_search()

    def show_invoice_or_phone_entry_search(self):
        self.date_entry.grid_remove()
        self.invoice_or_phone_entry.grid()

    def show_custom_date_search(self):
        self.invoice_or_phone_entry.grid_remove()
        self.date_entry.grid()
