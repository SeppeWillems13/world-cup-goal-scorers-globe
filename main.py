import csv
import plotly.graph_objects as go

# Read the CSV file
with open("edited_cvs/worldcupgoals_1930_2022_BirthPlaceAndCountriesAndLatLong.csv", "r") as f:
    csv_reader = csv.DictReader(f)
    data = list(csv_reader)

# Create a Scattergeo plot
fig = go.Figure(
    go.Scattergeo(
        lat=[float(row["Latitude"]) for row in data],
        lon=[float(row["Longitude"]) for row in data],
        mode="markers",
        marker=dict(
            size=5,
            color="blue",
            opacity=0.7,
        ),
        showlegend=False,
    )
)

# Customize the plot
fig.update_layout(
    title=dict(
        text="Birthplaces of World Cup Goal Scorers",
        font=dict(size=24),
    ),
    geo=dict(
        projection_type="natural earth",
        landcolor="rgb(217, 217, 217)",
        oceancolor="rgb(204, 255, 255)",
        showocean=True,
        showland=True,
        showcountries=True,
        countrywidth=0.5,
        showcoastlines=True,
        coastlinecolor="white",
        coastlinewidth=0.5,
    ),
)

# Show the plot
fig.show()
