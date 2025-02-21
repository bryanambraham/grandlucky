import os
import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO
from queries.queryups import *

# Fungsi untuk menyimpan data baru ke database
def add_new_data(Nou, Outlet, Type_UPS, Area_UPS, Jumlah_Batteray, Kapasitas_Batt, Last_Ganti_Batt, Dokumen_Pendukung, Status, user_update, date_update):
    # Menyambungkan ke database MySQL
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="",
        db="grandlucky"
    )
    cursor = connection.cursor()

    # Menyusun query untuk insert data baru
    query = """
    INSERT INTO ups_mtc_log (Nou, Outlet, Type_UPS, Area_UPS, Jumlah_Batteray, Kapasitas_Batt, Last_Ganti_Batt, Dokumen_Pendukung, Status, user_update, date_update)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Eksekusi query dengan data dari form
    cursor.execute(query, (Nou, Outlet, Type_UPS, Area_UPS, Jumlah_Batteray, Kapasitas_Batt, Last_Ganti_Batt, Dokumen_Pendukung, Status, user_update, date_update))

    # Commit perubahan dan menutup koneksi
    connection.commit()
    cursor.close()
    connection.close()

# Fungsi utama aplikasi Streamlit
def main():
    # Pilihan untuk menambah data baru
    form_option = st.selectbox("Pilih aksi:", ["-- Pilih --", "Add New Data"])

    if form_option == "Add New Data":
        # Form untuk menambahkan data baru
        with st.form(key="add_data_form"):
            Nou = st.number_input("Nomor Urut", min_value=1)
            Outlet = st.text_input("Outlet")
            Type_UPS = st.text_input("Type UPS")
            Area_UPS = st.text_input("Area UPS")
            Jumlah_Batteray = st.number_input("Jumlah Battery", min_value=1, step=1)
            user_update = st.text_input("Created by")
            date_update = st.date_input("Date Created")
            Last_Ganti_Batt = st.date_input("Last Ganti Batt")
            Dokumen_Pendukung = st.file_uploader("Dokumen Pendukung", type="pdf")
            Status = st.selectbox("Status", ["1", "0"])
            Kapasitas_Batt = st.number_input("Kapasitas Battery (Volt/PCS)", min_value=1, step=1)

            submit_button = st.form_submit_button("Add")

            # Jika tombol submit ditekan, simpan data ke database
            if submit_button:
                # Handle file upload jika ada
                if Dokumen_Pendukung is not None:
                    file_path = os.path.join("pdf_files", Dokumen_Pendukung.name)
                    # Pastikan folder pdf_files ada
                    os.makedirs("pdf_files", exist_ok=True)
                    with open(file_path, "wb") as f:
                        f.write(Dokumen_Pendukung.getbuffer())
                    Dokumen_Pendukung = file_path  # Simpan path file
                else:
                    Dokumen_Pendukung = "NULL"  # Jika tidak ada file yang di-upload

                # Menambahkan data baru ke database
                add_new_data(Nou, Outlet, Type_UPS, Area_UPS, Jumlah_Batteray, Kapasitas_Batt, Last_Ganti_Batt, Dokumen_Pendukung, Status, user_update, date_update)

                st.success("Data berhasil ditambahkan!")

    # Tampilkan data yang sudah ada di database
    st.subheader("UPS Maintenance Log")
    result=view_all_data_ups()
    df=pd.DataFrame(result,columns=["Nou","Outlet","Type_UPS","Area_UPS","Jumlah_Batteray","Last_Ganti_Batt","user_update","date_update","Dokumen_Pendukung","Status","Kapasitas_Batt"])

    st.sidebar.header("Filters Options")
    outlet=st.sidebar.multiselect(
        "Outlet: ",
        options=df["Outlet"].unique(),
        default=df["Outlet"].unique(),
    )

    type_ups=st.sidebar.multiselect(
        "Type UPS: ",
        options=df["Type_UPS"].unique(),
        default=df["Type_UPS"].unique(),
    )

    area_ups=st.sidebar.multiselect(
        "Area UPS: ",
        options=df["Area_UPS"].unique(),
        default=df["Area_UPS"].unique(),
    )

    status=st.sidebar.multiselect(
        "Status: ",
        options=df["Status"].unique(),
        default=df["Status"].unique(),
    )

    df_selection = df.query(
        "Outlet==@outlet & Type_UPS==@type_ups & Area_UPS==@area_ups & Status==@status"
    )

    # Pagination setup
    page_size = st.selectbox("Rows per page", [10, 20, 30, 50, 100], index=2, key="rows_upsmaintenance")
    total_pages = (len(df_selection) // page_size) + (1 if len(df_selection) % page_size > 0 else 0)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    start_row = (st.session_state.page_number - 1) * page_size
    end_row = start_row + page_size
    st.dataframe(df_selection.iloc[start_row:end_row], use_container_width=True)

    # Pagination buttons
    col1, col2, col3 = st.columns([7, 7, 2])
    with col1:
        if st.button("Previous",key="previous_button_upsmain") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.button("Next",key="next_button_upsmain") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

    # Show data range
    st.write(f"Showing {start_row + 1}-{min(end_row, len(df_selection))} of {len(df_selection)}")

    # # Display 'Dokumen_Pendukung' column with clickable links for viewing PDFs
    # for index, row in df_selection.iterrows():
    #     doc_name = row["Dokumen_Pendukung"]
    #     if doc_name and doc_name != "NULL":
    #         # Path file PDF berdasarkan nama file yang ada di 'Dokumen_Pendukung'
    #         file_path = os.path.join("pdf_files", doc_name)  # Ganti dengan path yang sesuai di server

    #         # Cek apakah file ada di path tersebut
    #         if os.path.exists(file_path):
    #             st.markdown(f"### {doc_name}")
    #             st.components.v1.html(f'''
    #                 <embed src="file://{file_path}" width="700" height="500" type="application/pdf">
    #             ''', height=600)
    #         else:
    #             st.warning(f"File {doc_name} tidak ditemukan di server.")

    # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="UPS_Maintenance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
