import streamlit
import pydeck
from utils import load_data, create_layer

# Page header

streamlit.set_page_config(page_title="Cycling VS Pollution", layout="wide", page_icon="🚲")
streamlit.title("Comparative study of Cycling Infrastructure and Pollution levels in Berlin and London")
streamlit.markdown("---")


# get data and build layers and views

london_cyclepath_data = load_data("data/CycleRoutesLondon.geojson")
berlin_cyclepath_data = load_data("data/CycleRoutesBerlin.geojson")
green_colour = [3,125,80]
red_colour = [255, 0, 0]
zoom = 11


london_layer = create_layer(london_cyclepath_data, green_colour) 
berlin_layer = create_layer(berlin_cyclepath_data, green_colour)

london_view_state = pydeck.ViewState(
    latitude=london_cyclepath_data.geometry.centroid.y.mean(),
    longitude=london_cyclepath_data.geometry.centroid.x.mean(),
    zoom=zoom
)

berlin_view_state = pydeck.ViewState(
    latitude=float(berlin_cyclepath_data.geometry.centroid.y.mean()),
    longitude=float(berlin_cyclepath_data.geometry.centroid.x.mean()),
    zoom=zoom
)

# make columns and maps

col1, col2 = streamlit.columns(2)

with col1:
    streamlit.subheader("London")
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state = london_view_state,
            layers=[london_layer],
            tooltip={"text": "{name}"}, 
        )
    )

with col2:
    streamlit.subheader("Berlin")
    streamlit.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=berlin_view_state,
            layers=[berlin_layer],
            tooltip={"text": "{name}"}, 
        )
    )

# Legend html

legend_html = """
<div style="background-color: black; padding: 20px; border-radius: 5px; border: 1px solid #ccc; width: 260px;">
    <h4 style="margin-top: 0;">Legend</h4>
    <div>
        <span style="display: inline-block; width: 20px; height: 20px; border-bottom: 2px solid rgb({green_colour[0]}, {green_colour[1]}, {green_colour[2]}); margin-right: 10px;"></span>
        <span>Cycling path</span>
    </div>
    <div>
        <span style="display: inline-block; width: 20px; height: 20px; border-bottom: 6px solid rgb({red_colour[0]}, {red_colour[1]}, {red_colour[2]}); margin-right: 10px;"></span>
        <span>Pollution hotspot</span>
    </div>
</div>
"""
streamlit.markdown(legend_html, unsafe_allow_html=True)


# Page Footer

streamlit.markdown("---")
streamlit.text("A project by Zahra Ali, Yuna and Mark")
