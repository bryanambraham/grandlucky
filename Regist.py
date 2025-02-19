import streamlit as st
import hashlib
import mysql.connector
import bcrypt

def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="",
        db="grandlucky"
    )
    return conn

def register_user():
    st.subheader("Registrasi Pengguna Baru")
    
    user_id = st.text_input("UserID")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    user_level = st.number_input('User_LevelID', min_value=1, max_value=10, step=1)
    email = st.text_input("Email")
    activated = st.selectbox('Status', ['Y', 'N'])
    image = st.file_uploader("Upload Profile Image", type=['jpg', 'jpeg', 'png'])
    date = st.date_input("Date")
    user_update = st.text_input("User_update")
    if st.button("Registrasi"):
        if username and password and email:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM master_user WHERE UserName = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                st.error("Username sudah terdaftar. Silakan pilih username lain.")
            else:
                query = """
                    INSERT INTO master_user (UserID, UserName, pass, UserLevelID, Email, activated, image, date_update, user_update)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                image_data = None
                if image is not None:
                    image_data = image.read()
                
                cursor.execute(query, (user_id, username, password, user_level, email, activated, image_data))
                conn.commit()
                cursor.close()
                conn.close()
                
                st.success("Pendaftaran berhasil! Silakan login.")
                st.experimental_rerun()  # Arahkan ke halaman login setelah registrasi selesai
        else:
            st.error("Mohon masukkan semua data dengan benar!")

def main():
    register_user()

if __name__ == "__main__":
    main()
