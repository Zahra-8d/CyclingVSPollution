from sqlalchemy import create_engine, URL

_engine_url = URL.create(drivername='postgresql',
                         username='postgres',
                         password='00000000',
                         host='localhost',
                         port=5432,
                         database='sdb25')

engine = create_engine(_engine_url,
                       echo=True,
                       plugins=['geoalchemy2'])

if __name__ == '__main__':
    with engine.connect() as conn:
        print('Connection succesful')