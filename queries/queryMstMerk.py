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
def view_all_data_master_merk():
    c.execute("select * from master_merk order by NOU1 asc")
    data=c.fetchall()
    return data