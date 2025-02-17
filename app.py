import streamlit as st
import mysql.connector
import sys
import os
import time

#importing database connection file
sys.path.append(os.path.abspath("pages_nav")) 
import database 
# Set page layout and collapse sidebar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Combine CSS (hide sidebar) & JavaScript (reload on tab focus)
st.markdown("""
    <style>
        /* Hide Sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>

    <script>
        document.addEventListener("visibilitychange", function() {
            if (document.visibilityState === "visible") {
                window.parent.location.reload();
            }
        });
    </script>
""", unsafe_allow_html=True)

# ✅ Function to authenticate user
def authenticate_user(phone_num, password):
    conn = database.get_connection()
    if not conn:
        return None
    try:
        cursor=conn.cursor()
        query = """
            SELECT g.upi_id, g.bank_name, 
                    COALESCE(p.balance, h.balance) AS balance
            FROM gpay_app_users g
            LEFT JOIN pnb_bank p ON g.phone_num = p.phone_num AND g.bank_name = 'pnb_bank'
            LEFT JOIN hdfc_bank h ON g.phone_num = h.phone_num AND g.bank_name = 'hdfc_bank'
            WHERE g.phone_num = %s;
        """
        cursor.execute(query, (phone_num,))
            # Fetch the column names
        columns = [desc[0] for desc in cursor.description]
        # Fetch all results as a list of tuples
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        result = [dict(zip(columns, row)) for row in rows]
        print(result)
        conn.close()
        return result
    
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        conn.close()



# Streamlit code
#initializing session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
st.session_state.logged_in = False


# # to forcly close the sidebar
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# hide_sidebar_style = """
#     <style>
#         section[data-testid="stSidebar"] {
#             display: none !important;
#         }
#     </style>
# """
# st.markdown(hide_sidebar_style, unsafe_allow_html=True)


# --- LOGIN PAGE ---
st.markdown("<h1 style='text-align: center;'>MYₚₐᵧ✅</h1>", unsafe_allow_html=True)

st.subheader("🔑 Login to your Account")
with st.form("signup_form", clear_on_submit=False):
    st.write("Enter your Credentials")
    phone_num = st.text_input("📞 Phone Number")
    password = st.text_input("🔑 Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    result=authenticate_user(phone_num, password)
    if result: 
        st.toast("Login successful!")
        st.balloons()
        st.session_state.logged_in = True
        st.session_state.user_phone = phone_num
        st.session_state.user_password = password

        with st.spinner("Signing in...",show_time=True):
                time.sleep(1)
# redirect to home page of app
        st.switch_page("pages/home.py")
    else:
        st.error("Invalid credentials! Try again.")

col1,col2,col13,col4,col5,col6,col7,col8,col10,col9=st.columns(10,gap="small",vertical_alignment='center')
with col2:
    st.text("Not a User?")
with col1:
    if st.button("📝 Sign Up"):
        st.switch_page("pages/sign_up.py")
        


