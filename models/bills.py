from database import db_connection
import re

class Bill:
    def __init__(self, parti, stemme, lovforslag):
        self.parti = parti
        self.stemme = stemme
        self.lovforslag = lovforslag

class Party:
    def __init__(self, parti):
        self.parti = parti
        

# drop down menu
def list_parties():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT parti FROM Partistemmer')
    db_parties = cur.fetchall()

    parties = []
    pattern = re.compile(r'^[A-Z]{1,3}$')
    for party in db_parties:
        if pattern.match(party[0]):
            if party[0] == 'LA':
                party = ('Liberal Alliance',)
            parties.append(Party(party[0]))
    conn.close()
    
    return parties

"""
# result table
def list_bills(parti=None, søgeord=""):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
    'SELECT ps.parti, ps.stemme, s.titelkort ' \
    'FROM PartiStemmer ps ' \
    'JOIN Afstemning a ON ps.afstemningsid = a.id ' \
    'JOIN Sagstrin st ON a.sagstrinid = st.id ' \
    'JOIN Sag s ON st.sagid = s.id ' \
    'WHERE a.typeid=1 AND st.typeid=17 AND s.typeid=3 AND ps.parti = %s', (parti,))

    rows = cur.fetchall()
    conn.close()

    bills = []
    for row in rows:
        bills.append(Bill(row[0], row[1], row[2]))


    bills_søgt = []  
    pattern = re.compile('.*{søgeord}.*') # OBS ikke raw string
    
    for i in bills:
        if pattern.match(i.lovforslag):
            bills_søgt.append(i)
    
    return bills_søgt
"""



def list_bills(parti=None, søgeord=""):
    conn = db_connection()
    cur = conn.cursor()

    base_query = (
        'SELECT ps.parti, ps.stemme, s.titelkort '
        'FROM PartiStemmer ps '
        'JOIN Afstemning a ON ps.afstemningsid = a.id '
        'JOIN Sagstrin st ON a.sagstrinid = st.id '
        'JOIN Sag s ON st.sagid = s.id '
        'WHERE a.typeid=1 AND st.typeid=17 AND s.typeid=3'
    )

    params = []
    if parti:
        base_query += ' AND ps.parti = %s'
        params.append(parti)

    cur.execute(base_query, params)
    rows = cur.fetchall()
    conn.close()

    bills = []
    for row in rows:
        bills.append(Bill(row[0], row[1], row[2]))

    # Regex søgning hvis søgeord givet
    if søgeord:
        pattern = re.compile(f".*{re.escape(søgeord)}.*")
        bills = [b for b in bills if pattern.search(b.lovforslag)]

    return bills
