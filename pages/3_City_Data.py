from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
alt.data_transformers.enable("vegafusion")

@st.cache_data
def load_data():
    path = r'data'  # or unix / linux / mac path

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


#getting states in a list

user_state = st.selectbox('Select a State', sorted(h1b['state_name'].unique().tolist()))

# TOP CITIES
h1b.loc[h1b.WORKSITE_STATE == 'DC', 'WORKSITE_CITY'] = "Washington"
# give this list as option to choose to the user
# user selects one of the states from the list
# search cities based on the USER_STATE variable

top_cities = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['WORKSITE_CITY'])['CASE_STATUS'].count().reset_index(name='count')
top_cities_count = top_cities.sort_values('count', ascending=False).head(10)

st.subheader("Top 5 Cities")
city_bar = alt.Chart(top_cities_count).mark_bar().encode(
alt.X('count', title='Number of Applications'),
alt.Y('WORKSITE_CITY', sort='-x', title='City'))

st.altair_chart(city_bar, use_container_width=True)