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
def view_all_data_service_hw():
    c.execute("select * from service_hw order by Nou asc")
    data=c.fetchall()
    return data