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

number_of_states = st.slider("Number of States",min_value=1,max_value=51,value=10, step=1)


st.subheader('TOP STATES')
# TOP STATES

# top states based on Certified

state_count = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE','state_name', 'popullation'])['CASE_STATUS'].count().reset_index(name='count')
state_count['count_per_10k'] = ((state_count['count']/state_count['popullation'])*10000).round(0)
top_state_count = state_count.sort_values('count_per_10k', ascending=False).head(number_of_states)

state_bar = alt.Chart(top_state_count).mark_bar(color='orange').encode(
alt.X('count_per_10k', title='Number of Applications per 10k people'),
alt.Y('state_name', sort='-x', title='State'))

st.altair_chart(state_bar, use_container_width=True)

#getting states in a list

list_of_top_states = top_state_count['state_name'].tolist()

# displaying it in the sidebar

user_state = st.selectbox(
    'Select a State',
    (list_of_top_states))

# st.write('You selected:', user_state)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.write(":red[Total Number of Employers]")
    top_emp2 = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['EMPLOYER_NAME'])['CASE_STATUS'].count().reset_index(name='count')
    count = len(top_emp2['EMPLOYER_NAME'].unique())
    st.subheader(count) 

with col2:
    st.write(":red[Median Wage]")
    state_count2 = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE','state_name', 'popullation']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    state_count2['count_per_10k'] = ((state_count2['count']/state_count2['popullation'])*10000).round(0)
    user_state_median_wage = state_count2.loc[state_count2['state_name'] == user_state, 'median_wage'].values[0]
    st.subheader(f"${user_state_median_wage}")
  

