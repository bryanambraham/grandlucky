import streamlit as st
import pandas as pd
from queries.querysoftwares import *
from io import BytesIO

def main():
    st.subheader("Softwares & Hardware Lists")

    result = view_all_data_softwares()
    df=pd.DataFrame(result,columns=["Nou","SW_Name","Link_Dwld","date_update","user_update"])

    st.sidebar.header("Filter Options")
    sw_name = st.sidebar.multiselect(
        "Software Name: ",
        options=df["SW_Name"].unique(),
        default=df["SW_Name"].unique(),
    )

    df_selection=df.query(
        "SW_Name==@sw_name"
    )

    st.dataframe(df_selection)

            # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="Softwares.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()