# run this command in terminal streamlit run code_1.py --server.maxMessageSize 400

import pandas as pd
import streamlit as st
import altair as alt
alt.data_transformers.enable("vegafusion")


h1b = pd.read_csv('h1b_data_10ksample.csv', encoding='ISO-8859-1')

# st.write(h1b)

# colname = list(h1b.columns)
# st.write(f"Colnames are =  {colname}")

#####  Cache ####

# @st.cache_data
# def load_data(csv):
#     df = pd.read_csv(csv)
#     return df
# df = load_data("<path to csv>")
# st.dataframe(df)



st.markdown('''
            # Analysing H1B Data
            ''')
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