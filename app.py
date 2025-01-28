import streamlit
import pydeck
from utils import createAllLayers
from db_utils import getBikeLaneLenght_perKM2, getBikeLaneLenght_perPER, getBikeLaneLenght_SUM, getCityArea, getCityPopulation

# Page header

streamlit.set_page_config(page_title="Cycling VS Pollution", layout="wide", page_icon="🚲")
streamlit.title("Comparative study of Cycling Infrastructure and Pollution levels in Berlin and London")
streamlit.markdown("---")


# get data from database and build layers and views
green_colour = [3,125,80]
red_colour = [255, 0, 0]
zoom = 8

london_layers, lat_london, lng_london = createAllLayers(city='London')
berlin_layers, lat_berlin, lng_berlin = createAllLayers(city='Berlin')

london_view_state = pydeck.ViewState(
    latitude=lat_london,
    longitude=lng_london,
    zoom=zoom
)

berlin_view_state = pydeck.ViewState(
    latitude=lat_berlin,
    longitude=lng_berlin,
    zoom=zoom
)

# make columns and maps

col1, col2 = streamlit.columns(2)

with col1:
    streamlit.header('London')
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state = london_view_state,
            layers=london_layers,
            tooltip={"html": "<b>District:</b> {Name} <br /><b>NO2:</b> {NO2} µg/m3"}, 
        )
    )

    streamlit.subheader(f"Cycle lanes per area: {getBikeLaneLenght_perKM2('London'):,.4f} m/km²")
    streamlit.subheader(f"Cycle lanes per person: {getBikeLaneLenght_perPER('London'):,.4f} m/person")
    streamlit.text(f"Total cycle lane length: {getBikeLaneLenght_SUM('London'):,.2f} m")
    streamlit.text(f"Total city area: {getCityArea('London'):,.2f} km²")
    streamlit.text(f"Total city population: {getCityPopulation('London'):,.2f} inh.")

with col2:
    streamlit.header("Berlin")
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=berlin_view_state,
            layers=berlin_layers,
            tooltip={"html": "<b>District:</b> {Name} <br /><b>NO2:</b> {NO2} µg/m3"}, 
        )
    )

    streamlit.subheader(f"Cycle lanes per area: {getBikeLaneLenght_perKM2('Berlin'):,.4f} m/km²")
    streamlit.subheader(f"Cycle lanes per person: {getBikeLaneLenght_perPER('Berlin'):,.4f} m/person")
    streamlit.text(f"Total cycle lane length: {getBikeLaneLenght_SUM('Berlin'):,.2f} m")
    streamlit.text(f"Total city area: {getCityArea('Berlin'):,.2f} km²")
    streamlit.text(f"Total city population: {getCityPopulation('Berlin'):,.2f} inh.")

streamlit.text(" ")
streamlit.text(" ")
# Legend html

legend_html = f"""
<div style="background-color: black; padding: 20px; border-radius: 5px; border: 1px solid #ccc; width: 260px;">
    <h4 style="margin-top: 0;padding: 0; margin-bottom: 7px">Legend</h4>
    <div>
        <span style="display: inline-block; width: 20px; height: 20px; border-bottom: 2px solid rgb({green_colour[0]}, {green_colour[1]}, {green_colour[2]}); margin-right: 10px;"></span>
        <span>Cycling path</span>
    </div>
    <div>
        <span style="display: inline-block; width: 20px; height: 20px; border-bottom: 15px solid rgb({red_colour[0]}, {red_colour[1]}, {red_colour[2]}); margin-right: 10px;"></span>
        <span>Pollution hotspot</span>
    </div>
</div>
"""
streamlit.markdown(legend_html, unsafe_allow_html=True)

streamlit.text(" ")
streamlit.text(" ")
streamlit.text(" ")

# Page Footer

streamlit.markdown("---")
streamlit.text("A project by Zahra Ali, Mark Grmek, Kyung Yun Choi")
