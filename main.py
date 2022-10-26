import sqlite3
import os
import pandas as pd
import streamlit as st
connexion = sqlite3.connect("../database/bce.db")
cursor = connexion.cursor()

# creating dataframe for entreprise table
cursor.execute("""
Select *
FROM enterprise
""")
enterprise = cursor.fetchall()
col = [description[0] for description in cursor.description]

df_enterprise = pd.DataFrame.from_records(data=enterprise, columns=col)


# getting insights
# general info
nbr_of_enterprises = df_enterprise.shape[0]

# 1.

# 2. Which percentage of the companies are under which Status?
groupby = df_enterprise.groupby(['Status']).count()
status_percent = groupby['EnterpriseNumber'] / nbr_of_enterprises * 100

# dashboarding
st.title('My awesome dashboard')
st.header('Answering questions')
st.subheader('Which percentage of the companies are under which Status?')
st.metric("% Enterprises with Active Status", status_percent['AC'], delta=None, delta_color="normal", help=None)


'''
# define query executor function
def run_query(query):
    cursor.execute(query)
    return cursor.fetchall()

rows = run_query(
    #SELECT JuridicalSituation, count(EnterpriseNumber) as nbr
    #from enterprise
    #group by JuridicalSituation;
   )

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
'''