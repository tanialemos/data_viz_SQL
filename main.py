import sqlite3
import os
import pandas as pd
import streamlit as st
connexion = sqlite3.connect("../database/bce.db")
cursor = connexion.cursor()

def run_query(query):
    cursor.execute(query)
    return cursor.fetchall()

rows = run_query('''
    SELECT JuridicalSituation, count(EnterpriseNumber) as nbr
    from enterprise
    group by JuridicalSituation;
    ''')

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")