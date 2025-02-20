import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from queries.queryMstMerk import *
from io import BytesIO

# st.set_page_config(page_title="Departments", page_icon="🏢", layout="wide")
def main():
    st.subheader("🌐Brands")

    #fetch data
    result=view_all_data_master_merk()
    df=pd.DataFrame(result, columns=["NOU1","Merk_Id","Merk","date_update","user_update"])

    st.sidebar.header('Filters Options')

    merk_id=st.sidebar.multiselect(
        "Choose ID: ",
        options=df["Merk_Id"].unique(),
        default=df["Merk_Id"].unique(),
    )

    merk=st.sidebar.multiselect(
        "Choose Merk: ",
        options=df["Merk"].unique(),
        default=df["Merk"].unique(),
    )

    df_selection=df.query(
        "Merk==@merk & Merk_Id==@merk_id"
    )

    st.dataframe(df_selection,use_container_width=True)

            # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="IT_Inventaris.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
                # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="MasterMerk.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()