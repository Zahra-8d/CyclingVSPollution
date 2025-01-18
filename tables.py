from sqlalchemy import Table, Column, MetaData, Identity, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, FLOAT
from geoalchemy2 import Geometry

metadata = MetaData()

City = Table(
    'City',
    metadata,
    Column('ID', INTEGER, Identity(always=True), primary_key=True),
    Column('Name', TEXT, nullable=False)
) 

BikeLane = Table(
    'BikeLane',
    metadata,
    Column('ID', INTEGER, Identity(always=True), primary_key=True),
    Column('CityID', INTEGER, ForeignKey('City.ID'), index=True),
    Column('Geom', Geometry('GEOMETRY'), nullable=False),
    Column('Lenght', FLOAT, nullable=False)
)

#TODO - create pollution table - data needed to know what columns to create

# Pollution = Table(
#     'Pollution',
#     metadata,
#     Column('ID', INTEGER, Identity(always=True), primary_key=True),
#     Column('CItyID', INTEGER, ForeignKey('City.ID'), index=True),
#     Column('Coordinates', ARRAY(FLOAT, dimensions=2), nullable=False),
#     Column('Level', FLOAT, nullable=False)
# )
#
