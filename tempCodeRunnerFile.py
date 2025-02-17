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