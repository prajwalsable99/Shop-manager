import streamlit as st
import mysql.connector
import pandas as pd
import time



from db_utils import init_page_details, connect_db

init_page_details('Dashboard', True)

def fetch_metrics():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(TotalAmount) FROM Orders")
    total_sales = float(cursor.fetchone()[0] or 0)


    cursor.execute("SELECT COUNT(*) FROM Orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(Price * StockQuantity) FROM Products")
    total_stock_value = float(cursor.fetchone()[0] or 0)

    cursor.execute("SELECT COUNT(*) FROM Customers")
    total_customers = cursor.fetchone()[0]

   
    cursor.execute("SELECT COUNT(DISTINCT Name) FROM Products")
    total_categories = cursor.fetchone()[0]

    cursor.execute("""
        SELECT c.Name, SUM(o.TotalAmount) AS TotalSpent
        FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        GROUP BY c.CustomerID, c.Name
        ORDER BY TotalSpent DESC
        LIMIT 3
    """)
    top_spending_customers = cursor.fetchall()

    cursor.execute("""
   SELECT COUNT(DISTINCT o.CustomerID) 
    FROM Orders o
    WHERE o.CustomerID IN (
    SELECT o.CustomerID 
    FROM Orders o
    GROUP BY o.CustomerID
    HAVING COUNT(o.OrderID) >= 2)

    """)
    customers_with_multiple_orders = cursor.fetchone()[0]  
  

    cursor.execute("""
        SELECT p.Name, SUM(oi.Quantity) AS TotalSold
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        GROUP BY p.ProductID
        ORDER BY TotalSold DESC
        LIMIT 3
    """)
    top_selling_products = cursor.fetchall()


    cursor.execute("""
        SELECT p.Name, SUM(oi.Quantity * p.Price) AS TotalRevenue
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        GROUP BY p.ProductID
        ORDER BY TotalRevenue DESC
        LIMIT 3
    """)
    top_selling_products_by_price = cursor.fetchall()

    conn.close()

  
    return {
        "total_sales": total_sales,
        "aov": total_sales / total_orders if total_orders > 0 else 0,
        "total_orders": total_orders,
        "total_stock_value": total_stock_value,
        "total_customers": total_customers,
        "total_categories": total_categories,
        "top_spending_customers": top_spending_customers,
        "customers_with_multiple_orders": customers_with_multiple_orders,
        'top_selling_products':top_selling_products,
        'top_selling_products_by_price':top_selling_products_by_price
    }

def display_metrics():
    metrics = fetch_metrics()

   
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Sales (₹)", f"₹{metrics['total_sales']:.2f}")
        st.metric("Average Order Value (₹)", f"₹{metrics['aov']:.2f}")

    with col2:
        st.metric("Product Categories", metrics['total_categories'])
        st.metric("Total Orders", metrics['total_orders'])

    with col3:
        st.metric("Remaining Stock (₹)", f"₹{metrics['total_stock_value']:.2f}")
        st.metric("Total Customers", metrics['total_customers'])


    st.write('----')
    
    c1, c2 = st.columns([3,1],vertical_alignment='center')
    with c1:
   
        st.write("### Top 3 Customers by Spending")
        st.table(pd.DataFrame(metrics['top_spending_customers'],columns=['customer','spend']))
    with c2:
    # Display the count of customers who placed more than or equal to 2 orders
        st.markdown(f"## Customers Retention rate" )
        st.subheader(metrics['customers_with_multiple_orders']/metrics['total_customers'] )

    df1=pd.DataFrame(data=metrics['top_selling_products'],columns=['product','quantity sold'])
    df2=pd.DataFrame(data=metrics['top_selling_products_by_price'],columns=['product','amount'])

    df1['quantity sold']=df1['quantity sold'].astype(float)
    df2['amount']=df2['amount'].astype(float)




    st.title("Top Selling Products Visualization")
    c1, c2 = st.columns(2,vertical_alignment='center')
    with c1:

        st.bar_chart(data=df1,x='product',y='quantity sold',color='#ffaa0088')
    with c2:
        st.bar_chart(data=df2,x='product',y='amount')


display_metrics()