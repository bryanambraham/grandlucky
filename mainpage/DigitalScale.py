import streamlit as st
import pandas as pd
from queries.querydigitalscale import *

def main():
    st.subheader("Digital Scale Log")
    result = view_digitalscale()
    df=pd.DataFrame(result,columns=["nou","outlet","merk","Type","scale_area","SN","tglbeli","tgltera","dokument_tera","status","dateupdate","userupdate"])

    st.sidebar.header("Filters Options")
    outlet=st.sidebar.multiselect(
        "Outlet: ",
        options=df["outlet"].unique(),
        default=df["outlet"].unique(),
    )

    merk=st.sidebar.multiselect(
        "Merk: ",
        options=df["merk"].unique(),
        default=df["merk"].unique(),
    )

    merk_type=st.sidebar.multiselect(
        "Type: ",
        options=df["Type"].unique(),
        default=df["Type"].unique(),
    )

    scale_area=st.sidebar.multiselect(
        "Scale Area: ",
        options=df["scale_area"].unique(),
        default=df["scale_area"].unique(),
    )

    sn=st.sidebar.multiselect(
        "Serial Number: ",
        options=df["SN"].unique(),
        default=df["SN"].unique(),
    )

    tgltera=st.sidebar.multiselect(
        "Tanggal Tera: ",
        options=df["tgltera"].unique(),
        default=df['tgltera'].unique(),
    )

    status=st.sidebar.multiselect(
        "Status: ",
        options=df["status"].unique(),
        default=df["status"].unique(),
    )

    df_selection = df.query(
        "outlet==@outlet & merk==@merk & Type==@merk_type & scale_area==@scale_area & SN==@sn & tgltera==@tgltera & status==@status"
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
