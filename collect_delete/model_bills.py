from database import db_connection
import re

class Bill:
    def __init__(self, parti, stemme, lovforslag):
        self.parti = parti
        self.stemme = stemme
        self.lovforslag = lovforslag
        
# drop down menu
def list_parties():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT parti FROM Partistemmer')
    db_parties = cur.fetchall()
    
    parties = []
    pattern = re.compile(r"^([a-zA-Z]{1,3}\s*?)$")  # Regex for 1-3 letters followed by optional spaces at start of line, but where string does not continue afterwards.
    for party in db_parties:
        result = pattern.search(party[0])  # Returns true if regex matches 
        if result:  # Match objects evaluate to True
            parties.append(party[0]) # Bill(party[0])
    conn.close()
    # print(parties)
    return parties
    #return db_parties

# result table
def list_bills(parti):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT ps.parti, ps.stemme, s.titelkort FROM PartiStemmer ps JOIN Afstemning a ON ps.afstemningsid = a.id JOIN Sagstrin st ON a.sagstrinid = st.id JOIN Sag s ON st.sagid = s.id WHERE a.typeid=1 AND st.typeid=17 AND s.typeid=3 AND ps.parti = %s', (parti,))
    rows = cur.fetchall()
    conn.close()
    bills = []
    for row in rows:
        bills.append(Bill(row[0], row[1], row[2]))
    return bills


