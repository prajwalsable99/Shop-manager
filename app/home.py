
import streamlit as st

from db_utils import init_page_details 

init_page_details('Home')




st.title("Shop Management App")
st.markdown("""
        ## Manage Your Shop with Ease
        Welcome to the **Shop Dashboard** – your one-stop solution for managing products, tracking sales, monitoring stock, and understanding your customer base. 
        This intuitive dashboard is designed to help shopkeepers streamline their operations and make data-driven decisions.

        ### Key Features:
        - **Sales Tracking**: Monitor total sales, average order value, and track customer spending patterns.
        - **Product Management**: Stay on top of your stock and keep track of product categories.
        - **Customer Insights**: Get an overview of your customer base, their spending habits, and order frequency.

        
    """)