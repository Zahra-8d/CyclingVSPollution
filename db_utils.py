from json import load
from typing import Literal
from sqlalchemy import select, insert, Insert, Select, func
from sqlalchemy.exc import NoResultFound
from shapely import LineString, MultiLineString
from shapely.ops import transform
from shapely import get_coordinates
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.functions import ST_Centroid
from pandas import DataFrame

from engine import engine
from tables import metadata, City, BikeLane

def createTables() -> None:
    metadata.create_all(engine)
    print('All tables sucesfully created')

def dropTables() -> None:
    metadata.drop_all(engine)
    print('All tables sucesfully dropped')

def addCityData() -> None:
    
    data: list[dict] = [{'Name': 'Berlin'},
                        {'Name': 'London'}]
    
    stmt: Insert = insert(City)

    with engine.connect() as conn:
        conn.execute(stmt, data)
        conn.commit()

    print('City data succesfully added to the database')

def getCityID(city: Literal['London','Berlin']) -> int:

    stmt: Select = (select(City.c['ID'])
                    .where(City.c['Name'] == city)
                    )
    
    with engine.connect() as conn:
        data = conn.execute(stmt).fetchone()
    
    if not data:
        raise NoResultFound(f'No city by the name of {city} in the database.')
    
    print(f'City ID = {data[0]} for {city}')
    return data[0]

def _removeZ(x,y,z=None):
    return tuple(filter(None, [x, y]))

def BikeLaneGeoJsontoDB(city: Literal['London','Berlin']) -> None:
    
    #DATA PREP----------------------------------------
    city_id = getCityID(city)
    filename: str = f'data/CycleRoutes{city}.geojson'
    lenght_key: str = 'LAENGE' if city=='Berlin' else 'Shape_Leng'
    
    data: list[dict] = []
    with open(filename) as file:
        print('file opened')
        json_data: dict = load(file)

        for lane in json_data['features']:
            lenght: float = lane['properties'][lenght_key]
            geometry: list[list] = lane['geometry']['coordinates']
    
            #convert nested list to shapely
            linetype = lane['geometry']['type']
            if  linetype == 'LineString':
                geometry = LineString(geometry)
                
            elif linetype == 'MultiLineString':
                geometry = MultiLineString(geometry)
            
            #remove Z coordinate if exists
            geometry = transform(_removeZ, geometry)
  
            #convert from shapely to PostGIS type
            geometry = from_shape(geometry) 

            data.append({'CityID': city_id,
                         'Geom': geometry,
                         'Lenght': lenght})
    
    #DATA WRITE---------------------------------------
    stmt: Insert = insert(BikeLane)

    with engine.connect() as conn:
        conn.execute(stmt, data)
        conn.commit()

    print(f'Bike lanes for {city} succesfully added to the database')

def to_coords(geometry: LineString|MultiLineString) -> list[list]:
    return get_coordinates(geometry).tolist()

def BikeLaneDBtoPandas(city: Literal['Berlin', 'London'],
                       columns: list[str] = ['Geom', 'Lenght']) -> DataFrame:

    #DATA FETCH------------------------------------------------
    stmt: Select = (select(BikeLane.c[*columns])
                    .where(City.c['Name'] == city)
                    .join(City, BikeLane.c['CityID'] == City.c['ID'])
                    )
    
    with engine.connect() as conn:
        data = conn.execute(stmt).fetchall()
    
    if not data: 
        raise NoResultFound(f'Could not find any bike lane data for {city}')
    
    #DATA PREP------------------------------------------------
    data = DataFrame(data=data, columns=columns)
    data['Geom'] = data['Geom'].apply(to_shape) #convert geometry back to shapely
    data['Geom'] = data['Geom'].apply(to_coords)

    return data

def getCentroid(city: Literal['Berlin', 'London']) -> tuple[float, float]:

    stmt: Select = (select(ST_Centroid(BikeLane.c['Geom']))
                    .where(City.c['Name'] == city)
                    .join(City, BikeLane.c['CityID']==City.c['ID']))
    
    with engine.connect() as conn:
        data = conn.execute(stmt).fetchone()

    if not data:
        raise NoResultFound(f'Could not fetch centroid of {city}')

    return tuple(to_shape(data[0]).coords)[0]

def getTotalBikeLaneLenghts(city: Literal['Berlin','London']) -> float:

    stmt: Select = (select(func.sum(BikeLane.c['Lenght']))
                    .where(City.c['Name'] == city)
                    .join(City, BikeLane.c['CityID'] == City.c['ID']))
    
    with engine.connect() as conn:
        data = conn.execute(stmt).fetchone()

    if not data:
        raise NoResultFound(f'Unable to sum the bike lane lenghts for {city}')
    
    return data[0]

def createDB() -> None:
    createTables()
    addCityData()
    BikeLaneGeoJsontoDB('London')
    BikeLaneGeoJsontoDB('Berlin')


