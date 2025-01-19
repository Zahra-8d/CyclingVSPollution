# Cycling VS Pollution
## Comparative study of Cycling Infrastructure and Pollution levels in Berlin and London

### Installation

  ```
  python pip install requirements.txt
  ```

### Run

  ```
  streamlit run app.py
  ```

### Create Database

  ```
  1. Create a database in your local PostgreSQL Server with PgAdmin4 and install postgis and postgis_raster extensions in the database.

  2. edit the engine create function in engine.py as such: 
  
  _engine_url = URL.create(drivername='postgresql',
                           username=<your username>,
                           password=<your password>,
                           host=<host>,
                           port=<port>,
                           database=<name of database where you want your data to be stored>)

  (all needed data can be found in PgAdmin4 -> right click on the
  server dropdown (usually PostgreSQL <version>) -> Connection)

  3. in db_utils.py run:
      createDB()
  ```
