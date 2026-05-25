import customtkinter as ctk
import sqlite3
from tkinter import ttk
from reportlab.pdfgen import canvas

def open_quotation_window(parent):
    print("Quatation window opened")
    window = ctk.CTkToplevel(parent)
    window.title("Quatation System")
    window.geometry("1200x900")

    quatation_items = []

    # Customer section
    ctk.CTkLabel(window, text='Customer Name').pack(pady=5)

    entry_customer = ctk.CTkEntry(window, width=300)
    entry_customer.pack(pady=5)

    # Product section

    ctk.CTkLabel(window, text='Select Product').pack(pady=5)

    conn = sqlite3.connect("computer_shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM products")
    products = [row[0] for row in cursor.fetchall()]

    conn.close

    product_dropdown = ctk.CTkComboBox(window, values=products, width=300)
    product_dropdown.pack(pady=5)

    ctk.CTkLabel(window, text="Quantity").pack(pady=5)

    entry_quantity = ctk.CTkEntry(window, width=100)
    entry_quantity.pack(pady=5)

    # Manual Item Section
    ctk.CTkLabel(window, text="Manual / Outsourced Item").pack(pady=5)

    entry_manual_name = ctk.CTkEntry(window, width=300, placeholder_text="Product Name")
    entry_manual_name.pack(pady=5)

    entry_manual_price = ctk.CTkEntry(window, width=300, placeholder_text="Price")
    entry_manual_price.pack(pady=5)

    entry_manual_quantity = ctk.CTkEntry(window, width=300, placeholder_text="Quantity")
    entry_manual_quantity.pack(pady=5)

    entry_supplier = ctk.CTkEntry(window, width=300, placeholder_text="Supplier Name")
    entry_supplier.pack(pady=5)

    # Table
    columns = ("Product", "Price", "Quantity", "Total")

    tree =ttk.Treeview(window, columns=columns, show="headings", height=6)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="x", padx=10, pady=10)

    # Total Label
    total_label = ctk.CTkLabel(window, text="Total: ₱0", font=("Arial", 20))
    total_label.pack(pady=10)

    # Discount section
    ctk.CTkLabel(window, text="Discount Value").pack(pady=5)

    entry_discount = ctk.CTkEntry(window, width=200)
    entry_discount.pack(pady=5)

    discount_type = ctk.CTkComboBox(window, values=["Percentage", "Fixed"], width=200)
    discount_type.pack(pady=5)

    # Service fee
    ctk.CTkLabel(window, text="Service Fee").pack(pady=5)

    entry_service_fee = ctk.CTkEntry(window, width=200)
    entry_service_fee.pack(pady=5)

    # Final total label
    final_total_label = ctk.CTkLabel(window, text="Final Total: ₱0", font=("Arial", 22))
    final_total_label.pack(pady=5)

    # Add Item Function
    def add_item():
        product_name = product_dropdown.get()
        quantity = entry_quantity.get()

        if not quantity:
            return
        
        if not quantity.isdigit():
            print("Quantity must be a number!")
            return  
        
        quantity = int(quantity)

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT price
            FROM products
            WHERE name = ?
        """, (product_name,))

        result = cursor.fetchone()

        conn.close()

        if result:
            price = result[0]
            total = price * quantity

            quatation_items.append(total)

            tree.insert(
                "",
                "end",
                values=(product_name, price, quantity, total)
            )

            overall_total = sum(quatation_items)

            total_label.configure(
                text=f"Total: ₱{overall_total}"
            )

            entry_quantity.delete(0, "end")

    def add_manual_item():
        product_name = entry_manual_name.get()
        price = entry_manual_price.get()
        quantity = entry_manual_quantity.get()
        supplier = entry_supplier.get()

        if not product_name or not price or not quantity:
            print(product_name)
            print(price)
            print(quantity)
            return
        
        price = float(price)
        quantity = int(quantity)

        total = price * quantity

        quatation_items.append(total)

        tree.insert(
            "",
            "end",
            values=(
                f"{product_name} ({supplier})",
                price,
                quantity,
                total
            )
        )

        overall_total = sum(quatation_items)

        total_label.configure(
            text=f"Total: ₱{overall_total}"
        )

        # clear entry
        entry_manual_name.delete(0, "end")
        entry_manual_price.delete(0, "end")
        entry_manual_quantity.delete(0, "end")
        entry_supplier.delete(0, "end")
    
    def calculate_final_total():
        total_amount = sum(quatation_items)

        discount_value = entry_discount.get()
        service_fee = entry_service_fee.get()

        if not discount_value:
            discount_value = 0

        if not service_fee:
            service_fee = 0

        discount_value = float(discount_value)
        service_fee = float(service_fee)

        discount_mode = discount_type.get()

        # percentage
        if discount_mode == "Percentage":
            discount_amount = (
                total_amount * discount_value / 100
            )

        else:
            discount_amount = discount_value

        final_total = (
            total_amount - discount_amount + service_fee
        )

        final_total_label.configure(
            text=F"Final Total: ₱{final_total}"
        )

        return final_total

    def save_quotation():
        customer_name = entry_customer.get()
            
        if not customer_name:
            print("Enter customer name")
            return

        total_amount = calculate_final_total()

        conn = sqlite3.connect("computer_shop.db")
        cursor = conn.cursor()

        # generate quotation number
        cursor.execute("""
            SELECT COUNT(*)
            FROM quotations
        """)

        count = cursor.fetchone()[0]

        quotation_number = f"Q-{count + 1}"

        # save quotation
        cursor.execute("""
            INSERT INTO quotations
            (quotation_number, customer_name, total_amount, status)
            VALUES (?, ?, ?, ?)
        """, (
            quotation_number,
            customer_name,
            total_amount,
            "Pending"
        ))

        quotation_id = cursor.lastrowid

        # save quotation 
        for item in tree.get_children():

            values = tree.item(item)["values"]

            product_name = values[0]
            price = values[1]
            quantity = values[2]
            total = values[3]

            cursor.execute("""
                INSERT INTO quotation_items
                (quotation_id, product_name, price, quantity, total)
                VALUES (?, ?, ?, ?, ?)
            """, (
                quotation_id,
                product_name,
                price,
                quantity,
                total
            ))

        conn.commit()
        conn.close()

        print("Quotation Saved")

    def generate_pdf():
        customer_name = entry_customer.get()

        pdf = canvas.Canvas("quotation.pdf")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 800, "COMPUTER SHOP QUOTATION")

        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, 70, f"Customer: {customer_name}")

        y = 720

        pdf.drawString(50, y, "Product")
        pdf.drawString(250, y, "Price")
        pdf.drawString(350, y, "Qty")
        pdf.drawString(450, y, "Total")

        y -= 30

        for item in tree.get_children():
            values = tree.item(item)["values"]

            pdf.drawString(50, y, str(values[0]))
            pdf.drawString(250, y, str(values[1]))
            pdf.drawString(350, y, str(values[2]))
            pdf.drawString(450, y, str(values[3]))

            y -= 25

        final_total = calculate_final_total()

        pdf.drawString(50, y - 20, f"Final Total: ₱{final_total}")

        pdf.save()

        print("PDF Generated")

    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    # Add item
    add_button = ctk.CTkButton(window, text="Add Item", command=add_item)
    add_button.pack(in_=button_frame, side="left", padx=10)

    # manual
    manual_button = ctk.CTkButton(window, text="Add Manual Item", command=add_manual_item)
    manual_button.pack(in_=button_frame, side="left", padx=10)
    
    # save
    save_button = ctk.CTkButton(window, text="Save Quotation", command=save_quotation)
    save_button.pack(in_=button_frame, side="left" ,padx=10)

    calculate_button = ctk.CTkButton(window, text="Calculate Final Total", command=calculate_final_total)
    calculate_button.pack(in_=button_frame, side="left" ,padx=10)

    # PDF
    pdf_button = ctk.CTkButton(window, text="Generate PDF", command=generate_pdf)
    pdf_button.pack(in_=button_frame, side="left", padx=10)
    

    