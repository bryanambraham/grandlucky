import streamlit as st
import mysql.connector
import hashlib

def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="",
        db="grandlucky"
    )
    return conn

def login_user():
    st.subheader("Login Pengguna")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if username and password:
            conn = connect_to_db()
            cursor = conn.cursor()
            
            query = "SELECT * FROM master_user WHERE UserName = %s AND pass = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["userlevel"] = user[3]
                st.success("Login berhasil! Selamat datang.")
                st.experimental_rerun()  # Memuat ulang aplikasi dan langsung ke halaman Home
            else:
                st.error("Username atau Password salah.")
        else:
            st.error("Mohon masukkan semua data!")

def main():
    login_user()

if __name__ == "__main__":
    main()
