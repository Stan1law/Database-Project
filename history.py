import customtkinter as ctk
import sqlite3
from tkinter import ttk
from quotation_details import open_quotation_details

def open_history_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Quotation History")
    window.geometry("700x500")

    columns = (
    "Quotation No",
    "Customer",
    "Total Amount",
    "Status"
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

    ctk.CTkLabel(window, text="Search Quotation").pack(pady=5)

    search_entry = ctk.CTkEntry(window, width=300)
    search_entry.pack(pady=5)

    search_button = ctk.CTkButton(window, text="Search", command=lambda: load_quotations(search_entry.get()))
    search_button.pack(pady=10)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def mark_as_sold():
        selected = tree.selection()

        if not selected:
            print("Select quotation")
            return
        
        item = tree.item(selected[0])

        quotation_number = item["values"][0]

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

            # get quotation items
            cursor.execute("""
                SELECT product_name, quantity
                FROM quotation_items
                WHERE quotation_id = ?
            """, (quotation_id,))

            items = cursor.fetchall()

            for product_name, quantity in items:
                # reduce stock
                cursor.execute("""
                    UPDATE products
                    SET stock = stock - ?
                    WHERE name = ?
                """, (
                    quantity,
                    product_name
                ))

            # update quotation status
            cursor.execute("""
                UPDATE quotations
                SET status = 'Sold'
                WHERE quotation_id = ?
            """, (quotation_id,))

        conn.commit()
        conn.close()

        print("Quotation marked as SOLD")

        load_quotations()
    
    sold_botton = ctk.CTkButton(window, text="Mark as sold", command=mark_as_sold)
    sold_botton.pack(pady=10)

    def load_quotations(search_text=""):
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
            quotation_number,
            customer_name,
            total_amount,
            status
            FROM quotations
            WHERE quotation_number LIKE ?
            OR customer_name LIKE ?
        """, (
            f"%{search_text}%",
            f"%{search_text}%"
        ))

        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()

    load_quotations()

    def open_selected_quotation(event):
        print("Double click")
        selected = tree.selection()

        if not selected:
            return
        
        item = tree.item(selected[0])

        quotation_number = item["values"][0]

        open_quotation_details(window, quotation_number)

    tree.bind("<Double-Button-1>", open_selected_quotation)