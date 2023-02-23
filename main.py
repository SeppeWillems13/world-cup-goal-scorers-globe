import json
import os
import pandas as pd
import streamlit as st
from typing import List, Tuple

# Global variables
WORLD_CUP_YEARS = [
    1930,
    1934,
    1938,
    1950,
    1954,
    1958,
    1962,
    1966,
    1970,
    1974,
    1978,
    1982,
    1986,
    1990,
    1994,
    1998,
    2002,
    2006,
    2010,
    2014,
    2018,
    2022,
]
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, "edited_cvs/worldcupgoals_1930_2022.csv")


def setup() -> None:
    st.set_page_config(page_title="World Cup Goals")
    st.header("")
    st.markdown(
        "<script src='https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.10.0/dist/tf.min.js'></script>",
        unsafe_allow_html=True,
    )


def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv(CSV_PATH, encoding="iso-8859-1")
    except FileNotFoundError:
        st.error("Error: CSV file not found.")
        df = pd.DataFrame()
    return df


@st.cache_data()
def filter_data(
    df: pd.DataFrame,
    selected_years: List[int],
    name_search: str,
    goals: int,
    selected_countries: List[str],
    birthplace_search: str,
    different_country: bool,
) -> Tuple[pd.DataFrame, int]:
    selected_years_str = list(map(str, selected_years))
    df_filtered = df[df["Years"].str.contains("|".join(selected_years_str))]

    if selected_countries:
        df_filtered = df_filtered[df_filtered["Country"].isin(selected_countries)]

    if birthplace_search:
        df_filtered = df_filtered[df_filtered["BirthPlace"] == birthplace_search]

    if name_search:
        df_filtered = df_filtered[
            df_filtered["Player"].str.contains(name_search, case=False)
        ]

    if different_country:
        df_filtered = df_filtered[
            df_filtered["Country"] != df_filtered["CountryOfBirth"]
        ]

    num_countries = df_filtered["Country"].nunique()

    return df_filtered, num_countries


def filter_data_sidebar(
    df: pd.DataFrame,
) -> Tuple[List[int], str, int, List[str], str, bool]:
    selected_world_cup_years = st.sidebar.multiselect(
        "Select World Cup years:", WORLD_CUP_YEARS
    )
    goals = st.sidebar.slider("Filter by Goals Scored:", 1, 15, 1)
    selected_countries = st.sidebar.multiselect(
        "Filter by Country (e.g. Germany):", sorted(df["Country"].unique())
    )

    birthplace_search = ""
    if selected_countries:
        filtered_birthplaces = sorted(
            set(
                df.dropna(subset=["BirthPlace"])
                .loc[df["Country"].isin(selected_countries), "BirthPlace"]
                .unique()
            )
        )
        birthplace_search = st.sidebar.selectbox(
            "Search for a player by birthplace:", [""] + filtered_birthplaces
        )
    else:
        birthplace_search = st.sidebar.selectbox(
            "Search for a player by birthplace:",
            [""] + sorted(df["BirthPlace"].dropna().unique()),
        )

    all_player_names = sorted(df["Player"].unique())
    if selected_countries:
        all_player_names = sorted(
            df.loc[df["Country"].isin(selected_countries), "Player"].unique()
        )

    name_search = st.sidebar.selectbox(
        "Search for a player by name:", [""] + all_player_names
    )

    different_country = st.sidebar.checkbox("Players Born in a Different BirthCountry")

    return (
        selected_world_cup_years,
        name_search,
        goals,
        selected_countries,
        birthplace_search,
        different_country,
    )


def render_map(df: pd.DataFrame) -> None:
    (
        selected_world_cup_years,
        name_search,
        goals,
        selected_countries,
        birthplace_search,
        different_country,
    ) = filter_data_sidebar(df)

    df_filtered, num_countries = filter_data(
        df,
        selected_world_cup_years,
        name_search,
        goals,
        selected_countries,
        birthplace_search,
        different_country,
    )

    total_players = len(df_filtered)

    st.header(f"World Cup Goals ({total_players} Players, {num_countries} Countries)")

    if not df_filtered.empty:
        df_filtered = df_filtered.rename(
            columns={"Latitude": "LAT", "Longitude": "LON"}
        )
        st.map(df_filtered[["LAT", "LON"]])

        st.subheader("Filtered Players (first 100 rows):")
        all_birthplaces = sorted(df_filtered["BirthPlace"].unique())

        search_birthplace = st.selectbox(
            "Search for a BirthPlace:", [""] + all_birthplaces
        )
        if search_birthplace:
            df_filtered = df_filtered[df_filtered["BirthPlace"] == search_birthplace]

        player_data = df_filtered[
            ["Player", "Goals", "Country", "BirthPlace", "CountryOfBirth"]
        ].copy()

        player_data["Goals"] = player_data["Goals"].apply(
            lambda x: json.loads(x.replace("'", '"'))
        )
        player_data = player_data[
            player_data["Goals"].apply(lambda x: isinstance(x, dict))
        ]
        player_data["Goals"] = player_data["Goals"].apply(
            lambda x: "\n".join([f"{k}: {v[0]}" for k, v in x.items()])
        )

        st.table(player_data.head(100))
    else:
        st.warning("No players found matching the selected criteria.")


def disclaimer() -> None:
    st.markdown("---")
    st.write(
        "Disclaimer: The data in this app is sourced from Wikipedia and may contain inaccuracies. The number of "
        "World Cup years a player is listed as having played in is not necessarily the same as the number of years "
        "they actually scored a goal. Additionally, some countries listed may no longer exist or have different "
        "names. This data is incomplete and may be updated in the future. Please note that players born in the same "
        "city may have slightly diverging latitude and longitude coordinates in order to prevent overlapping on the "
        "map visualization. As a result, the displayed locations may not exactly reflect the actual birthplace of "
        "the players."
    )


def main() -> None:
    setup()
    df = load_data()
    render_map(df)
    disclaimer()


if __name__ == "__main__":
    main()
