import streamlit as st
import mysql.connector

#connection
conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="grandlucky"
)

c=conn.cursor()

#fetching
def view_all_outlets():
    c.execute("select * from outlet order by Outlet_id asc")
    data=c.fetchall()
    return data