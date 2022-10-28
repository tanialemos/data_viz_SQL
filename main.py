import datetime
import sqlite3
from turtle import width
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np
#from PIL import Image
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
fig_entities, ax = plt.subplots(figsize =(7, 3))
ax.barh(df_entity_type_count['entity_type'], df_entity_type_count['nbr'], 
data=df_entity_type_count, height=0.4)
ax.invert_yaxis()

current_values = plt.gca().get_xticks() / 1000
plt.gca().set_xticklabels([f'{x:,}' for x in current_values])

ax.grid(b = True, color ='black',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2, axis='x')

ax.set_xlabel("Number of entities (thousands)")
ax.set_title("Number of different entities", loc='left')

# 1. Which percentage of the companies are under which juridical form?
rows = run_query('''
    SELECT Category
    from code
    Group by Category
   ''')
col = [description[0] for description in cursor.description]
code = pd.DataFrame.from_records(data=rows, columns=col)
category = list(code['Category'].T)

code_tbls = {}
for table_name in category:
    rows = run_query(
        f"""
            Select  Code, Description
            from code
            where code.Category = "{table_name}" AND code."Language"="FR";
            """
    )
    col = [description[0] for description in cursor.description]
    code_tbls[table_name] = pd.DataFrame.from_records(data=rows, columns=col)

rows = run_query('''
    Select *
    FROM enterprise
   ''')
col = [description[0] for description in cursor.description]
enterprise = pd.DataFrame.from_records(data=rows, columns=col)

dict_tbl = {}
list_key = [ 'JuridicalSituation', 'JuridicalForm', 'TypeOfEnterprise']

for key in list_key:
     dict_tbl[key] = code_tbls[key]

for tbls_name, tbls in dict_tbl.items():
    enterprise = enterprise.set_index(tbls_name).join(tbls.set_index('Code'), how='left')\
         .rename(columns={'Description' : tbls_name})

JurForm_repartition = (enterprise.groupby('JuridicalForm')['EnterpriseNumber']
                .count()
                .reset_index(name='nmb_JurForm') )

#repartition per category in %
JurForm_repartition['%']=JurForm_repartition['nmb_JurForm']/enterprise['EnterpriseNumber'].count()*100

JurForm_repartition = JurForm_repartition.sort_values(by=['%'],ascending=False ).head(20)
# creation of a list of names with the goal to see it distribution 
JuridicalForm_names = list(JurForm_repartition['JuridicalForm'].T)

#remove the other en create a separate frame
selection = ['Société privée à responsabilité limitée',
            'Société à responsabilité limitée',
            'Association sans but lucratif',
            'Société anonyme',
            'Association des copropriétaires',
            'Entité étrangère']

JurForm_repartition.loc[JurForm_repartition['JuridicalForm'].isin(selection),'cleaned_JuridicalForm']= JurForm_repartition['JuridicalForm']
JurForm_repartition.loc[~JurForm_repartition['JuridicalForm'].isin(selection),'cleaned_JuridicalForm']= 'other'

#select only values that is = other
Fig_JuridicalForm_others = JurForm_repartition.loc[JurForm_repartition['cleaned_JuridicalForm']=='other']

# fig of values per juridiction
Fig_JuridicalForm = JurForm_repartition.groupby('cleaned_JuridicalForm')['%'].sum().reset_index(name=('%'))

# Plot juridical form
fig_jurical_form, ax = plt.subplots(figsize =(2, 2))
ax.pie(Fig_JuridicalForm['%'], labels=Fig_JuridicalForm['cleaned_JuridicalForm'],
autopct='%1.1f%%')
ax.axis('equal')

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
width = 0.3
wedge_properties = {"width":width}

fig_enterprise_type, ax = plt.subplots(figsize =(2, 2))
ax.pie(df_entreprise_type_count['percent'], labels=df_entreprise_type_count['type_desc'],
autopct='%1.1f%%', wedgeprops=wedge_properties)
ax.axis('equal') 


# 4. What is the average company's age in each sector
#define the age of the company
def round_10(x):
    return np.ceil(x/10)*10

today_date = datetime.datetime.now().date()
enterprise['StartDate']= pd.to_datetime(enterprise['StartDate']).dt.date
enterprise['Age']= (today_date-enterprise['StartDate'])
enterprise['Age'] = (enterprise['Age'].dt.days/365).apply(np.ceil)
enterprise['Age_10'] = enterprise['Age'].apply(round_10)

rows = run_query('''
    SELECT EntityNumber, substr(NaceCode,1,2) Industry, NaceVersion, ActivityGroup, Classification
    FROM activity
    GROUP BY EntityNumber , Industry, NaceVersion, ActivityGroup, Classification
    ''')
col = [description[0] for description in cursor.description]
activity = pd.DataFrame.from_records(data=rows, columns=col)

a = enterprise
b = activity
inner_activity_entreprise = pd.merge(a,b,left_on='EnterpriseNumber', right_on='EntityNumber',how='left')

entreprise_activities = inner_activity_entreprise.sort_values(by=['EnterpriseNumber','Industry', 'ActivityGroup','Classification','NaceVersion'])\
.drop_duplicates(subset=['EnterpriseNumber','Industry','ActivityGroup', 'Classification'],keep="last")

map_2003 = pd.read_csv("mapping_sector_2003.csv")
map_2003['code_sector'] = map_2003['code_sector'].astype(str).str.zfill(2)
map_2003 = map_2003[['code_sector','letter_sector']]
map_2008 = pd.read_csv("mapping_sector_2008.csv")
map_2008['code_sector'] = map_2008['code_sector'].astype(str).str.zfill(2)
map_2008 = map_2008[['code_sector','letter_sector']]

a = entreprise_activities[entreprise_activities['NaceVersion']=='2008']
b = code_tbls['Nace2008']
c = map_2008

entreprise_activities = pd.merge(a,b,left_on='Industry', right_on='Code',how='left')\
                .merge(c,left_on='Industry', right_on='code_sector',how='left' )

entreprise_activities = entreprise_activities[['EnterpriseNumber','StartDate','JuridicalSituation','JuridicalForm','TypeOfEnterprise','Age','Age_10','NaceVersion','ActivityGroup','code_sector','Description', 'letter_sector']]

df = entreprise_activities[entreprise_activities['StartDate']!=pd.to_datetime('1800-01-01')]

median_age_sector = df.groupby(['letter_sector'])['Age'].mean().reset_index('letter_sector').sort_values('Age')

conversion_table_sector = median_age_sector.merge(code_tbls['Nace2008'],left_on='letter_sector', right_on='Code',how='left' ).sort_values('Code')
conversion_table_sector = conversion_table_sector[['Code','Description']]
conversion_table_sector['Description']=conversion_table_sector['Description'].str[12:]

# plot
fig_avg_age_sector, ax = plt.subplots(figsize =(7, 4))
ax.barh( median_age_sector['letter_sector'],median_age_sector['Age'], data=median_age_sector, height=0.4)
ax.invert_yaxis()

ax.grid(b = True, color ='black',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2, axis='x')

ax.set_xlabel("Average age (years)")
ax.set_ylabel('Sector')
ax.set_title("Average company age per sector", loc='left')

# 5. age per sector
ages_sectors = df.groupby(['letter_sector','Age_10'])['EnterpriseNumber'].count().unstack().reset_index().set_index('letter_sector')

s_sort = df.groupby('letter_sector')['EnterpriseNumber'].count().sort_values()
sector_age_rep = ages_sectors.reindex(index=s_sort.index ).reset_index()

#fig = sector_age_rep.plot(x='letter_sector', stacked=True, kind='barh')
#fig.legend(loc='right')
#image = Image.open('sector_ages.png.')

# dashboarding
title_container = st.container()
title_container.title('BCE Open Data')

gen_info_container = st.container()
gen_info_container.subheader("General information")
gen_info_container.pyplot(fig_entities)

entity_type_container = st.container()
entity_type_container.subheader("Enterprise juridical form")
entity_type_container.pyplot(fig_jurical_form)

percent = str(df_status.at[0, 'percent']) + '%'
entity_status_container = st.container()
entity_status_container.subheader("Enterprise status")
entity_status_container.metric("Enterprises with Active Status", percent, delta=None, delta_color="normal", help=None)

entity_type_container = st.container()
entity_type_container.subheader("Enterprise types")
entity_type_container.pyplot(fig_enterprise_type)

entity_type_container = st.container()
entity_type_container.subheader("Average company age per sector")
entity_type_container.pyplot(fig_avg_age_sector)
st.table(conversion_table_sector)

entity_type_container = st.container()
entity_type_container.subheader("Enterprise types")
entity_type_container.pyplot(fig_enterprise_type)

#entity_type_container = st.container()
#entity_type_container.subheader("Company age distribution per sector")
#entity_type_container.image(image, caption='Sector age distribution')
