import streamlit as st
from db_utils import connect_db,init_page_details
import time  


init_page_details('Add Order')

def create_order():
    st.subheader("Create a New Order")

  
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID, Name FROM Customers")
    customers = cursor.fetchall()
    conn.close()

    if customers:
        customer_choices = [f"{customer[0]} - {customer[1]}" for customer in customers]
        selected_customer = st.selectbox("Select Customer", customer_choices)
        customer_id = int(selected_customer.split(" - ")[0])

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT ProductID, Name, Price, StockQuantity FROM Products")
        products = cursor.fetchall()
        conn.close()

       
        order_items = []
        total_amount = 0  

        for product in products:
            product_id, product_name, product_price, stock_quantity = product

            if stock_quantity > 0:  
                selected = st.checkbox(f"{product_name} (₹{product_price}) - Stock: {stock_quantity}", key=product_id)

                if selected:
                    quantity = st.number_input(f"Enter Quantity for {product_name}", min_value=1, max_value=stock_quantity, step=1, key=f"quantity_{product_id}")
                    total_price = product_price * quantity
                    order_items.append({
                        'product_id': product_id,
                        'product_name': product_name,
                        'price': product_price,
                        'quantity': quantity,
                        'total_price': total_price  
                    })
                    total_amount += total_price  

       
        if order_items:
            st.subheader("Selected Items for the Order:")
            for item in order_items:
                st.write(f"{item['product_name']} - {item['quantity']} x ₹{item['price']} = ₹{item['total_price']}")

            st.write(f"Total Order Amount: ₹{total_amount}")

            if st.button("Create Order"):
                with st.spinner('Creating order... Please wait.'):

           
                    time.sleep(2) 

                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO Orders (CustomerID, TotalAmount, OrderDate) VALUES (%s, %s, NOW())",
                            (customer_id, total_amount)
                        )
                        conn.commit()
                        order_id = cursor.lastrowid
                        
                      
                        for item in order_items:
                            cursor.execute(
                                "INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price, TotalPrice) VALUES (%s, %s, %s, %s, %s)",
                                (order_id, item['product_id'], item['quantity'], item['price'], item['total_price'])
                            )

                        for item in order_items:
                            cursor.execute(
                                "UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s",
                                (item['quantity'], item['product_id'])
                            )
                        conn.commit()
                        conn.close()

                        st.success(f"Order created successfully! Order ID: {order_id}")

                
                        time.sleep(2)
                        st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.stop()

        else:
            st.write("No products selected yet.")
    else:
        st.write("No customers available.")

create_order()
