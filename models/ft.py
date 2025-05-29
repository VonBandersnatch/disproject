from database import db_connection
import re

class Bill:
    def __init__(self, parti, stemme, lovforslag):
        self.parti = parti
        self.stemme = stemme
        self.lovforslag = lovforslag

def list_parties():
    #drop down menu
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT parti FROM Partistemmer")
    db_parties = cur.fetchall()

    parties = []
    pattern = re.compile(r"^([a-zA-Z]{1,3}\s*?)$")
    for parti in db_parties:
        result = pattern.search(parti[0])
        if result:  
            parties.append((parti[0],parti[0]))
    conn.close()
    return parties

def list_bills(party_chosen, subject):
    conn = db_connection()
    cur = conn.cursor()
    query = """SELECT ps.parti, ps.stemme, s.titelkort FROM PartiStemmer ps JOIN Afstemning a ON ps.afstemningsid=a.id 
                JOIN Sagstrin st ON a.sagstrinid = st.id JOIN Sag s ON st.sagid=s.id
                WHERE a.typeid=1 AND st.typeid=17 AND s.typeid=3"""
    if party_chosen != "":
        query += " AND ps.parti="+"'"+party_chosen+"'"
    if subject != "":
        query += " AND s.titelkort LIKE '%" + subject + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    bills = []
    for row in rows:
        bills.append(Bill(row[0], row[1], row[2]))

    return bills
