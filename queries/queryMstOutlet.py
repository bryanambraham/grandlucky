import mysql.connector
import streamlit as st

#connection
conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="grandlucky"
)

c=conn.cursor()

#fetch data
def view_all_data_master_outlet():
    c.execute("select * from master_outlet order by Outlet_id asc")
    data=c.fetchall()
    return data