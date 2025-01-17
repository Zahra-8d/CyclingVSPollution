import geopandas
import pydeck

from typing import Literal
from db_utils import BikeLaneDBtoPandas, getCentroid

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

def createBikeLaneLayer(city: Literal['Berlin', 'London'],
                        color_rgb: list[int] = [3,125,80]) -> tuple[pydeck.Layer, float, float]:
    """
    Return the pydeck.Layer and the mean Lat and Lng for the chosen city
    """
    
    data = BikeLaneDBtoPandas(city=city)
    Clng, Clat = getCentroid(city=city)

    layer = pydeck.Layer(
            type='PathLayer',
            data = data,
            opacity=0.7,
            pickable=True,
            get_color=color_rgb,
            width_scale=2,
            width_min_pixels=2,
            get_path = 'Geom', 
            get_width=10
    )
    
    return layer, Clat, Clng
