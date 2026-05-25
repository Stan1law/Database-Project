import customtkinter as ctk
import sqlite3
from tkinter import ttk


def open_products_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Products")
    window.geometry("700x700")

    # Entries
    ctk.CTkLabel(window, text="Product Name").pack()
    entry_name = ctk.CTkEntry(window)
    entry_name.pack()

    ctk.CTkLabel(window, text="Brand").pack()
    entry_brand = ctk.CTkEntry(window)
    entry_brand.pack()

    ctk.CTkLabel(window, text="Price").pack()
    entry_price = ctk.CTkEntry(window)
    entry_price.pack()

    ctk.CTkLabel(window, text="Stock").pack()
    entry_stock = ctk.CTkEntry(window)
    entry_stock.pack()


    # Save Function 
    def save_product():
        name = entry_name.get()
        brand = entry_brand.get()
        price = entry_price.get()
        stock = entry_stock.get()

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products (name, brand, price, stock)
            VALUES (?, ?, ?, ?)
        """, (name, brand, price, stock))

        conn.commit()
        conn.close()

        print("Saved!")

        # clear entries
        entry_name.delete(0, "end")
        entry_brand.delete(0, "end")
        entry_price.delete(0, "end")
        entry_stock.delete(0, "end")

        load_products()

    save_button = ctk.CTkButton(window, text="Save", command=save_product)
    save_button.pack(pady=5)


    # Table
    columns = ("ID", "Name", "Brand", "Price", "Stock")

    table_frame = ctk.CTkFrame(window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)


    # Load Products 
    def load_products():
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()


    def delete_product():
        selected = tree.selection()

        if not selected:
            print("No product selected")
            return

        item = tree.item(selected[0])
        product_id = item['values'][0]

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

        print("Deleted!")
        load_products()


    def select_product(event):
        selected = tree.selection()
        if not selected:
            return

        item = tree.item(selected[0])
        values = item['values']

        entry_name.delete(0, "end")
        entry_name.insert(0, values[1])

        entry_brand.delete(0, "end")
        entry_brand.insert(0, values[2])

        entry_price.delete(0, "end")
        entry_price.insert(0, values[3])

        entry_stock.delete(0, "end")
        entry_stock.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", select_product)


    def update_product():
        selected = tree.selection()

        if not selected:
            print("No product selected")
            return

        item = tree.item(selected[0])
        product_id = item['values'][0]

        name = entry_name.get()
        brand = entry_brand.get()
        price = entry_price.get()
        stock = entry_stock.get()

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE products
            SET name = ?, brand = ?, price = ?, stock = ?
            WHERE id = ?
        """, (name, brand, price, stock, product_id))

        conn.commit()
        conn.close()

        print("Updated!")
        load_products()

    tree.pack(fill="both", expand=True)

    # button frame
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(fill="x", pady=5)

    # refresh buttons
    refresh_button = ctk.CTkButton(button_frame, text="Refresh", command=load_products)
    refresh_button.pack(side="left", padx=5)

    # delete button
    delete_button = ctk.CTkButton(button_frame, text="Delete Selected", command=delete_product)
    delete_button.pack(side="left", padx=5)

    # update_button
    update_button = ctk.CTkButton(button_frame, text="Update Selected", command=update_product)
    update_button.pack(side="left", padx=5)
    
    # auto load
    load_products()