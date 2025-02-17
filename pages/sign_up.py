import streamlit as st
import mysql.connector
import sys
import os

sys.path.append(os.path.abspath("pages_nav"))  # Add directory to path
import database  # Now you can import


def register_user(first_na,last_na,phone_num,email,bank_name):
    conn = database.get_connection()
    if not conn:
        return "Database connection error."
    try:
        cursor = conn.cursor()
        query = "INSERT INTO gpay_app_users(first_name,last_name,phone_num,bank_name,email) VALUES (%s,%s,%s, %s, %s)"
        cursor.execute(query, (first_na,last_na,phone_num,bank_name,email))
        conn.commit()
        cursor.close()
        return "User registered successfully! Please log in."
    except mysql.connector.Error as e:
        conn.rollback()
        return f"Error: {e}"
    finally:
        conn.close()

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)
# Initialize session state
if "registered" not in st.session_state:
    st.session_state.registered = False

st.markdown("<h1 style='text-align: center;'>MYₚₐᵧ✅</h1>", unsafe_allow_html=True)
st.subheader("📝 Sign Up")

with st.form("signup_form", clear_on_submit=True):
    st.write("Enter your Credentials")
    first_na = st.text_input("👤First Name ", key="first Name")
    last_na = st.text_input("👤 Last Name", key="Last Name")
    email = st.text_input("👤 email", key="signup_email")
    new_phone = st.text_input("📞 Phone Number", max_chars=10, key="signup_phone")
    bank_name = option = st.selectbox("Bank",
                                      ("hdfc_bank","pnb_bank"),placeholder="Select Bank")

    checkbox_val = st.checkbox("Final Check")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    if submitted:
        if checkbox_val:
            # sql database check
            result = register_user(first_na,last_na,new_phone,email,bank_name)
            if "successfully" in result.lower():
                st.toast(result)
                st.balloons()
                st.toast("Registration Successfull")
                st.session_state.registered = True    
            else:  
                st.toast("Registration Unsuccessfull")   
                ## to be refine afterwards
                st.error(result)
        else:
            st.warning('Please tick the checkbox', icon="⚠️")

# Show Home button only after registration
if st.session_state.registered:
    if st.button("🔙 Back to Login"): 
        st.switch_page("app.py")