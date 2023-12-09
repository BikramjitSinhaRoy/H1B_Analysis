from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
alt.data_transformers.enable("vegafusion")


#####  Cache ####

# @st.cache_data
# def load_data(csv):
#     df = pd.read_csv(csv)
#     return df
# df = load_data("<path to csv>")
# st.dataframe(df)

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

st.title('Analysing H1B Data')
st.markdown('''
            ### Top Cities
            ''')

st.sidebar.header('Top cities based on number of applications')
number_of_cities = st.sidebar.slider("Number of Cities",min_value=1,max_value=20,value=5, step=1)

city_count = h1b.groupby(['WORKSITE_CITY'])['CASE_NUMBER'].count().reset_index(name='count')
top_city_count = city_count.sort_values('count', ascending=False).head(number_of_cities)
bar2 = alt.Chart(top_city_count).mark_bar().encode(
alt.X('count', title='Number of Applications'),
alt.Y('WORKSITE_CITY', sort='-x', title='City'))
st.altair_chart(bar2, use_container_width=True)