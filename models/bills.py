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

class Vote:
    def __init__(self, stemme):
        self.stemme = stemme
        

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
            parties.append(Party(party[0]))
    conn.close()
    
    return parties

def party_vote():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT stemme FROM Partistemmer')
    db_stemme = cur.fetchall()

    stemme_liste = []
    for s in db_stemme:
        stemme_liste.append(Vote(s[0]))
    conn.close()
    
    return stemme_liste

def list_bills(parti=None, søgeord="", vote=""):
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

    if vote:
        base_query += ' AND ps.stemme = %s'
        params.append(vote)

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
