import streamlit as st
from db_utils import connect_db,init_page_details
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import os
from io import BytesIO


init_page_details('View orders',True)

def generate_pdf(order_id, customer_name, order_items, total_amount):
    
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
   
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontSize=20, alignment=1, fontName='Helvetica-Bold')
    section_style = ParagraphStyle('Section', fontSize=14, alignment=0, fontName='Helvetica-Bold', spaceAfter=12)
    content_style = styles['Normal']
    
    
    title = Paragraph("Invoice", title_style)
    
    # Order and Customer Info
    order_info = [
        ("Order ID:", str(order_id)),
        ("Customer Name:", customer_name),
        ("Total Amount:", f"{total_amount} (INR)"),
    ]
    
    order_info_table = Table(order_info, colWidths=[100, 350])
    order_info_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')]))

    
    item_data = [["Product Name", "Quantity", "Price", "Total Price"]]
    for item in order_items:
        item_data.append([item['product_name'], item['quantity'], f"{item['price']} (INR)", f"{item['total_price']} (INR) "])
    
    item_table = Table(item_data)
    item_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
    
 
    total_section = Paragraph(f"<b>Total Amount: {total_amount} (INR) </b>", section_style)

    
    elements = [title, order_info_table, total_section, item_table]
    doc.build(elements)

    
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data
def view_orders():
    st.subheader("All Orders")


    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT o.OrderID, c.Name AS CustomerName, o.TotalAmount, o.OrderDate FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID")
    orders = cursor.fetchall()
    conn.close()

    if orders:
        order_data = []
        for order in orders:
            order_id, customer_name, total_amount, order_date = order
            order_data.append([order_id, customer_name, total_amount, order_date])

     
        column_names = ["Order ID", "Customer Name", "Total Amount", "Order Date"]
        
        st.table(pd.DataFrame(order_data, columns=column_names))
        

        selected_order_id = st.selectbox("Select an Order to Download PDF", [order[0] for order in orders], index=0)

        if selected_order_id:
          
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT p.Name, oi.Quantity, oi.Price, oi.TotalPrice FROM OrderItems oi JOIN Products p ON oi.ProductID = p.ProductID WHERE oi.OrderID = %s", (selected_order_id,))
            order_items = cursor.fetchall()
            conn.close()

           
            order_items_list = [{
                'product_name': item[0],
                'quantity': item[1],
                'price': item[2],
                'total_price': item[3]
            } for item in order_items]
            total_bill=0
            for item in order_items_list:
                total_bill+=item['total_price']
         
            if st.button(f"Generate PDF for Order {selected_order_id}"):
                pdf_buffer = generate_pdf(selected_order_id, customer_name, order_items_list, total_bill)

                # Provide the PDF for download
                st.download_button(
                    label="Download PDF Invoice",
                    data=pdf_buffer,
                    file_name=f"Order_{selected_order_id}_Invoice.pdf",
                    mime="application/pdf"
                )

    else:
        st.write("No orders available.")


view_orders()