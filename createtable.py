from condb import create_connection

conn = create_connection()
cursor = conn.cursor()


cursor.execute(''' 
    CREATE TABLE belanja 
    (no_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nama_item CHAR(100), 
    jumlah_item INT,
    harga REAL,
    total_harga REAL,
    diskon INT,
    harga_diskon REAL)
''')

conn.commit()