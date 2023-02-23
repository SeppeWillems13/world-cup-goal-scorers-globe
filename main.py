import json
import os
import pandas as pd
import streamlit as st


def setup():
    # Set the app title
    st.set_page_config(page_title="World Cup Goals")
    header = st.header("")
    header.markdown("<script src='https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.10.0/dist/tf.min.js'></script>",
                    unsafe_allow_html=True)


def load_data():
    global df, world_cup_years
    # Get the absolute path of the current directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Read in the CSV file as a DataFrame
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, 'edited_cvs/worldcupgoals_1930_2022.csv'),
                         encoding='iso-8859-1')
    except FileNotFoundError:
        print("Error: CSV file not found.")
        df = pd.DataFrame()
    # Define a list of all the World Cup years
    world_cup_years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998,
                       2002,
                       2006, 2010, 2014, 2018, 2022]


@st.cache_data()
def filter_data(selected_years, name_search, goals, selected_countries, birthplace_search, different_country=False):
    # Convert the integer values in selected_years to strings
    selected_years = list(map(str, selected_years))

    # Filter the DataFrame based on the selected World Cup year
    df_filtered = df[df['Years'].str.contains('|'.join(selected_years))]

    # Filter the DataFrame based on the selected countries
    if selected_countries:
        df_filtered = df_filtered[(df_filtered['Country'].isin(selected_countries))]

    # Filter the DataFrame based on birthplace search
    if birthplace_search:
        df_filtered = df_filtered[df_filtered['BirthPlace'] == birthplace_search]

    # Filter the DataFrame based on name search input
    if name_search:
        df_filtered = df_filtered[df_filtered['Player'].str.contains(name_search, case=False)]

    # Filter the DataFrame based on country of birth
    if different_country:
        df_filtered = df_filtered[df_filtered['Country'] != df_filtered['CountryOfBirth']]

    # Count the number of distinct countries in the filtered DataFrame
    num_countries = len(df_filtered['Country'].unique())

    return df_filtered, num_countries


def filter_data_sidebar():
    global selected_world_cup_years, different_country, selected_countries, birthplace_search, max_goals_value, goals, df_filtered, num_countries, name_search, detailed
    # Add a multiselect to select World Cup years
    selected_world_cup_years = st.sidebar.multiselect('Select World Cup years:', world_cup_years)
    # Create a slider for filtering by goals scored
    goals = st.sidebar.slider("Filter by Goals Scored:", 1, 15, 1)

    # Create a multiselect dropdown with all countries
    selected_countries = st.sidebar.multiselect("Filter by Country (e.g. Germany):", sorted(df['Country'].unique()))

    if selected_countries:
        filtered_birthplaces = list(
            set(df.dropna(subset=['BirthPlace']).loc[(df['Country'].isin(selected_countries)), 'BirthPlace'].unique()))
        filtered_birthplaces.sort()
        birthplace_search = st.sidebar.selectbox("Search for a player by birthplace:",
                                                 options=[''] + filtered_birthplaces,
                                                 index=0)
    else:
        birthplace_search = st.sidebar.selectbox("Search for a player by birthplace:",
                                                 options=[''] + list(df['BirthPlace'].unique()),
                                                 index=0)

        # Create a search box for player name input
    all_player_names = list(df['Player'])
    all_player_names.sort()
    if selected_countries:
        all_player_names = list(df.loc[df['Country'].isin(selected_countries), 'Player'].unique())
        all_player_names.sort()
        name_search = st.sidebar.selectbox("Search for a player by name:", options=[''] + all_player_names, index=0)
    else:
        name_search = st.sidebar.selectbox("Search for a player by name:", options=[''] + all_player_names, index=0)

    # Create a checkbox for players born in a different country than they played for
    different_country = st.sidebar.checkbox("Players Born in a Different BirthCountry")
    if different_country:
        df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals, selected_countries,
                                                 birthplace_search, True)
    else:
        df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals, selected_countries,
                                                 birthplace_search, False)
    return selected_world_cup_years, name_search, goals, selected_countries, birthplace_search, different_country


def render_map():
    selected_world_cup_years, name_search, goals, selected_countries, birthplace_search, different_country = filter_data_sidebar()

    # Filter the DataFrame based on selected World Cup years, name search input, and goals scored
    df_filtered, num_countries = filter_data(selected_world_cup_years, name_search, goals, selected_countries,
                                             birthplace_search, different_country)

    total_players = len(df_filtered)

    st.header(f"World Cup Goals ({total_players} Players,{num_countries} Countries)")

    # Rename the 'Latitude' column to 'lat'
    df_filtered = df_filtered.rename(columns={'Latitude': 'LAT'})
    df_filtered = df_filtered.rename(columns={'Longitude': 'LON'})

    # Display the map in Streamlit app
    st.map(df_filtered[['LAT', 'LON']])

    st.subheader("Filtered Players (first 100 rows):")

    all_birthplaces = list(df_filtered['BirthPlace'].unique())

    search_birthplace = st.selectbox("Search for a BirthPlace:", options=[''] + all_birthplaces, index=0)
    if search_birthplace:
        df_filtered = df_filtered[df_filtered['BirthPlace'] == search_birthplace]

    player_data = df_filtered[['Player', 'Goals', 'Country', 'BirthPlace', 'CountryOfBirth']]

    player_data['Goals'] = player_data['Goals'].apply(lambda x: json.loads(x.replace("'", "\"")))
    player_data = player_data[player_data['Goals'].apply(lambda x: isinstance(x, dict))]
    player_data['Goals'] = player_data['Goals'].apply(lambda x: '\n'.join([f"{k}: {v[0]}" for k, v in x.items()]))

    list_df = [player_data[i:i + 100] for i in range(0, player_data.shape[0], 100)]
    if len(list_df) > 0:
        merged_df = pd.concat(list_df, ignore_index=True)
        st.table(merged_df.head(100))
    else:
        st.warning("No players found matching the selected criteria.")


def disclaimer():
    # Add the disclaimer at the bottom of the page
    st.markdown('---')
    st.write("Disclaimer: The data in this app is sourced from Wikipedia and may contain inaccuracies. The number of "
             "World Cup years a player is listed as having played in is not necessarily the same as the number of years "
             "they actually scored a goal. Additionally, some countries listed may no longer exist or have different "
             "names. This data is incomplete and may be updated in the future. Please note that players born in the same "
             "city may have slightly diverging latitude and longitude coordinates in order to prevent overlapping on the "
             "map visualization. As a result, the displayed locations may not exactly reflect the actual birthplace of "
             "the players.")


def main():
    setup()
    load_data()
    render_map()
    disclaimer()


if __name__ == '__main__':
    main()
