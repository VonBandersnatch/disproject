from database import db_connection

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
    for party in db_parties:
        parties.append(party[0]) # Bill(party[0])
    conn.close()
    print(parties)
    return parties

# result table
def list_bills():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT ps.parti, ps.stemme, s.titelkort, s.typeid, st.typeid, a.typeid, a.vedtaget FROM PartiStemmer ps JOIN Afstemning a ON ps.afstemningsid = a.id JOIN Sagstrin st ON a.sagstrinid = st.id JOIN Sag s ON st.sagid = s.id WHERE a.typeid=1 AND st.typeid=17 AND s.typeid=3;')
    rows = cur.fetchall()
    conn.close()

    bills = []
    for row in rows:
        bills.append(Bill(row[0], row[1], row[2]))
    
    return bills


