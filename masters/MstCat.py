import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from queries.queryMstCat import *
from io import BytesIO

# st.set_page_config(page_title="Categories", page_icon="🏢", layout="wide")

def main():
    st.subheader("🎮Master Category")
    st.markdown("##")

    #fetch data
    result=view_all_data_master_categoryhw()
    df=pd.DataFrame(result, columns=["NOU","Category_Name", "Date_Updated", "Updated_By"])

    # buat nampilin df nya
    # st.dataframe(df)

    #switcher
    st.sidebar.header("Filters Options")
    category=st.sidebar.multiselect(
        "Category Name: ",
        options=df["Category_Name"].unique(),
        default=df["Category_Name"].unique(),
    )

    date=st.sidebar.multiselect(
        "Latest Update Date: ",
        options=df["Date_Updated"].unique(),
        default=df["Date_Updated"].unique(),
    )

    user=st.sidebar.multiselect(
        "Latest Update by: ",
        options=df["Updated_By"].unique(),
        default=df["Updated_By"].unique(),
    )

    df_selection=df.query(
        "Category_Name==@category & Date_Updated==@date & Updated_By==@user"
    )

    # Dropdown for selecting rows per page
    page_size = st.selectbox("Rows per page", [10, 20, 30, 50, 100], index=2,key="rows_mstcat")  # Default 30
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
        if st.button("Previous",key="previous_button_mstcat") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.button("Next",key="next_button_mstcat") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

    # Show data range
    st.write(f"Showing {start_row + 1}-{min(end_row, len(df_selection))} of {len(df_selection)}")
            # Export to Excel
    if st.button("Export ke Excel",key="export_excel_mstcat"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="MasterCategory.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
if __name__ == "__main__":
    main()