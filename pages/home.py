import streamlit as st
import time
import datetime
import mysql.connector 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import july
from july.utils import date_range
import pandas as pd
import sys
import os
import time
from decimal import Decimal

#importing database connection file
sys.path.append(os.path.abspath("pages_nav")) 
import database  

try:
    # to forcly prevent sidebar to display
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    hide_sidebar_style = """
        <style>
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    if "logged_in" in st.session_state or 'user_phone' in st.session_state:
            
        def get_user_details(phone_num):
            
            conn = database.get_connection()
            cursor=conn.cursor()
            query = """
                SELECT g.first_name,g.upi_id, g.bank_name, 
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

            query2 = """ SELECT distinct(phone_num) FROM gpay_app_users; """
            cursor.execute(query2)
            options=cursor.fetchall()
            #print(options)
            result.append(options)
            conn.close()
            return result
        
        def transfer_money(s_upi_id, r_num, amt):
            conn = database.get_connection()
            cursor=conn.cursor()
            try:        
                cursor.execute("SET @message = '';")
                cursor.callproc("gpay_upi", (s_upi_id, r_num, amt, "@message"))
                # cursor.execute("SELECT @message;")
                message = 'Success'
                conn.commit()
                return message
            
            except Exception as e:
                conn.rollback()
                return f"Error: {str(e)}"
            finally:
                conn.close()


        def dashboard(upi_id):
            conn = database.get_connection()
            cursor=conn.cursor()
            try:
                cursor.execute("""create temporary table temp as(        
                        WITH RECURSIVE all_days AS (
                            SELECT 1 AS day_num
                            UNION ALL
                            SELECT day_num + 1 FROM all_days WHERE day_num < 31
                        )
                        SELECT 
                            m.month_num, 
                            d.day_num, 
                            0 AS amount
                        FROM 
                            (SELECT 1 AS month_num UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL 
                            SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL 
                            SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL 
                            SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12) m
                        JOIN 
                            all_days d 
                        ON 
                            d.day_num <= DAY(LAST_DAY(CONCAT(YEAR(NOW()),'-', m.month_num, '-01')))
                        );""")
                
                query3= """
                        with cte as(
                        select month(transaction_date) as month_num, day(transaction_date) as day_num, sum(amount)amt
                        from gpay_app_transactions 
                        where upi_id= %s and action= 'Debit'
                        group by month_num, day_num
                        )
                        select t.month_num,t.day_num,
                        case 
                        when amt is null then amount
                        else amt
                        end
                        as amount_spend
                        from cte g
                        right join temp t
                        on g.month_num=t.month_num and g.day_num=t.day_num
                        order by t.month_num asc,t.day_num asc; 
                    """
                cursor.execute(query3, (upi_id,))

    # Fetch the column names
                columns = [desc[0] for desc in cursor.description]
    # Fetch all results as a list of tuples
                rows = cursor.fetchall()
    # Convert rows to a list of dictionaries
                result = [list(row)for row in rows]
                conn.commit()
                # print(result)
                return result
            
            except Exception as e:
                conn.rollback()
                return f"Error: {str(e)}"
            finally:
                conn.close()

        phone_num = st.session_state.user_phone
        user_password = st.session_state.user_password
        
        tab1, tab2, tab3 = st.tabs(["Home", "PaY","Dashboard"])

        with tab1:
        #streamlit app interface
            st.markdown("<h1 style='text-align: center;'>MYₚₐᵧ✅</h1>", unsafe_allow_html=True)
            result= get_user_details(phone_num)
            if result:
                col1,col2,col3=st.columns(3)
                with col1:
                    st.subheader("👤Hi, "+result[0]['first_name']+" ☺️")
                    selected_account = st.selectbox("Select Account", result[:len(result)-1], 
                                                    format_func=lambda x: f"{x['bank_name']}-{x['upi_id']}")
                with col1:
                    if selected_account:
            
                        upi_id = selected_account["upi_id"]
                        balance = selected_account["balance"]
                        st.write(f"**UPI ID:** {upi_id}")
                        st.write(f"**Bank:** {selected_account['bank_name']}")
                        st.write(f"**Balance:** ₹{balance}")
                               
                
# Money Transfer Section
        with tab2:
            col1,col2,col3=st.columns(3)
            with col2:    
                st.subheader("🔄 Transfer Money")
                options=[]
                for i in result[-1]:
                    options.append(i[0])

                r_num = st.selectbox("Enter the Number",options,placeholder="Select Contact/PhoneNumber",
                                    index=None)
                amt = st.number_input("💸 Enter Amount",value=None,format="%0.2f",placeholder='0.00')
                
                
                if st.button("Send Money"):
                    print(upi_id,r_num,amt)
                    # if amt > balance:
                    #     pass
                        # st.error("❌ Insufficient Balance")
                    # else:
                    result =transfer_money(upi_id, r_num, amt)
                    if "SUCCESS" in result.upper():
                        
                        with st.spinner("Processing Request...", show_time=False):
                            time.sleep(1.5)
                        st.success("Transaction Successfull")
                        time.sleep(1)
                    else:
                        with st.spinner("Wait for it...", show_time=False):
                            time.sleep(1.5)
                            if 'Insufficient Balance' in result:
                                st.error(result)
                            else:
                                print(result)
                                st.error("Error Processing Your Request")
                                time.sleep(1)
                    st.rerun()
# Dashboard
        with tab3:
            data=dashboard(upi_id)
            
            data=pd.DataFrame(data,columns=['1','2','3'])
            ## Create data
            dates = date_range("2025-01-01", "2025-12-31")

            plt.style.use("dark_background")
            
            fig, ax = plt.subplots(figsize=(30,25))
        
            custom_cmap = mcolors.LinearSegmentedColormap.from_list("black", ["white", "green"])
            # Tell july to make a plot in a specific axes
            july.heatmap(
                dates=dates,
                data=data['3'],
                cmap=custom_cmap,
                horizontal=True,
                value_label=True,
                date_label=False,
                weekday_label=True,
                month_label=True,
                year_label=True,
                colorbar=True,
                month_grid=True,
                fontfamily="monospace",
                fontsize=15,
                title="Daily Spending Chart",
                dpi=150,
                ax=ax   ## <- Tell July to put the heatmap in that Axes
            )
            st.pyplot(fig)
            with st.expander("This Month Report "):
                fig2, ax2 = plt.subplots(figsize=(2,2))
                current_time = datetime.datetime.now()
                custom_cmap = mcolors.LinearSegmentedColormap.from_list("black", ["black", "green"])
                july.month_plot(dates, data['3'],cmap=custom_cmap,month=current_time.month,fontsize=4,
                                    value_label=True,ax=ax2)
                
                st.pyplot(fig2,use_container_width=True)         
                    
            fig2, ax2 = plt.subplots(figsize=(2,2))
            current_time = datetime.datetime.now()
            custom_cmap = mcolors.LinearSegmentedColormap.from_list("black", ["black", "green"])
            july.month_plot(dates, data['3'],cmap=custom_cmap,month=current_time.month,fontsize=4,
                                value_label=True,ax=ax2)
            
            st.pyplot(fig2,use_container_width=True)      

except AttributeError as e:
    print(e)
    st.error("login Session Expired")
    time.sleep(2)
    st.switch_page("app.py")
