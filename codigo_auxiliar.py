states_info = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
states_info = states_info[["code","state"]]



import plotly.graph_objects as go

fig = go.Figure(data=go.Choropleth(
    locations=joined_db_v4['code'], # Spatial coordinates
    z = (COLUNA A MOSTRAR).astype(float), # Data to be color-coded
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
