import streamlit as st
import pandas as pd
from queries.queryMstStock  import *
from io import BytesIO

def main():
    st.subheader("📋Stocks")

    #fetching data
    result = view_all_data_master_stok()
    df = pd.DataFrame(result, columns=["NOU","Kode_stock","Desc","QTY","Date_Update","user_update"])

    #filters
    #buat ngefilter kita mau cari berdasarkan kriterianya apa
    st.sidebar.header("Filters Options")
    kode_stock = st.sidebar.multiselect(
        "Kode Stok: ",
        options=df["Kode_stock"].unique(),
        default=df["Kode_stock"].unique(),
    )

    df_selection=df.query(
        "Kode_stock==@kode_stock"
    )

    #=============================#Buat filter kolum apa aja yang mau di tampilin dari tabel
    # showdata = st.multiselect('Choose Columns: ',df_selection.columns, default=[])
    # st.write(df_selection[showdata])
    #=============================#

    # Dropdown for selecting rows per page
    page_size = st.selectbox("Rows per page", [10, 20, 30, 50, 100], index=2, key="rows_mststock")  # Default 30
    total_pages = (len(df_selection) // page_size) + (1 if len(df_selection) % page_size > 0 else 0)

    # Page management
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    # Display the selected page of data
    start_row = (st.session_state.page_number - 1) * page_size
    end_row = start_row + page_size
    st.dataframe(df_selection.iloc[start_row:end_row], use_container_width=True)

    # Pagination buttons
    col1, col2, col3 = st.columns([7, 7, 2])
    with col1:
        if st.button("Previous",key="previous_button_mststock") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.button("Next",key="next_button_mststock") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

    # Show data range
    st.write(f"Showing {start_row + 1}-{min(end_row, len(df_selection))} of {len(df_selection)}")

            # Export to Excel
    if st.button("Export ke Excel",key="mststock"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="MasterStock.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()