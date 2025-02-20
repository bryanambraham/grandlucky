import streamlit as st
import pandas as pd
from queries.querystockmovement import *

def main():
    st.subheader("Stock Movement")
    result = view_all_data_stock_movement()
    df=pd.DataFrame(result,columns=["NOU","Kode_stock","Desc","QTY","Lokasi","dept","Mode","Date","user_update"])

    st.sidebar.header("Filters Options")
    dept=st.sidebar.multiselect(
        "Department: ",
        options=df["dept"].unique(),
        default=df["dept"].unique(),
    )

    lokasi=st.sidebar.multiselect(
        "Lokasi: ",
        options=df["Lokasi"].unique(),
        default=df["Lokasi"].unique(),
    )

    kode_stock=st.sidebar.multiselect(
        "Kode Stok: ",
        options=df["Kode_stock"].unique(),
        default=df["Kode_stock"].unique(),
    )

    df_selection = df.query(
        "dept==@dept & Lokasi==@lokasi & Kode_stock==@kode_stock"
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
