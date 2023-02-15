import os
import pandas as pd
import plotly.express as px
import streamlit as st


# Allow CORS (Cross-Origin Resource Sharing)
def allow_cors():
    header = st.header("")
    header.markdown("<script src='https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.10.0/dist/tf.min.js'></script>",
                    unsafe_allow_html=True)


allow_cors()

# your app routes go here
# Set the app title
st.set_page_config(page_title="World Cup Goals")

# Get the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Read in the CSV file as a DataFrame
df = pd.read_csv(os.path.join(BASE_DIR, 'edited_cvs/worldcupgoals_1930_2022.csv'),
                 encoding='iso-8859-1')

# Define a list of all the World Cup years
world_cup_years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002,
                   2006, 2010, 2014, 2018, 2022]


@st.cache_data()
def filter_data(selected_years, name_search, goals):
    # Convert the integer values in selected_years to strings
    selected_years = list(map(str, selected_years))

    # Filter the DataFrame based on the selected World Cup year
    if selected_years:
        df_filtered = df[df['Years'].str.contains('|'.join(selected_years))]
    else:
        df_filtered = df

    # Filter the DataFrame based on name search input
    if name_search:
        df_filtered = df_filtered[df_filtered['Player'].str.contains(name_search, case=False)]

    # Filter the DataFrame based on goals scored
    df_filtered = df_filtered[(df_filtered['Goals'] >= goals)]

    # Count the number of distinct countries in the filtered DataFrame
    num_countries = len(df_filtered['Country'].unique())

    return df_filtered, num_countries


# Add a multiselect to select World Cup years
selected_world_cup_years = st.sidebar.multiselect('Select World Cup years:', world_cup_years)

# Add a name search input
name_search = st.sidebar.text_input("Search for a player by name:")

# Add a slider to filter by goals scored
max_goals = int(df['Goals'].max())
goals = st.sidebar.slider("Filter by number of goals scored:", min_value=1, max_value=max_goals, value=1)

detailed = st.sidebar.checkbox('Player details')

if not detailed:
    # Filter the DataFrame based on selected World Cup years, name search input, and goals scored
    df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals)

    total_players = len(df_filtered)
    total_goals = df_filtered['Goals'].sum()

    st.header(f"World Cup Goals ({total_players} Players, {total_goals} Goals, {num_countries} Countries)")

    # Rename the 'Latitude' column to 'lat'
    df_filtered = df_filtered.rename(columns={'Latitude': 'LAT'})
    df_filtered = df_filtered.rename(columns={'Longitude': 'LON'})
    # Display the map in Streamlit app
    st.map(df_filtered)
else:
    df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals)

    # Add a selectbox to select the map scope
    map_scopes = ['world', 'europe', 'asia', 'africa', 'north america', 'south america']
    scope = st.sidebar.selectbox('Map scope', map_scopes, index=0)

    fig = px.scatter_geo(df_filtered,
                         lat="Latitude",
                         lon="Longitude",
                         color="Country",
                         hover_name="Player",
                         size="Goals",
                         size_max=max_goals,
                         projection="natural earth",
                         scope=scope,
                         hover_data={
                             'CountryOfBirth': True,
                             'Goals': True,
                             'Country': False,
                             'Latitude': False,
                             'Longitude': False,
                         },
                         )
    fig.update_geos(showcountries=True, countrycolor="Black", showsubunits=True, subunitcolor="Blue")

    # Filter the DataFrame based on selected World Cup years, name search input, and goals scored
    df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals)

    total_players = len(df_filtered)
    total_goals = df_filtered['Goals'].sum()

    # Title
    st.title(f"World Cup Goals ({total_players} Players, {total_goals} Goals, {num_countries} Countries)")

    # Display the chart in Streamlit app
    st.plotly_chart(fig)
# Add the disclaimer at the bottom of the page
st.markdown('---')
st.write(
    "Disclaimer: The data in this app is sourced from Wikipedia and may contain inaccuracies. The number of World Cup years a player is listed as having played in is not necessarily the same as the number of years they actually scored a goal. Additionally, some countries listed may no longer exist or have different names. This data is incomplete and may be updated in the future.")
