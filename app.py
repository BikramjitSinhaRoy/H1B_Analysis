# if streamlit run main_code.py gives error, then run this command in terminal streamlit run main_code.py --server.maxMessageSize 400

import pandas as pd
import streamlit as st
import altair as alt
alt.data_transformers.enable("vegafusion")

# merging csv files 
df1 = pd.read_csv('data/h1b_0_row_100000_88656646-f04a-4c03-babd-35dc1c45e013.csv')
df2 = pd.read_csv('data/h1b_1_row_100000_0722dbd9-add3-4fa0-a4b3-84ccbb1bc301.csv')
df3 = pd.read_csv('data/h1b_2_row_100000_db8275ad-f4c7-44b6-b9fa-f828723862b6.csv')
df4 = pd.read_csv('data/h1b_3_row_100000_9af7689e-dd3b-46c3-b59e-ba559f217769.csv')
df5 = pd.read_csv('data/h1b_4_row_100000_68b349c1-713d-408a-a17b-d98d8ba7490e.csv')
df6 = pd.read_csv('data/h1b_5_row_100000_7d8a907f-74da-4bc4-93fb-bf7f39f3c0c6.csv')
df7 = pd.read_csv('data/h1b_6_row_100000_c11a0d17-8ac5-410a-97e7-2d84a85c6b1c.csv')
df8 = pd.read_csv('data/h1b_7_row_100000_128386ad-7f0e-40d8-a5b7-614b0c337d40.csv')
df9 = pd.read_csv('data/h1b_8_row_100000_be460e73-50c3-4a66-bf5f-5747b9bf7601.csv')
df10 = pd.read_csv('data/h1b_9_row_100000_f91ce906-28d1-425f-a64c-ade6d57d36d9.csv')
df11 = pd.read_csv('data/h1b_10_row_100000_eaa682ee-e7a0-486a-a027-812ecbde2293.csv')
df12 = pd.read_csv('data/h1b_11_row_100000_9f36dbc3-1fbb-4b62-8f45-5a8bfec44d38.csv')
df13 = pd.read_csv('data/h1b_12_row_100000_5145f6db-9df6-4011-900c-73e033d62a62.csv')
df14 = pd.read_csv('data/h1b_13_row_100000_16b323d3-9e5a-4291-b8d3-af8455d931af.csv')
df15 = pd.read_csv('data/h1b_14_row_100000_a5ecb50e-d2b3-4f32-b320-0e182497bac8.csv')
df16 = pd.read_csv('data/h1b_15_row_100000_81c6a785-1c7e-4bd2-9b83-78a35220c0d3.csv')
df17 = pd.read_csv('data/h1b_16_row_100000_6c44e89b-6070-47dc-8ef6-6e9845153ccd.csv')
df18 = pd.read_csv('data/h1b_17_row_100000_29a66c18-b629-4904-b18d-2f85e814301b.csv')
df19 = pd.read_csv('data/h1b_18_row_100000_bb1ffd7b-b051-491f-8d45-16a81eecc6fe.csv')
df20 = pd.read_csv('data/h1b_19_row_100000_0ec3d1c9-a8de-43d6-94c0-396608c56754.csv')
df21 = pd.read_csv('data/h1b_20_row_100000_05826312-cdc0-4aa6-9780-250f27e78ce2.csv')
df22 = pd.read_csv('data/h1b_21_row_100000_ab810638-c26d-4641-853d-b73037103ba4.csv')
df23 = pd.read_csv('data/h1b_22_row_100000_28c753de-36b0-4a6b-8491-6c117438c3d9.csv')
df24 = pd.read_csv('data/h1b_23_row_100000_1df99d12-1095-4800-8eea-2309ff969eb3.csv')
df25 = pd.read_csv('data/h1b_24_row_100000_5272a115-0942-4b85-8dea-7e0718adb3b6.csv')

h1b = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20,df21,df22,df23,df24,df25], ignore_index=True) 


# h1b = pd.read_csv('h1b_data_10ksample.csv', encoding='ISO-8859-1')

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



# st.markdown('''
#             # Analysing H1B Data
#             ''')

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





# top states based on Certified

state_count = h1b[h1b['CASE_STATUS']=='Certified'].groupby(['WORKSITE_STATE'])['CASE_STATUS'].count().reset_index(name='count')
top_state_count = state_count.sort_values('count', ascending=False).head(10)
st.write(top_state_count)