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
def view_all_data_softwares():
    c.execute("select * from `sw&hw` order by Nou asc")
    data=c.fetchall()
    return data