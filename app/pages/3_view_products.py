import streamlit as st
from db_utils import connect_db ,init_page_details 

init_page_details('Products',True)

def view_products():
    st.subheader("Existing Products")


    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, Name, StockQuantity, Price FROM Products")
    products = cursor.fetchall()
    conn.close()

   
    if products:
        columns = ["Product ID", "Name", "Stock Quantity", "Price"]


        products_dict = [
            {columns[i]: product[i] for i in range(len(columns))} for product in products
        ]

        st.table(products_dict)
    else:
        st.write("No products available.")

view_products()