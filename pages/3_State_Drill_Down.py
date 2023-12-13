from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
alt.data_transformers.enable("vegafusion")
st.set_page_config(layout="wide")

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

st.title("US State - Drill Down")

#getting states in a list

user_state = st.selectbox('Select a State', sorted(h1b['state_name'].unique().tolist()))


col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('''
            ##### Certified Cases
            ''')
    state_data = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['state_name', 'EMPLOYER_NAME']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    total = state_data['count'].sum()
    st.header(f":red[{total}]")

with col2:
    st.markdown('''
            ##### Number of Employers
            ''')
    state_data = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['state_name', 'EMPLOYER_NAME']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    count = len(state_data['EMPLOYER_NAME'].unique())
    st.header(f":red[{count}]")

with col3:
    st.markdown('''
            ##### Median Wage
            ''')
    state_data = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['state_name', 'EMPLOYER_NAME']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    wage = state_data['median_wage'].median()
    st.header(f":red[${wage}]")






tab1, tab2, tab3 = st.tabs(["Top Cities", "Top Employers", "Top Jobs"])

with tab1: # TOP CITIES
    h1b.loc[h1b.WORKSITE_STATE == 'DC', 'WORKSITE_CITY'] = "Washington"
    # give this list as option to choose to the user
    # user selects one of the states from the list
    # search cities based on the USER_STATE variable

    top_cities = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['WORKSITE_CITY']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()

    col1, col2 = st.columns([0.7, 0.3], gap='large')
    with col1:
        number_of_cities = st.slider("Number of Cities",min_value=1,max_value=20,value=10, step=1)
    with col2:
        radio_button_options_city = ['Certified Count', 'Median Wage']
        user_sort_city = st.radio('Cities by:', radio_button_options_city)
    
    if user_sort_city == 'Certified Count':
        top_cities_count = top_cities.sort_values('count', ascending=False).head(number_of_cities)
        city_bar = alt.Chart(top_cities_count).mark_bar().encode(
        alt.X('count', title='Number of Certified'),
        alt.Y('WORKSITE_CITY', sort='-x', title='City'),
        tooltip=[alt.Tooltip('WORKSITE_CITY:N', title='City:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
        )

        st.subheader(f"Top :red[{number_of_cities}] Cities by Certified Count")
        st.altair_chart(city_bar, use_container_width=True)

    else:
        top_cities_count = top_cities.sort_values('median_wage', ascending=False).head(number_of_cities)
        city_bar = alt.Chart(top_cities_count).mark_bar().encode(
        alt.X('median_wage', title='Median Wage'),
        alt.Y('WORKSITE_CITY', sort='-x', title='City'),
        tooltip=[alt.Tooltip('WORKSITE_CITY:N', title='City:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
        )

        st.subheader(f"Top :red[{number_of_cities}] Cities by Median Wage")
        st.altair_chart(city_bar, use_container_width=True)

with tab2: # TOP EMPLOYERS
    top_emp = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['EMPLOYER_NAME']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()
    
    col1, col2 = st.columns([0.7, 0.3], gap='large')
    with col1:
        number_of_employers = st.slider("Number of Employers",min_value=1,max_value=20,value=10, step=1)
    with col2:
        radio_button_options_emp = ['Certified Count', 'Median Wage']
        user_sort_emp = st.radio('Employers by:', radio_button_options_emp)
    
    if user_sort_emp == 'Certified Count':
        top_emp_count = top_emp.sort_values('count', ascending=False).head(number_of_employers)

        emp_bar = alt.Chart(top_emp_count).mark_bar().encode(
        alt.X('count', title='Number of Certified'),
        alt.Y('EMPLOYER_NAME', sort='-x', title='Employer'),
        tooltip=[alt.Tooltip('EMPLOYER_NAME:N', title='Employer:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
        )

        st.subheader(f"Top :red[{number_of_employers}] Employers by Certified Count")
        st.altair_chart(emp_bar, use_container_width=True)
    
    else:
        top_emp_count = top_emp.sort_values('median_wage', ascending=False).head(number_of_employers)

        emp_bar = alt.Chart(top_emp_count).mark_bar().encode(
        alt.X('median_wage', title='Median Wage'),
        alt.Y('EMPLOYER_NAME', sort='-x', title='Employer'),
        tooltip=[alt.Tooltip('EMPLOYER_NAME:N', title='Employer:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
        )

        st.subheader(f"Top :red[{number_of_employers}] Employers by Median Wage")
        st.altair_chart(emp_bar, use_container_width=True)        


with tab3: #TOP JOB TITLES
    top_job = h1b[(h1b['CASE_STATUS']=='Certified') & (h1b['state_name'] == user_state)].groupby(['SOC_TITLE']).agg({'CASE_STATUS': 'size', 'PREVAILING_WAGE': 'median'}).rename(columns={'CASE_STATUS' : 'count', 'PREVAILING_WAGE': 'median_wage'}).reset_index()

    col1, col2 = st.columns([0.7, 0.3], gap='large')
    with col1:
        number_of_jobs = st.slider("Number of Job Titles",min_value=1,max_value=20,value=10, step=1)
    with col2:
        radio_button_options_job = ['Certified Count', 'Median Wage']
        user_sort_job = st.radio('Job Titles by:', radio_button_options_job)

    if user_sort_job == 'Certified Count':
        top_job_count = top_job.sort_values('count', ascending=False).head(number_of_jobs)
        job_bar = alt.Chart(top_job_count).mark_bar().encode(
            alt.X('count', title='Number of Certified'),
            alt.Y('SOC_TITLE', sort='-x', title='Job Title'),
            tooltip=[alt.Tooltip('SOC_TITLE:N', title='Job Title:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
            )
        st.subheader(f"Top :red[{number_of_jobs}] Job Titles by Certified Count")
        st.altair_chart(job_bar, use_container_width=True)

    else:
        top_job_count = top_job.sort_values('median_wage', ascending=False).head(number_of_jobs)
        job_bar = alt.Chart(top_job_count).mark_bar().encode(
            alt.X('median_wage', title='Median Wage'),
            alt.Y('SOC_TITLE', sort='-x', title='Job Title'),
            tooltip=[alt.Tooltip('SOC_TITLE:N', title='Job Title:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')]
            )
        st.subheader(f"Top :red[{number_of_jobs}] Job Titles by Median Wage")
        st.altair_chart(job_bar, use_container_width=True)
        
    # st.dataframe(top_job_count)
    

    # job_bar = alt.Chart(top_job_count).mark_bar().encode(
    # alt.X('count', title='Number of Certified'),
    # alt.Y('SOC_TITLE', sort='-x', title='Job Title'),
    # tooltip=[alt.Tooltip('SOC_TITLE:N', title='Job Title:'), alt.Tooltip('count:Q', title='Number of Certified:', format=',d'), alt.Tooltip('median_wage:Q', title='Median Wage ($):', format=',d')])

    # st.subheader(f"Top :red[{number_of_jobs}] Job Titles")
    # st.altair_chart(job_bar, use_container_width=True)
