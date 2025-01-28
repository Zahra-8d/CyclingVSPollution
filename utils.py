import geopandas
import pydeck

from typing import Literal
from db_utils import getBikeLaneDF, getCityZoomPoint, getPollutionDF

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
                        color_rgb: list[int] = [3,125,80]
                        ) -> pydeck.Layer:
    
    data = getBikeLaneDF(city=city)

    layer = pydeck.Layer(
            type='PathLayer',
            data = data,
            opacity=0.7,
            get_color=color_rgb,
            width_scale=2,
            width_min_pixels=2,
            get_path = 'Geom', 
            get_width=10
    )

    return layer

def createPollutionLayer(city: Literal['Berlin', 'London'],
                         color_rgb: list[int] = [255,127,80]
                         ) -> pydeck.Layer:
            
    data = getPollutionDF(city=city)
    
    layer = pydeck.Layer(
            "PolygonLayer",
            opacity=0.05,
            data=data,
            get_polygon="Geom",
            get_elevation="NO2",
            get_name = 'Name',
            get_fill_color = 'fill_color',
            get_line_color=[255, 255, 255],
            auto_highlight=True,
            extruded=True,
            pickable=True,
            wireframe=True,
    )

    return layer

def createAllLayers(city: Literal['Berlin', 'London']
                    ) -> tuple[list[pydeck.Layer], float, float]:
    """
    Create all needed layers and return Lat and Lng of where to zoom in on the city
    """

    lng, lat = getCityZoomPoint(city)
    bikelane_layer = createBikeLaneLayer(city)
    pollution_layer = createPollutionLayer(city)

    return [bikelane_layer, pollution_layer], lat, lng