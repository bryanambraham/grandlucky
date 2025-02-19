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
def view_all_data_ms_inv():
    c.execute("select * from ms_inv order by NOU asc limit 100")
    data=c.fetchall()
    return data