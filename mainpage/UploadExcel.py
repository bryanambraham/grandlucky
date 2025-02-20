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

# Fungsi untuk menampilkan data dari tabel di database
def display_data_from_db(table_name):
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
            default=df[col].unique()
        )

    # Filter data berdasarkan pilihan di sidebar
    # Perbaikan pada query string, kita memanfaatkan pandas 'loc'
    filtered_df = df
    for col in selected_filters:
        if selected_filters[col]:  # Hanya melakukan filter jika ada pilihan
            filtered_df = filtered_df[filtered_df[col].isin(selected_filters[col])]

    # Pagination setup
    page_size = 15
    total_pages = (len(filtered_df) // page_size) + (1 if len(filtered_df) % page_size > 0 else 0)

    # Page management
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    # Display the selected page of data
    start_row = (st.session_state.page_number - 1) * page_size
    end_row = start_row + page_size
    st.dataframe(filtered_df.iloc[start_row:end_row], use_container_width=True)

    # Pagination buttons
    col1, col2, col3 = st.columns([7, 7, 2])
    with col1:
        if st.button("Previous") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.button("Next") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

    # Show data range
    st.write(f"Showing {start_row + 1}-{min(end_row, len(filtered_df))} of {len(filtered_df)}")

    # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            filtered_df.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name=f"{table_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Fungsi utama
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

            # Menampilkan data dari tabel baru setelah data disimpan
            if st.button(f"Tampilkan Data dari Tabel {page_name}"):
                display_data_from_db(page_name)

        else:
            st.warning("Silakan unggah file Excel.")
    else:
        st.warning("Masukkan nama halaman untuk membuat tabel baru.")

if __name__ == "__main__":
    main()
