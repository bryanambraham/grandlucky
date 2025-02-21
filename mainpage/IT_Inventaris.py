import streamlit as st
import pandas as pd
import plotly.express as px
from queries.queryms_inv import *
from io import BytesIO

def main():
    st.subheader("IT Inventaris")

    # Fetching data
    result = view_all_data_ms_inv()
    df = pd.DataFrame(result, columns=["NOU", "Outlet", "Current_Outlet", "Nama_HW", "Merk", "Type", "Tgl_beli", "Lokasi", "User_HW", "IP_Address", "HW_Name", "SN", "Tgl_Destroy", "Date_Create", "User_Create", "Date_update", "User_update", "status", "Count"])

    # Filters
    st.sidebar.header("Filters Options")
    curr_outlet = st.sidebar.multiselect("Current Outlet: ", options=df["Current_Outlet"].unique(), default=df["Current_Outlet"].unique())
    nama_hw = st.sidebar.multiselect("Nama HW: ", options=df["Nama_HW"].unique(), default=df["Nama_HW"].unique())
    type = st.sidebar.multiselect("Type: ", options=df["Type"].unique(), default=df["Type"].unique())
    lokasi = st.sidebar.multiselect("Lokasi: ", options=df["Lokasi"].unique(), default=df["Lokasi"].unique())
    user_hw = st.sidebar.multiselect("User HW: ", options=df["User_HW"].unique(), default=df["User_HW"].unique())
    ip_address = st.sidebar.multiselect("IP Lists: ", options=df["IP_Address"].unique(), default=df["IP_Address"].unique())
    user_create = st.sidebar.multiselect("Created by: ", options=df["User_Create"].unique(), default=df["User_Create"].unique())
    user_update = st.sidebar.multiselect("Updated by: ", options=df["User_update"].unique(), default=df["User_update"].unique())
    status = st.sidebar.multiselect("Status: ", options=df["status"].unique(), default=df["status"].unique())

    # Apply filters
    df_selection = df.query(
        "Current_Outlet==@curr_outlet & Nama_HW==@nama_hw & Type==@type & Lokasi==@lokasi & User_HW==@user_hw & IP_Address==@ip_address & User_Create==@user_create & User_update==@user_update & status==@status"
    )

    # Create a simple bar chart for visual representation
    chart_data = df_selection.groupby('Type').size().reset_index(name='Count')
    fig = px.bar(chart_data, x='Type', y='Count', title='Hardware Type Distribution')
    st.plotly_chart(fig, use_container_width=True)

    # Summary statistics under the chart
    total_items = df_selection.shape[0]
    summary_text = f"**Total Devices Filtered**: {total_items} devices matching the applied filters."

    # You can add more detailed stats, for example:
    avg_count_per_type = chart_data['Count'].mean()
    max_count_per_type = chart_data['Count'].max()
    min_count_per_type = chart_data['Count'].min()

    summary_text += f"\n\n**Average count per type**: {avg_count_per_type:.2f}\n"
    summary_text += f"**Max count for a type**: {max_count_per_type}\n"
    summary_text += f"**Min count for a type**: {min_count_per_type}"

    # Display the summary
    st.markdown(summary_text)

    # Pagination for the table
    page_size = st.selectbox("Rows per page", [10, 20, 30, 50, 100], index=2, key="rows_itinvent")  # Default 30
    total_pages = (len(df_selection) // page_size) + (1 if len(df_selection) % page_size > 0 else 0)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    # Display the selected page of data
    start_row = (st.session_state.page_number - 1) * page_size
    end_row = start_row + page_size
    st.dataframe(df_selection.iloc[start_row:end_row], use_container_width=True)

    # Pagination buttons
    col1, col2, col3 = st.columns([7, 7, 2])
    with col1:
        if st.button("Previous", key="previous_button_itinvent") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.button("Next", key="next_button_itinvent") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

    # Show data range
    st.write(f"Showing {start_row + 1}-{min(end_row, len(df_selection))} of {len(df_selection)}")

    # Export to Excel
    if st.button("Export to Excel", key="export_excel_itinvent"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_selection.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="IT_Inventaris.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
