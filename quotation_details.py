import customtkinter as ctk
import sqlite3
from tkinter import ttk


def open_quotation_details(parent, quotation_number):

    print("Opening quotation:", quotation_number)

    window = ctk.CTkToplevel(parent)
    window.title(f"Quotation Details - {quotation_number}")
    window.geometry("700x500")

    title = ctk.CTkLabel(
        window,
        text=f"Quotation: {quotation_number}",
        font=("Arial", 22)
    )

    title.pack(pady=10)

    columns = (
        "Product",
        "Price",
        "Quantity",
        "Total"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=15
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    conn = sqlite3.connect("computer_shop.db")
    cursor = conn.cursor()

    # get quotation id
    cursor.execute("""
        SELECT quotation_id
        FROM quotations
        WHERE quotation_number = ?
    """, (quotation_number,))

    result = cursor.fetchone()

    if result:

        quotation_id = result[0]

        cursor.execute("""
            SELECT
            product_name,
            price,
            quantity,
            total
            FROM quotation_items
            WHERE quotation_id = ?
        """, (quotation_id,))

        rows = cursor.fetchall()

        print(rows)

        for row in rows:
            tree.insert("", "end", values=row)

    else:
        print("Quotation not found")

    conn.close()