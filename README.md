# Streamlit App
https://h1b-analysis.streamlit.app/
- # Features
# Introduction
If you plan to work in the US on H-1B Visa, The LCA is a document that the employer must file with the U.S. Department of Labor (DOL) before they can submit an H-1B visa petition to the U.S. Citizenship and Immigration Services (USCIS). A Certified LCA is one of the first steps toward getting your H-1B work visa in the U.S.

- USE CASE can come here


# Data Preparation
- One common error in map creation is the tendency to generate a population density map, rather than crafting a map that accurately portrays the specific scenario related to the topic. In order to overcome this challenge, I added US State population data and calculated how many certified cases there were in each state for every 10,000 people.
- Added geojson file and joined on US State Name to get the State Boundaries for the plotting the map.

# Data Sources
1. The dataset contains more than 2.4 million LCA disclosure data records (2019 - 2023) from the United States Department of Labor (https://www.dol.gov/agencies/eta/foreign-labor/performance)
2. The geojson file for US State Boundaries (https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/?flg=en-us)
3. The US state population data (https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html)

# Future Work
