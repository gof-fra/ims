import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(id INTEGER PRIMARY KEY AUTOINCREMENT, nom text, email text, sexe text, contact text, date_debut text, date_fin text, password text, type text, address text, salaire text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS client(invoice INTEGER PRIMARY KEY AUTOINCREMENT, nom text, contact text, desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT, nom text)")
    con.commit()
                                                        
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, category text, client text, nom text, prix text, qty text, status)")
    con.commit()

create_db()