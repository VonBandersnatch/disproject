import requests
import json
import pandas as pd

def gettable(name:str):
    response = requests.get("https://oda.ft.dk/api/"+name+"?$inlinecount=allpages")
    data = response.json()
    df=pd.DataFrame(data['value'])
    df.to_csv(name+'.csv')
    
tables = ['Afstemning', 'Afstemningstype','Møde','Sagstrin','Sag']

for table in tables:
    gettable(table)