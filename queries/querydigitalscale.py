import mysql.connector
import streamlit as st

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="grandlucky"
)

c=conn.cursor()

#fetching data
def view_digitalscale():
    c.execute("select * from digital_scale_log order by nou asc")
    data=c.fetchall()
    return data