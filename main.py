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
fig_entities, ax = plt.subplots(figsize =(8, 3))
ax.barh(df_entity_type_count['entity_type'], df_entity_type_count['nbr'], data=df_entity_type_count, height=0.4)
ax.invert_yaxis()

current_values = plt.gca().get_xticks() / 1000
plt.gca().set_xticklabels([f'{x:,}' for x in current_values])

ax.grid(b = True, color ='black',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2, axis='x')

ax.set_xlabel("Number of entities (thousands)")
ax.set_title("Number of different entities", loc='left')

# 1.

# 2. Which percentage of the companies are under which Status?
rows = run_query('''
    select count(EnterpriseNumber) as nbr_entreprises, Status 
    from enterprise 
    group by Status
   ''')
cols = ['nbr_enterprises', 'status']
df_status = pd.DataFrame(rows, columns=cols)
df_status['percent'] = df_status['nbr_enterprises'] / df_status['nbr_enterprises'].sum() * 100

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
fig_enterprise_type, ax = plt.subplots(figsize =(2, 2))
ax.pie(df_entreprise_type_count['percent'], labels=df_entreprise_type_count['type_desc'],
autopct='%1.1f%%')
ax.axis('equal') 

# dashboarding
title_container = st.container()
title_container.title('BCE Open Data')

gen_info_container = st.container()
gen_info_container.subheader("General information")
gen_info_container.pyplot(fig_entities)

percent = str(df_status.at[0, 'percent']) + '%'
entity_status_container = st.container()
entity_status_container.subheader("Enterprise status")
entity_status_container.metric("Enterprises with Active Status", percent, delta=None, delta_color="normal", help=None)

entity_type_container = st.container()
entity_type_container.subheader("Enterprise types")
entity_type_container.pyplot(fig_enterprise_type)
