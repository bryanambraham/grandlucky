import streamlit as st
import pandas as pd
import mysql.connector
import os
from io import BytesIO

# Koneksi ke database
def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",  # Ganti dengan username kamu
        passwd="",  # Ganti dengan password kamu
        db="grandlucky"
    )
    return conn

# Fungsi untuk mengimpor file Excel
def load_excel_file():
    uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        return df
    return None

# Fungsi untuk membuat tabel baru sesuai dengan nama halaman (nama tabel)
def create_table_in_db(df, table_name):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Membuat tabel baru sesuai dengan nama halaman
    columns = ', '.join([f"`{col}` VARCHAR(255)" for col in df.columns])

    # Query untuk membuat tabel baru
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    );
    """
    
    cursor.execute(create_table_query)

    # Menangani nilai NaN dengan mengganti menjadi None (NULL dalam database)
    df = df.where(pd.notnull(df), None)

    # Menambahkan data ke tabel yang baru dibuat
    for i, row in df.iterrows():
        insert_query = f"INSERT INTO `{table_name}` ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

    st.success(f"Tabel '{table_name}' telah berhasil dibuat dan data telah dimasukkan ke dalamnya!")

# Fungsi untuk membuat halaman baru di folder mainpage
def create_page_in_mainpage(df, table_name):
    # Membuat folder 'mainpage' jika belum ada
    folder_path = "mainpage"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Menyiapkan nama file baru dengan format .py sesuai dengan nama tabel
    file_path = os.path.join(folder_path, f"{table_name}.py")
    
    # Menulis kode untuk halaman baru ke file .py
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""
import streamlit as st
import pandas as pd
import mysql.connector

# Koneksi ke database
def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",  # Ganti dengan username kamu
        passwd="",  # Ganti dengan password kamu
        db="grandlucky"
    )
    return conn

# Fungsi untuk menampilkan data dari tabel di database
def display_data_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Query untuk mengambil data dari tabel yang baru dibuat
    cursor.execute(f"SELECT * FROM `{table_name}`")
    data = cursor.fetchall()

    # Menampilkan data sebagai DataFrame
    columns = [desc[0] for desc in cursor.description]  # Mendapatkan nama kolom
    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    # Sidebar filter options
    st.sidebar.header("Filters Options")
    selected_filters = {}

    # Looping setiap kolom untuk menambahkan filter
    for col in df.columns:
        selected_filters[col] = st.sidebar.multiselect(
            f"{col}:",
            options=df[col].unique(),
            default=df[col].unique()  # Retain the selected filters if exists
        )

    # Filter data berdasarkan pilihan di sidebar
    filtered_df = df
    for col in selected_filters:
        if selected_filters[col]:  # Hanya melakukan filter jika ada pilihan
            filtered_df = filtered_df[filtered_df[col].isin(selected_filters[col])]

    # Menampilkan data yang difilter
    st.title(f"Data dari Tabel {table_name}")
    st.dataframe(filtered_df)

# Fungsi utama untuk menampilkan data di halaman dinamis
def main():
    display_data_from_db()

if __name__ == "__main__":
    main()
        """)
    st.success(f"Halaman baru '{table_name}.py' telah berhasil dibuat di folder '{folder_path}'!")

# Fungsi utama aplikasi
def main():
    st.title("Upload Data Excel dan Buat Tabel Baru di Database")

    # Input untuk nama halaman/tabel baru
    page_name = st.text_input("Masukkan Nama Halaman Baru (Nama Tabel):")
    
    if page_name:
        # Memuat file Excel
        df = load_excel_file()

        if df is not None:
            # Menampilkan DataFrame yang diimpor
            st.write("Data yang diimpor:")
            st.dataframe(df)

            # Membuat tabel baru di database dan menyimpan data
            if st.button("Buat Tabel Baru dan Simpan Data ke Database"):
                create_table_in_db(df, page_name)
                create_page_in_mainpage(df, page_name)

            # Menampilkan data dari tabel baru setelah data disimpan
            if st.button(f"Tampilkan Data dari Tabel {page_name}"):
                display_data_from_db(page_name)

        else:
            st.warning("Silakan unggah file Excel.")
    else:
        st.warning("Masukkan nama halaman untuk membuat tabel baru.")

if __name__ == "__main__":
    main()
