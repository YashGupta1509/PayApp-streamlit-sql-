import streamlit as st
import mysql.connector
import os
import time
import pymysql
import pandas as pd
from sqlalchemy import create_engine
# ✅ Database Connection Function

# def get_connection():
#     user = os.environ.get('Sql_name')  # Get credentials from environment
#     password_ = os.environ.get('Sql_password')
#     try:
#         conn = mysql.connector.connect(
#             host='127.0.0.1',  # Change to RDS hostname if needed
#             user=user,
#             password=password_,
#             database='world',
#             auth_plugin='mysql_native_password'
#         )
#         return conn
#     except mysql.connector.Error as e:
#         st.error(f"Database connection error: {e}")
#         return None
    
# aws setup
def get_connection():
    user = os.environ.get('Sql_name')  # Get credentials from environment
    password_ = os.environ.get('Sql_password')
    try:
        conn = mysql.connector.connect(host='mypay-database.cpyiiusea4t5.ap-south-1.rds.amazonaws.com',user='admin',password='YashGupta15',database='world')
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None