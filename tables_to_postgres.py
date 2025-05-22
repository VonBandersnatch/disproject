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
filename = os.path.join('data','Partistemmer.csv')

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
    cursor.execute('''CREATE TABLE IF NOT EXISTS afstemning (afstemningsid INT, parti TEXT, forimod TEXT)''')
    conn.commit()

    cursor.execute("INSERT INTO afstemning (afstemningsid, parti, forimod) VALUES (4, 'V', 'Imod')")
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO afstemning (afstemningsid, parti, forimod) VALUES (%s, %s, %s)",(row['Afstemningsid'],row['Parti'], row['For/imod/hverken']))

    conn.commit()
    conn.close()

init_db()
