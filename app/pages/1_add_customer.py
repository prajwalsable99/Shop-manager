import streamlit as st
import mysql.connector
from db_utils import connect_db  
import pandas as pd

def fetch_all_customers():
    conn = connect_db()
    cursor = conn.cursor()

   
    query = "SELECT CustomerID, Name, Phone, CreatedAt FROM Customers"
    cursor.execute(query)
    customers = cursor.fetchall()
    
    conn.close()
    return customers


def display_all_customers():
    st.title("All Customers")

   
    customers = fetch_all_customers()

    if customers:
     
        st.dataframe(customers)
    else:
        st.write("No customers found.")


def add_customer(name, phone):
    conn = connect_db()
    cursor = conn.cursor()

   
    query = """
        INSERT INTO Customers (Name, Phone)
        VALUES (%s, %s)
    """
    values = (name, phone)

    try:
        cursor.execute(query, values)
        conn.commit()
        st.success("Customer added successfully!")
    except mysql.connector.Error as err:
        conn.rollback()
        st.error(f"Error adding customer: {err}")
    finally:
        conn.close()


def display_add_customer_form():
    st.title("Add New Customer")

  
    with st.form(key='add_customer_form'):
        name = st.text_input("Customer Name", max_chars=100)
        phone = st.text_input("Phone Number", max_chars=10)

        submit_button = st.form_submit_button("Add Customer")

        if submit_button:
            if name and phone:
                add_customer(name, phone)
            else:
                st.error("Please fill all the fields.")



display_add_customer_form()


if st.button("Show All Customers"):
    display_all_customers()