# run this command in terminal streamlit run main.py --server.maxMessageSize 400

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


# st.set_page_config(layout="wide")

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

# st.markdown('''
#             ### Top Cities
#             ''')

# st.sidebar.header('Top cities based on number of applications')
# number_of_cities = st.sidebar.slider("Number of Cities",min_value=1,max_value=20,value=5, step=1)

# city_count = h1b.groupby(['WORKSITE_CITY'])['CASE_NUMBER'].count().reset_index(name='count')
# top_city_count = city_count.sort_values('count', ascending=False).head(number_of_cities)
# bar2 = alt.Chart(top_city_count).mark_bar().encode(
# alt.X('count', title='Number of Applications'),
# alt.Y('WORKSITE_CITY', sort='-x', title='City'))
# st.altair_chart(bar2, use_container_width=True)


number_of_states = st.slider("Number of States",min_value=1,max_value=51,value=10, step=1)


st.subheader('TOP STATES')
# TOP STATES

# top states based on Certified

state_count = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE','state_name', 'popullation'])['CASE_STATUS'].count().reset_index(name='count')
state_count['count_per_10k'] = ((state_count['count']/state_count['popullation'])*10000).round(0)
top_state_count = state_count.sort_values('count_per_10k', ascending=False).head(number_of_states)

temp_bar = alt.Chart(top_state_count).mark_bar(color='orange').encode(
alt.X('count_per_10k', title='Number of Applications per 10k people'),
alt.Y('state_name', sort='-x', title='State'))

st.altair_chart(temp_bar, use_container_width=True)

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
    temp = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE','state_name', 'popullation']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    temp['count_per_10k'] = ((temp['count']/temp['popullation'])*10000).round(0)
    user_state_median_wage = temp.loc[temp['state_name'] == user_state, 'median_wage'].values[0]
    st.subheader(f"${user_state_median_wage}")
  



# TOP CITIES
h1b.loc[h1b.WORKSITE_STATE == 'DC', 'WORKSITE_CITY'] = "Washington"
# give this list as option to choose to the user
# user selects one of the states from the list
# search cities based on the USER_STATE variable

top_cities = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['WORKSITE_CITY'])['CASE_STATUS'].count().reset_index(name='count')
top_cities_count = top_cities.sort_values('count', ascending=False).head(5)

st.subheader("Top 5 Cities")
city_bar = alt.Chart(top_cities_count).mark_bar().encode(
alt.X('count', title='Number of Applications'),
alt.Y('WORKSITE_CITY', sort='-x', title='City'))

st.altair_chart(city_bar, use_container_width=True)


# TOP EMPLOYERS

# give the STATE list as option to choose to the user
# user selects one of the states from the list
# search EMPLOYERS based on the USER_STATE variable

# top cities based on USER_variable, for now lets assume user_variable == 'CA'

# can make a word map


top_emp = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['EMPLOYER_NAME'])['CASE_STATUS'].count().reset_index(name='count')
top_emp_count = top_emp.sort_values('count', ascending=False).head(10)

st.subheader("Top 10 Employers")
emp_bar = alt.Chart(top_emp_count).mark_bar().encode(
alt.X('count', title='Number of Applications'),
alt.Y('EMPLOYER_NAME', sort='-x', title='Employer'))

st.altair_chart(emp_bar, use_container_width=True)

# TOP JOB TITLES

# give the STATE list as option to choose to the user
# user selects one of the states from the list
# search EMPLOYERS based on the USER_STATE variable

# top cities based on USER_variable, for now lets assume user_variable == 'CA'


top_jobs = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['SOC_TITLE'])['CASE_STATUS'].count().reset_index(name='count')
top_job_count = top_jobs.sort_values('count', ascending=False).head(10)

st.subheader("Top 10 Jobs")
job_bar = alt.Chart(top_job_count).mark_bar().encode(
alt.X('count', title='Number of Applications'),
alt.Y('SOC_TITLE', sort='-x', title='Job Title'))

st.altair_chart(job_bar, use_container_width=True)




## Temp

temp = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE','state_name', 'popullation']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
temp['count_per_10k'] = ((temp['count']/temp['popullation'])*10000).round(0)
top_emp2 = temp.sort_values('count_per_10k', ascending=False).head(5)


temp_bar = alt.Chart(top_emp2).mark_bar().encode(
alt.X('count_per_10k', title='Number of Applications per 10k people'),
alt.Y('state_name', sort='-x', title='State'),
alt.Color('median_wage:Q', title='Median Wage', scale=alt.Scale(scheme='tealblues')))

st.altair_chart(temp_bar, use_container_width=True)