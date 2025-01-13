import geopandas
import pydeck

def load_data(filepath):
    return geopandas.read_file(filepath)

def create_layer(data, color):
    return pydeck.Layer(
        "GeoJsonLayer",
        data,
        opacity=0.7,
        pickable=True,
        stroked=True, 
        get_line_color=color,  
        get_line_width=10, 
    )