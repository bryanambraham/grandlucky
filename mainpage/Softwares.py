import streamlit as st
import pandas as pd
from queries.querysoftwares import *

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


if __name__ == "__main__":
    main()