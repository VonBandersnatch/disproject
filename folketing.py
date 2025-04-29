import requests
import json
import pandas as pd

response = requests.get("https://oda.ft.dk/api/Afstemning?$inlinecount=allpages")
afstemninger = response.json()

for afstemning in afstemninger['value']:
    print(afstemning)
