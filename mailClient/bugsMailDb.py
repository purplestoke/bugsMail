import sqlite3
from keys import *
from cryptography.hazmat.primitives import serialization

# CREATES DATABASE
def createDB():
    try:
        conn = sqlite3.connect('bugsMailDb.sqlite3')
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON;')
        cur.executescript("""
            DROP TABLE IF EXISTS DummyMail;
            DROP TABLE IF EXISTS User;

            CREATE TABLE User (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            privkey BLOB,
            pubkey BLOB,
            email TEXT
            );

            CREATE TABLE DummyMail (
            user_id INTEGER,
            signature TEXT,
            hash TEXT,
            service TEXT,
            email TEXT,
            FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        return "Success"
    except sqlite3.Error as e:
        return f"DB Error {e}"
    finally: conn.close()

# ESTABLISH CONN AND CUR TO DB
def connDB():
    conn = sqlite3.connect('bugsMailDb.sqlite3')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
    return conn, cur

# ADD A USER
def insertUser(username):
    conn, cur = connDB()
    try:
        # GENERATE PRIVATE AND PUBLIC KEY
        privPem, pubPem =  genKeys()
        # GENERATE BASE EMAIL FROM USERNAME AND PUBLIC KEY
        baseAddr = username + "@thebugshub.com"
        # INSERT INFO INTO USER TABLE
        cur.execute('INSERT INTO User (username, privkey, pubkey, email) VALUES (?, ?, ?, ?)', (username, privPem, pubPem, baseAddr))
        conn.commit()
        return "Tables updated and key's generated!"
    except sqlite3.Error as e:
        return f"Failed to generate key pair for user {e}"
    finally:
        conn.close()

# GENERATE A DUMMY EMAIL AND SAVE TO DB
def genDummyEmail(username, service):
    conn, cur = connDB()
    # PULLING USER ID
    try:
        pullId = cur.execute('SELECT id FROM User WHERE username = ?', (username,))
        userId = pullId.fetchone()[0]
    except sqlite3.Error as e:
        return f"User not found {e}"
    # PULLING USER PRIVATE KEY
    try:
        pull = cur.execute('SELECT privkey FROM User WHERE id = ?', (userId,))
        ret = pull.fetchone()[0]
    except sqlite3.Error as e:
        return f'Error {e}'
    # GENERATE A DUMMY EMAIL
    privKey = serialization.load_pem_private_key(
        ret,
        password=None,
    )
    sig = signMessage(service, privKey)
    hsh, dummyAddr = sigToAddr(sig, service)
    # INSERT NEW PUBLIC KEY AND DUMMY EMAIL INTO DummyEmail TABLE
    try:
        cur.execute('INSERT INTO DummyMail (user_id, signature, hash, service, email) VALUES (?, ?, ?, ?, ?)', (userId, sig, hsh, service, dummyAddr,))
        conn.commit()
        return f"Success in generating {dummyAddr} email"
    except sqlite3.Error as e:
        return f"Error inserting pub key and dummy email into table {e}"
    finally: conn.close()

# RECREATE DUMMY EMAIL
toAddr = "BestBuy8a3d9bbdb6@thebugshub.com"
def recreateDummy(toAddr):
    


if __name__ == "__main__":
    pass
