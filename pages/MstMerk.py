import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from queries.queryMstMerk import *

st.set_page_config(page_title="Departments", page_icon="🏢", layout="wide")
st.subheader("🌐Brands")

#fetch data
result=view_all_data_master_merk()
df=pd.DataFrame(result, columns=["NOU1","Merk_Id","Merk","date_update","user_update"])

#side bar
st.sidebar.image("assets/gl.png",caption="Welcome to GrandLucky's IT Dashboard")

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