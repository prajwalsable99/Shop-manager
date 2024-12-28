import mysql.connector
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def connect_db():
    """Connect to the MySQL database and return the connection object."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )




def init_page_details(page_title,wide_flag=False):

    if (wide_flag):
        layout='wide'
    else:
        layout='centered'

    st.set_page_config(
        page_title=page_title,
        page_icon="🛒", 
        initial_sidebar_state="expanded",
        layout=layout
    )


