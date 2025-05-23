import psycopg2
import os
import pandas as pd

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', 'disuser')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname='todo' user=" + user + " host=" + host + " password =" + password
    conn = psycopg2.connect(db)

    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, category_name TEXT NOT NULL UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, todo_text TEXT NOT NULL UNIQUE, category_id INTEGER NOT NULL, FOREIGN KEY(category_id) REFERENCES categories(id))''')
    cur.execute('''DROP TABLE IF EXISTS PartiStemmer ''') 
    cur.execute('''CREATE TABLE IF NOT EXISTS PartiStemmer (afstemningsid INTEGER, parti VARCHAR, stemme VARCHAR)''')
    cur.execute('''DROP TABLE IF EXISTS Afstemning ''') 
    cur.execute('''CREATE TABLE IF NOT EXISTS Afstemning (id INTEGER, konklusion VARCHAR, vedtaget INTEGER, kommentar VARCHAR, modeid INTEGER, typeid INTEGER, sagstrinid INTEGER, opdateringsdato TIMESTAMP)''')    
    cur.execute('''DROP TABLE IF EXISTS Sagstrin ''') 
    cur.execute('''CREATE TABLE IF NOT EXISTS Sagstrin (id INTEGER, sagid INTEGER, typeid INTEGER, opdateringsdato TIMESTAMP)''')    
    cur.execute('''DROP TABLE IF EXISTS Sag ''') 
    cur.execute('''CREATE TABLE IF NOT EXISTS Sag (id INTEGER, titelkort VARCHAR, opdateringsdato TIMESTAMP, typeid INTEGER)''')    

    conn.commit()

    categories = ['DIS', 'House chores']
    for category in categories:
        cur.execute('INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT DO NOTHING', (category,))

    todos = [('Assignment 1', 'DIS'), ('Groceries', 'House chores'), ('Assignment 2', 'DIS'), ('Project', 'DIS')]
    for (todo, category) in todos:
        cur.execute('INSERT INTO todos (todo_text, category_id) VALUES (%s, (SELECT id FROM categories WHERE category_name = %s)) ON CONFLICT DO NOTHING', (todo, category))

    df_PartiStemmer = pd.DataFrame()
    df_PartiStemmer = pd.read_csv("Partistemmer_v3.csv", index_col=False)
    df_PartiStemmer = df_PartiStemmer.drop(columns=['Unnamed: 0'])
    for index, row in df_PartiStemmer.iterrows():
        cur.execute("INSERT INTO PartiStemmer (afstemningsid, parti, stemme) VALUES (%s, %s, %s)", (row['afstemningsid'], row['parti'], row['stemme'])
                    )
    
    df_Afstemning = pd.DataFrame()
    df_Afstemning = pd.read_csv("Afstemning_data_v3.csv", index_col=False)
    #df_PartiStemmer = df_PartiStemmer.drop(columns=['Unnamed: 0'])
    for index, row in df_Afstemning.iterrows():
        cur.execute("INSERT INTO Afstemning (id, konklusion, vedtaget, kommentar, modeid, typeid, sagstrinid, opdateringsdato) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
                    )

    df_Sagstrin = pd.DataFrame()
    df_Sagstrin = pd.read_csv("Sagstrin_data_v3.csv", index_col=False)
    #df_PartiStemmer = df_PartiStemmer.drop(columns=['Unnamed: 0'])
    for index, row in df_Sagstrin.iterrows():
        cur.execute("INSERT INTO Sagstrin (id, sagid, typeid, opdateringsdato) VALUES (%s, %s, %s, %s)", (row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3])
                    )
    
    df_Sag = pd.DataFrame()
    df_Sag = pd.read_csv("Sag_data_v3.csv", index_col=False)
    #df_PartiStemmer = df_PartiStemmer.drop(columns=['Unnamed: 0'])
    for index, row in df_Sag.iterrows():
        cur.execute("INSERT INTO Sag (id, titelkort, opdateringsdato, typeid) VALUES (%s, %s, %s, %s)", (row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3])
                    )


    conn.commit()
    conn.close()
