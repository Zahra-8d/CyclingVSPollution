from sqlalchemy import Table, Column, MetaData, Identity, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, FLOAT
from geoalchemy2 import Geometry

metadata = MetaData()

City = Table(
    'City',
    metadata,
    Column('ID', INTEGER, Identity(always=True), primary_key=True),
    Column('Name', TEXT, nullable=False),
    Column('Population', INTEGER, nullable=False),
    Column('Area', INTEGER, nullable=False, comment='km2')
) 

BikeLane = Table(
    'BikeLane',
    metadata,
    Column('ID', INTEGER, Identity(always=True), primary_key=True),
    Column('CityID', INTEGER, ForeignKey('City.ID'), index=True),
    Column('Geom', Geometry('GEOMETRY'), nullable=False),
    Column('Lenght', FLOAT, nullable=False, comment='m')
)

Pollution = Table(
    'Pollution',
    metadata,
    Column('ID', INTEGER, Identity(always=True), primary_key=True),
    Column('CityID', INTEGER, ForeignKey('City.ID'), index=True),
    Column('Name', TEXT, nullable=True),
    Column('Geom', Geometry('GEOMETRY'), nullable=False),
    Column('NO2', FLOAT, nullable=True, comment='µg/m3')
)

