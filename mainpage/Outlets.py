import streamlit as st
import pandas as pd
from queries.queryoutlets import *
from io import BytesIO

def main():
    st.subheader("Outlet's Lists: ")
    
    result=view_all_outlets()
    df=pd.DataFrame(result,columns=["Outlet_id","Outlet_name","date_update","user_update"])

    st.sidebar.header("Filter Options")
    outletid = st.sidebar.multiselect(
        "Outlet ID: ",
        options=df['Outlet_id'].unique(),
        default=df['Outlet_id'].unique(),
    )

    outletname = st.sidebar.multiselect(
        "Outlet Name: ",
        options=df['Outlet_name'].unique(),
        default=df['Outlet_name'].unique(),
    )

    df_selection = df.query(
        "Outlet_id==@outletid & Outlet_name==@outletname"
    )

    st.dataframe(df_selection, use_container_width=True)

            # Export to Excel
    if st.button("Export ke Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="Outlets.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()