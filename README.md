# Streamlit App
https://h1b-analysis.streamlit.app/
- ## Features
1. Geographic Insights
An interactive map of U.S. states is available, color-coded based on the number of certified cases per 10,000 population for each state. This feature provides a visual representation of H-1B labor trends across the country.

2. State Overview
Users can select a state of interest to obtain detailed information, including:
    - Median Wage: Explore the median wage for the selected state.
    - Total Employers: View the total number of employers in the chosen state.
    - Certified Cases: Access information on the total number of certified cases in the state.

3. In-Depth State Analysis
Users can delve deeper into specific states to uncover detailed information such as:
    - Top Job Titles: Identify the most prevalent job titles in the selected state.
    - Top Cities to Work In: Explore the top cities within the state for H-1B employment.
    - Top Employers: Discover the leading employers based on either the highest certified case count or the highest median wage.

# Introduction
If you plan to work in the US on H-1B Visa, The LCA is a document that the employer must file with the U.S. Department of Labor (DOL) before they can submit an H-1B visa petition to the U.S. Citizenship and Immigration Services (USCIS). A Certified LCA is one of the first steps toward getting your H-1B work visa in the U.S.

# Use Case
The H-1B Analysis app is designed to empower users with comprehensive information and analytics related to the LCA process. Gain valuable insights into certified applications, annual wages, top employers, and key trends across U.S. states. Whether you are an employer, a prospective H-1B visa applicant, or a researcher, this app provides a valuable resource for understanding and analyzing H-1B labor certification trends.

# Data Preparation
- One common error in map creation is the tendency to generate a population density map, rather than crafting a map that accurately portrays the specific scenario related to the topic. In order to overcome this challenge, I added US State population data and calculated how many certified cases there were in each state for every 10,000 people.
- Added geojson file and joined on US State Name to get the State Boundaries for the plotting the map.

# Data Sources
1. The dataset contains more than 1.7 million LCA disclosure data records (2020 - 2023) from the United States Department of Labor (https://www.dol.gov/agencies/eta/foreign-labor/performance)
2. The geojson file for US State Boundaries (https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/?flg=en-us)
3. The US state population data (https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html)

# Future Work
1. Integration with External Datasets:
Explore opportunities to integrate additional datasets, such as economic indicators, immigration policies, or industry-specific data, to       provide a more comprehensive understanding of the factors influencing H-1B labor dynamics.

2. Predictive Analytics:
Integrate predictive modeling to forecast future H-1B labor trends and provide insights into potential shifts in job demand, wage patterns, and geographical preferences.

3. Feedback Mechanism and User Surveys:
Implement a feedback mechanism and conduct user surveys to gather input on user experiences and preferences, guiding future enhancements and ensuring the app meets the evolving needs of its users.