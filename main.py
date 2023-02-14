import pandas as pd
import streamlit as st
import plotly.express as px

# Read in the CSV file as a DataFrame
df = pd.read_csv('edited_cvs/worldcupgoals_1930_2022_BirthPlaceAndCountriesAndLatLong.csv', encoding='iso-8859-1')

# Sort the DataFrame by country in alphabetical order
df = df.sort_values('Country', ascending=True)

# Add a name search input
name_search = st.sidebar.text_input("Search for a player by name:")

# Filter the DataFrame based on name search input
if name_search:
    df = df[df['Player'].str.contains(name_search, case=False)]

# Add a slider to filter by goals scored
goals = st.sidebar.slider("Filter by number of goals scored:", min_value=0, max_value=20, value=0)

# Filter the DataFrame based on goals scored
df = df[df['Goals'] >= goals]

# Add a checkbox to show goalscorers born outside of the country they played for
show_foreign = st.sidebar.checkbox("Show goalscorers born outside of the country they played for")

# Filter the DataFrame based on the checkbox selection
if not show_foreign:
    df = df[df['Country'] == df['CountryOfBirth']]

# Create a Plotly chart
fig = px.scatter_geo(df, lat="Latitude", lon="Longitude", color="Country",
                     hover_name="Player", size="Goals",
                     projection="natural earth", scope='world',
                     hover_data={'CountryOfBirth': False, 'Country': True, 'Goals': True})

# Add country lines to the chart
fig.update_geos(showcountries=True, countrycolor="Black", showsubunits=True, subunitcolor="Blue")

#title
st.title("World Cup Goals by Birth Country")

# Display the chart in Streamlit app
st.plotly_chart(fig)
