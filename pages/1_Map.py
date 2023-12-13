import pandas as pd
import streamlit as st
import altair as alt
import folium
from streamlit_folium import st_folium
from branca.colormap import linear
from pathlib import Path

@st.cache_data
def load_data():
    path = r'data'

    # Get the files from the path provided in the OP
    files = Path(path).glob('*.csv')  # .rglob to get subdirectories

    dfs = list()
    for i, f in enumerate(files):
        data = pd.read_csv(f)
        data['file'] = f'File {i}'
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)
    return df

h1b= load_data()

st.header("Certified Cases per 10k people by State")


df = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['state_name', 'popullation'])['CASE_STATUS'].count().reset_index(name='count')
df['count_per_10k'] = ((df['count']/df['popullation'])*10000).round(0)

# MAP US STATES 

map = folium.Map(location=[39, -97.5],zoom_start=4, scrollWheelZoom = False, tiles='CartoDB positron')

colormap = linear.GnBu_09.scale(5,173)
colormap.caption = 'Certified per 10k population'
map.add_children(colormap)

choropleth = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df,
    columns=('state_name', 'count_per_10k'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
    fill_color='GnBu'

    )
choropleth.geojson.add_to(map)

df = df.set_index('state_name')
# state_name = 'North Carolina'
# st.write(df['state_name'] == state_name, 'count_per_10k')

for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['certified'] = 'Certified cases per 10k people: ' +str(df.loc[state_name, 'count_per_10k'] if state_name in list(df.index) else 'N/A')

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','certified'], labels=False)
)

st_map = st_folium(map,width= 700, height=450)

selected_state = ''
if st_map['last_active_drawing']:
    selected_state = st_map['last_active_drawing']['properties']['name']

state_count2 = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['state_name', 'popullation']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
state_count2['count_per_10k'] = ((state_count2['count']/state_count2['popullation'])*10000).round(0)
if selected_state:
    state_count2 = state_count2[state_count2['state_name']== selected_state]

col1, col2 = st.columns(2, gap="large")
with col1:
    total = state_count2['count'].sum()
    st.write(f"Certified Cases :red[{selected_state}]")
    st.subheader(total)
with col2:
    wage = state_count2['median_wage'].median()
    st.write(f"Median Wage :red[{selected_state}]")
    st.subheader(f"${wage}")

