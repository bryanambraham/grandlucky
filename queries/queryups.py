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
def view_all_data_ups():
    c.execute("select * from ups_mtc_log order by Nou asc")
    data=c.fetchall()
    return data