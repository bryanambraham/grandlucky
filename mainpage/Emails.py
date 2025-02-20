import streamlit as st
import pandas as pd
from queries.queryemails import *

def main():
    st.subheader("Digital Scale Log")
    result = view_all_data_emails()
    df=pd.DataFrame(result,columns=["NOU","Outlet","Nama","Email_Address","Password","id_dept","Dept","mailing_list","Email_Send_out","Internet","date_update","user_update"])

    st.sidebar.header("Filters Options")
    outlet=st.sidebar.multiselect(
        "Outlet: ",
        options=df["Outlet"].unique(),
        default=df["Outlet"].unique(),
    )

    nama=st.sidebar.multiselect(
        "Nama: ",
        options=df["Nama"].unique(),
        default=df["Nama"].unique(),
    )

    dept=st.sidebar.multiselect(
        "Dept: ",
        options=df["Dept"].unique(),
        default=df["Dept"].unique(),
    )

    mailing_list=st.sidebar.multiselect(
        "Mailing List: ",
        options=df["mailing_list"].unique(),
        default=df["mailing_list"].unique(),
    )

    internet=st.sidebar.multiselect(
        "Internet: ",
        options=df["Internet"].unique(),
        default=df["Internet"].unique(),
    )

    df_selection = df.query(
        "Outlet==@outlet & Nama==@nama & Dept==@dept & mailing_list==@mailing_list & Internet==@internet"
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

