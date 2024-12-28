import streamlit as st
from db_utils import connect_db ,init_page_details 

init_page_details('Add Stock')

def add_product():
    st.subheader("Add a New Product")


    name = st.text_input("Product Name")
    stock_quantity = st.number_input("Stock Quantity", min_value=1)
    price = st.number_input("Price", min_value=0.0)

    if st.button("Add Product"):
        if name and stock_quantity and price:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Products (Name, StockQuantity, Price) VALUES (%s, %s, %s)",
                (name, stock_quantity, price)
            )
            conn.commit()  
            conn.close()
            st.success("Product added successfully!")
        else:
            st.error("Please fill out all fields!")

add_product()
