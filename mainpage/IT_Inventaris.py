import streamlit as st
import pandas as pd
from queries.queryms_inv import *

def main():
    st.subheader("IT Inventaris")

    #fetching data
    result = view_all_data_ms_inv()
    df = pd.DataFrame(result, columns=["NOU","Outlet","Current_Outlet","Nama_HW","Merk","Type","Tgl_beli","Lokasi","User_HW","IP_Address","HW_Name","SN","Tgl_Destroy","Date_Create","User_Create","Date_update","User_update","status","Count"])

    #filters
    #buat ngefilter kita mau cari berdasarkan kriterianya apa
    st.sidebar.header("Filters Options")
    curr_outlet = st.sidebar.multiselect(
        "CUrrent Outlet: ",
        options=df["Current_Outlet"].unique(),
        default=df["Current_Outlet"].unique(),
    )

    nama_hw = st.sidebar.multiselect(
        "Nama HW: ",
        options=df["Nama_HW"].unique(),
        default=df["Nama_HW"].unique(),
    )

    type = st.sidebar.multiselect(
        "Type: ",
        options=df["Type"].unique(),
        default=df["Type"].unique(),
    )

    lokasi = st.sidebar.multiselect(
        "Lokasi: ",
        options=df["Lokasi"].unique(),
        default=df["Lokasi"].unique(),
    )

    user_hw = st.sidebar.multiselect(
        "User HW: ",
        options=df["User_HW"].unique(),
        default=df["User_HW"].unique(),
    )

    ip_address = st.sidebar.multiselect(
        "IP Lists: ",
        options=df["IP_Address"].unique(),
        default=df["IP_Address"].unique(),
    )

    user_create = st.sidebar.multiselect(
        "Created by: ",
        options=df["User_Create"].unique(),
        default=df["User_Create"].unique(),
    )

    user_update = st.sidebar.multiselect(
        "Updated by: ",
        options=df["User_update"].unique(),
        default=df["User_update"].unique(),
    )

    status = st.sidebar.multiselect(
        "Status: ",
        options=df["status"].unique(),
        default=df["status"].unique(),
    )

    df_selection=df.query(
        "Current_Outlet==@curr_outlet & Nama_HW==@nama_hw & Type==@type & Lokasi==@lokasi & User_HW==@user_hw & IP_Address==@ip_address & User_Create==@user_create & User_update==@user_update & status==@status"
    )

    #=============================#Buat filter kolum apa aja yang mau di tampilin dari tabel
    # showdata = st.multiselect('Choose Columns: ',df_selection.columns, default=[])
    # st.write(df_selection[showdata])
    #=============================#
    #setup pagination
    page_size = 15
    total_pages = (len(df_selection) // page_size) + (1 if len(df_selection) % page_size > 0 else 0)

    # Page management  
    if 'page_number' not in st.session_state:  
        st.session_state.page_number = 1  

    # Display the selected page of data  
    start_row = (st.session_state.page_number - 1) * page_size  
    end_row = start_row + page_size  
    st.dataframe(df_selection.iloc[start_row:end_row],use_container_width=True)  

    # Pagination buttons  
    col1, col2, col3 = st.columns([7, 7, 2])  
    with col1:  
        if st.button("Previous") and st.session_state.page_number > 1:  
            st.session_state.page_number -= 1  
    with col2:  
        st.write(f"Page {st.session_state.page_number} of {total_pages}", )  
    with col3:  
        if st.button("Next") and st.session_state.page_number < total_pages:  
            st.session_state.page_number += 1  

    # Show data range  
    st.write(f"Showing {start_row + 1}-{min(end_row, len(df_selection))} of {len(df_selection)}")  

if __name__ == "__main__":
    main()