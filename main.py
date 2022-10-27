import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
connexion = sqlite3.connect("../database/bce.db")
cursor = connexion.cursor()

# define query executor function
def run_query(query):
    cursor.execute(query)
    return cursor.fetchall()

# creating dataframe for entreprise table TODO delete
cursor.execute("""
Select *
FROM enterprise
""")
enterprise = cursor.fetchall()
col = [description[0] for description in cursor.description]

df_enterprise = pd.DataFrame.from_records(data=enterprise, columns=col)


# Getting insights
# general info
# nbr of entitys in Belgium
rows = run_query('''
    select 'Branch' as Type,  COUNT(Id) as Nbr
    from branch
    union
    select 'Establishment', COUNT(EstablishmentNumber)
    from establishment
    union
    select 'Enterprise', count(EnterpriseNumber)
    from enterprise
    order by Nbr desc
   ''')
cols = ['entity_type', 'nbr']
df_entity_type_count = pd.DataFrame(rows, columns=cols)
# plotting bar chart for types of entities
fig_entities, ax = plt.subplots(figsize =(8, 2))
 
# creating the bar plot
ax.barh(df_entity_type_count['entity_type'], df_entity_type_count['nbr'], data=df_entity_type_count, height=0.4)

# reoder from highest to lowest
ax.invert_yaxis()

# after plotting the data, format the labels in thousands
current_values = plt.gca().get_xticks() / 1000
# using format string '{:.0f}' here but you can choose others
plt.gca().set_xticklabels([f'{x:,}' for x in current_values])

# Add x, y gridlines
ax.grid(b = True, color ='black',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2, axis='x')

ax.set_xlabel("Number of entities (thousands)")
ax.set_title("Number of different entities in Belgium", loc='left')

# 1.

# 2. Which percentage of the companies are under which Status?


# 3. Which percentage of the companies are which type of entreprise?
rows = run_query('''
    select count(enterprise.EnterpriseNumber), TypeOfEnterprise.Description
    from enterprise
    left join (Select Code, Description
	from code
	where code.Category = "TypeOfEnterprise" AND code."Language"="FR")  TypeOfEnterprise
    on enterprise.TypeOfEnterprise = TypeOfEnterprise.Code
    group by TypeOfEnterprise.Description
    ''')
cols = ['enterprise_count', 'type_desc']
df_entreprise_type_count = pd.DataFrame(rows, columns=cols)
df_entreprise_type_count['percent'] = df_entreprise_type_count['enterprise_count'] / df_entreprise_type_count['enterprise_count'].sum() * 100

# ploting % enterprise type
fig_enterprise_type, ax = plt.subplots(figsize=(6, 3))
ax.pie(df_entreprise_type_count['percent'], labels=df_entreprise_type_count['type_desc'],
autopct='%1.1f%%')
ax.axis('equal') 

# dashboarding
title_container = st.container()
title_container.title('My awesome dashboard')

gen_info_container = st.container()
gen_info_container.subheader("General information")
gen_info_container.pyplot(fig_entities)

entity_type_container = st.container()
entity_type_container.subheader("Enterprise types")
entity_type_container.pyplot(fig_enterprise_type)
#st.subheader('Which percentage of the companies are under which Status?')
#st.metric("% Enterprises with Active Status", status_percent['AC'], delta=None, delta_color="normal", help=None)
