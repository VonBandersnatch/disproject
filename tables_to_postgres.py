from sqlalchemy import create_engine
import psycopg2
import os
import pandas as pd
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '1763')
host = os.environ.get('HOST', '127.0.0.1')
defaultdbname = 'postgres'
ftdbname = 'ft'
filename = os.path.join('data','afstemning_data_v3.csv')

def db_connection(name):
    conn = psycopg2.connect(host = host, user = user, password = password, database = name)
    return conn

def init_db():
    # connect to default database, necessary to create a new database
    conn = db_connection(defaultdbname)
    # Required for CREATE DATABASE command
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    
    try:
        cursor.execute("CREATE DATABASE "+ftdbname)
        print(f"Database '{ftdbname}' created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{ftdbname}' already exists")
    cursor.close()
    conn.close()

    # connect to the database we really want.
    conn = db_connection(ftdbname)
    cursor = conn.cursor()

    df = pd.read_csv(filename)
    cursor.execute('''DROP TABLE IF EXISTS PartiStemmer''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS PartiStemmer (afstemningsid INT, parti TEXT, stemme TEXT)''')
    cursor.execute('''DROP TABLE IF EXISTS Afstemning''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Afstemning (id INT, konklusion STRING, vedtaget BOOLEAN, kommentar STRING, modeid INT, typeid INT, sagstrinid INT, opdateringsdato DATETIME)''')    
    cursor.execute('''DROP TABLE IF EXISTS Sagstrin''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sagstrin (id INT, sagid INT, typeid INT, opdateringsdato DATETIME)''')    
    cursor.execute('''DROP TABLE IF EXISTS Sag''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sag (id INT, titelkort STRING, opdateringsdato DATETIME, typeid INT)''')    
    conn.commit()

    df_PartiStemmer = pd.read_csv("data.csv")
# Insert data into PostgreSQL
    df_PartiStemmer.to_sql("PartiStemmer", con=conn, if_exists="replace", index=False)
    df_Afstemning.to_sql("Afstemning", con=conn, if_exists="replace", index=False)
    df_Sagstrin.to_sql("Sagstrin", con=conn, if_exists="replace", index=False)
    df_Sag.to_sql("Sag", con=conn, if_exists="replace", index=False)



"""

# Load the CSV data

# Define the PostgreSQL connection URI
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)


    for index, row in df.iterrows():
        cursor.execute("INSERT INTO afstemning (afstemningsid, parti, forimod) VALUES (%s, %s, %s)",(row['Afstemningsid'],row['Parti'], row['For/imod/hverken']))

"""

    conn.commit()
    conn.close()

init_db()
