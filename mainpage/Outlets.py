import streamlit as st
import pandas as pd
from queries.queryoutlets import *

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

if __name__ == "__main__":
    main()