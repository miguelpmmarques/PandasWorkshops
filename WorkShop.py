#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px


# ## Importar Dados

# In[2]:


url = 'https://raw.githubusercontent.com/miguelpmmarques/PandasWorkshops/main/president_county_candidate.csv'
# Passa o CSV para um DataFrame
eleicoes = pd.read_csv(url)
print(eleicoes.info())



# In[3]:


url = 'https://raw.githubusercontent.com/miguelpmmarques/PandasWorkshops/main/president_state.csv'
states_votes = pd.read_csv(url)
# Aqui estamos a alterar o nome da coluna state so para
# nao causar confusoes mais para a frente
states_votes = states_votes.rename(columns ={"state":"state_name"})
print(states_votes.info())



# ## Group By - Agregações
# - sum 
# - mean
# - std
# - median
# - max
# - min
# 
# 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html

# In[4]:


# neste caso estamos a fazer uma agregacao da soma de modo a ter a 
# soma de votos e a soma de co
county_won = eleicoes.groupby(["state","candidate"]).sum().reset_index()
county_won


# # Join
# 
# 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html

# In[5]:


# set index define a key da outra base de dados
# on define a key da base de dados que estamos a dar join
joined_db = county_won.join(states_votes.set_index('state_name'), on='state',rsuffix='_total')
joined_db


# ## Calculo sobre colunas

# In[6]:


joined_db["Percentage_votes"] = np.round(joined_db["total_votes"]/joined_db["total_votes_total"]*100,2)


# In[24]:


# Alterar nomes de colunas
joined_db_v1 = joined_db.rename(columns={
    "total_votes":"State votes",
    "won":"County Won"
})
joined_db_v1


# In[25]:


# eliminar colunas
joined_db_v2 = joined_db_v1.drop(columns=["total_votes_total"])
joined_db_v2


# ## Selects e Wheres

# In[26]:


query1 = joined_db_v2["Percentage_votes"] > 60
query1


# In[10]:


joined_db_v2[query1][["state","candidate"]]


# In[27]:


trump_stats = joined_db_v2[(joined_db_v2["candidate"]=="Donald Trump")][["State votes","County Won","Percentage_votes"]]
# O describe mostra as estatisticas todas por colunas
trump_stats.describe()


# In[28]:


biden_stats = joined_db_v2[(joined_db_v2["candidate"]=="Joe Biden")][["State votes","County Won","Percentage_votes"]]
# O describe mostra as estatisticas todas por colunas
biden_stats.describe()


# In[30]:


q4 = joined_db_v2["candidate"] == "Joe Biden"
q3 = joined_db_v2["candidate"] == "Donald Trump"
joined_db_v3 = joined_db_v2[q3 | q4]
joined_db_v3


# In[14]:


fig = px.line(joined_db_v3, x="state",
              y="Percentage_votes",
              color="candidate",
             color_discrete_sequence=["red","blue"])
fig.show()


# In[15]:


joined_db_v3


# In[16]:


states_info = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
states_info = states_info[["code","state"]]
joined_db_v4 = joined_db_v3.join(states_info.set_index("state"),on="state")
joined_db_v4 = joined_db_v4[joined_db_v4["candidate"] == "Joe Biden"]


# In[23]:


import plotly.graph_objects as go

fig = go.Figure(data=go.Choropleth(
    locations=joined_db_v4['code'], # Spatial coordinates
    z = joined_db_v4['Percentage_votes'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Bluered_r',
    zmax = 100,
    zmin = 0,
    colorbar_title = "Percentage Votes For Biden",
))

fig.update_layout(
    title_text = '2020 US Election by State',
    geo_scope='usa', # limite map scope to USA
)

fig.show()

