import streamlit as st
import os
from Login import login_user
from Regist import register_user
from Home import home_page

def list_pages():
    # Daftar halaman di folder pages, hanya ditampilkan jika sudah login
    pages_dir = "masters"
    pages = [f.replace(".py", "") for f in os.listdir(pages_dir) if f.endswith(".py")]
    return pages

def main():
    # Cek login status
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        # Menampilkan homepage
        home_page()

        # Sidebar: Pilih View Master dengan selectbox
        page = st.sidebar.selectbox("Pilih Masters", ["None"] + list_pages())  # Default None, tidak langsung memilih halaman
        
        # Cek apakah pengguna memilih halaman
        if page != "None":
            # Halaman lain yang dipilih setelah login
            module = __import__(f"masters.{page}", fromlist=[page])
            module.main()  # Memanggil fungsi main() di setiap halaman
        else:
            st.write("🔎Silahkan Memilih halaman dari dropdown untuk melihat konten🔍")
            
    else:
        # Jika belum login, hanya tampilkan halaman Login dan Registrasi
        st.sidebar.image("assets/gl.png",caption="Welcome to GrandLucky's IT Dashboard")    
        page = st.sidebar.selectbox("Pilih Halaman", ("Login", "Registrasi"))
        if page == "Login":
            login_user()  # Tampilkan halaman login
        elif page == "Registrasi":
            register_user()  # Tampilkan halaman registrasi

if __name__ == "__main__":
    main()
