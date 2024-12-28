import streamlit as st
from db_utils import connect_db ,init_page_details

init_page_details('Update Stock')


def update_product_stock():
    st.subheader("Update Product Stock and Price")

 
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, Name FROM Products")
    products = cursor.fetchall()
    conn.close()

    if products:
        product_choices = [f"{product[0]} - {product[1]}" for product in products] 
        selected_product = st.selectbox("Select Product", product_choices)

        product_id = int(selected_product.split(" - ")[0])

      
        new_stock_quantity = st.number_input("New Stock Quantity", min_value=0)
        new_price = st.number_input("New Price", min_value=0.0)

        if st.button("Update Stock and Price"):
            if new_stock_quantity >= 0 and new_price >= 0:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Products SET StockQuantity = %s, Price = %s WHERE ProductID = %s",
                    (new_stock_quantity, new_price, product_id)
                )
                conn.commit()  
                conn.close()
                st.success(f"Stock and Price for Product ID {product_id} updated!")
            else:
                st.error("Stock quantity and price must be non-negative values.")
    else:
        st.write("No products available to update.")

update_product_stock()

# Call the function to render the page