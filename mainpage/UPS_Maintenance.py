import streamlit as st
import pandas as pd
from queries.queryups import *
from io import BytesIO

def main():    
    st.subheader("UPS Maintenance Log")
    result=view_all_data_ups()
    df=pd.DataFrame(result,columns=["Nou","Outlet","Type_UPS","Area_UPS","Jumlah_Battery","Last_Ganti_Batt","user_update","date_update","Dokumen_Pendukung","Status","Kapasitas_Batt"])

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


    