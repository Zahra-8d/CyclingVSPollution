import streamlit
import pydeck
from utils import createBikeLaneLayer
from db_utils import getTotalBikeLaneLenghts

# Page header

streamlit.set_page_config(page_title="Cycling VS Pollution", layout="wide", page_icon="🚲")
streamlit.title("Comparative study of Cycling Infrastructure and Pollution levels in Berlin and London")
streamlit.markdown("---")


# get data from database and build layers and views
green_colour = [3,125,80]
red_colour = [255, 0, 0]
zoom = 8
london_population = 8866000
berlin_population = 3432000
london_size = 1572000000 #metres squared
berlin_size = 891700000 #metres squared

london_layer, lat_london, lng_london = createBikeLaneLayer(city='London', color_rgb=green_colour)
berlin_layer, lat_berlin, lng_berlin = createBikeLaneLayer(city='Berlin', color_rgb=green_colour)


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
    streamlit.header("London")
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state = london_view_state,
            layers=[london_layer],
            tooltip={"text": "{name}"}, 
        )
    )
    bike_lane_length = getTotalBikeLaneLenghts('London')
    proportion_by_area = bike_lane_length / london_size
    proportion_by_pop = bike_lane_length / london_population

    streamlit.subheader(f"Cycle lanes per square meter: {proportion_by_area:,.4f}")
    streamlit.subheader(f"Cycle lanes per person: {proportion_by_pop:,.4f}")
    streamlit.text(f"Total cycle lane length: {bike_lane_length:,.2f} metres")
    streamlit.text(f"Total city area: {london_size:,.2f} m²")
    streamlit.text(f"Total city population: {london_population:,.2f}")

with col2:
    streamlit.header("Berlin")
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=berlin_view_state,
            layers=[berlin_layer],
            tooltip={"text": "{name}"}, 
        )
    )

    bike_lane_length = getTotalBikeLaneLenghts('Berlin')
    proportion_by_area = bike_lane_length / berlin_size
    proportion_by_pop = bike_lane_length / berlin_population

    streamlit.subheader(f"Cycle lanes per square meter: {proportion_by_area:,.4f}")
    streamlit.subheader(f"Cycle lanes per person: {proportion_by_pop:,.4f}")
    streamlit.text(f"Total cycle lane length: {bike_lane_length:,.2f} metres")
    streamlit.text(f"Total city area: {berlin_size:,.2f} m²")
    streamlit.text(f"Total city population: {berlin_population:,.2f}")

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
streamlit.text("A project by Zahra Ali, Yuna and Mark")
