import streamlit as st
import pandas as pd
from queries.queryservicehw import *

def main():
    st.subheader("Service Hardware")
    result = view_all_data_service_hw()
    df=pd.DataFrame(result,columns=["Tgl_perbaikan","Desc_kerusakan","Tgl_selesai","Vendor_Name","Date_Create","User_Create","Date_update","User_update","Count","Nou","SN","Current_Outlet", "Nama_HW", "Merk", "Type", "Lokasi", "User_HW"])

    st.sidebar.header("Filters Options")
    curr_outlet=st.sidebar.multiselect(
        "Current Outlet: ",
        options=df["Current_Outlet"].unique(),
        default=df["Current_Outlet"].unique(),
    )

    user_hw=st.sidebar.multiselect(
        "User: ",
        options=df["User_HW"].unique(),
        default=df["User_HW"].unique(),
    )

    lokasi=st.sidebar.multiselect(
        "Lokasi: ",
        options=df["Lokasi"].unique(),
        default=df["Lokasi"].unique(),
    )


    df_selection = df.query(
        "Current_Outlet==@curr_outlet & User_HW==@user_hw & Lokasi==@lokasi"
    )

    # st.dataframe(df_selection,use_container_width=True)

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

