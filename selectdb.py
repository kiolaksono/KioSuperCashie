from condb import create_connection

conn = create_connection()
cursor = conn.cursor()

cursor.execute('SELECT * FROM belanja')

result = cursor.fetchall()
for row in result:
    print(row)

