import streamlit as st
import os
from mainpage import *

st.set_page_config(page_title="Grandlucky Dashboard by Bryan🏢")

def list_pages():
    # Daftar halaman di folder pages, hanya ditampilkan jika sudah login
    pages_dir = "mainpage"
    pages = [f.replace(".py", "") for f in os.listdir(pages_dir) if f.endswith(".py")]
    return pages

def home_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Anda harus login terlebih dahulu.")
        st.button("Kembali ke Login", on_click=lambda: st.session_state.update(logged_in=False))
    else:
        st.header(f'Selamat datang, {st.session_state["username"]}! 👋')
        st.write(f'Level: {st.session_state.get("userlevel")}')
        #side bar
        st.sidebar.image("assets/gl.png",caption="Welcome to GrandLucky's IT Dashboard")        
        # Sidebar: Pilih MainPage dengan selectbox
        page = st.sidebar.selectbox("Pilih Main Page", ["None"] + list_pages())  # Default None, tidak langsung memilih halaman
                
        # Cek apakah pengguna memilih halaman
        if page != "None":
            # Halaman lain yang dipilih setelah login
            module = __import__(f"mainpage.{page}", fromlist=[page])
            module.main()  # Memanggil fungsi main() di setiap halaman
        else:
            st.write("")