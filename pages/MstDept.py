import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from queries.queryMstDepartment import *

st.set_page_config(page_title="Departments", page_icon="🏢", layout="wide")
st.subheader("🏢Departments")

#fetch data
result=view_all_data_master_dept()
df=pd.DataFrame(result, columns=["Nou","Dept_id","Dept","date_update","user_update"])

#side bar
st.sidebar.image("assets/gl.png",caption="Welcome to GrandLucky's IT Dashboard")

#switcher
st.sidebar.header("Filters Options")
# dept_id=st.sidebar.multiselect(
#     "Which Department ID: ",
#     options=df["Dept_id"].unique(),
#     default=df["Dept_id"].unique(),
# )

updated_by=st.sidebar.multiselect(
    "Choose User: ",
    options=df["user_update"].unique(),
    default=df["user_update"].unique(),
)

dept=st.sidebar.multiselect(
    "Choose Department: ",
    options=df["Dept"].unique(),
    default=df["Dept"].unique(),
)

df_selection=df.query(
    "Dept==@dept & user_update==@updated_by"
)

# st.dataframe(df_selection,use_container_width=True)

# Pagination setup  
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