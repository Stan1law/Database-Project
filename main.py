import customtkinter as ctk
from database import connect_db
from products import open_products_window
from quotation import open_quotation_window
from history import open_history_window

connect_db()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Computer Shop System")
app.geometry("500x400")

title = ctk.CTkLabel(app, text="Computer Shop System", font=("Arial", 24))
title.pack(pady=20)

btn_products = ctk.CTkButton(app, text="Products", width=200, command=lambda: open_products_window(app))
btn_products.pack(pady=10)

btn_quotation = ctk.CTkButton(app, text="Quotation", width=200, command=lambda: open_quotation_window(app))
btn_quotation.pack(pady=10)

btn_history = ctk.CTkButton(app, text="Quotation History", width=200, command=lambda: open_history_window(app))
btn_history.pack(pady=10)

btn_customers = ctk.CTkButton(app, text="Customers", width=200)
btn_customers.pack(pady=10) 

btn_sales = ctk.CTkButton(app, text="Sales", width=200) 
btn_sales.pack(pady=10)

btn_exit = ctk.CTkButton(app, text="Exit", width=200, command=app.destroy)
btn_exit.pack(pady=10)

app.mainloop()