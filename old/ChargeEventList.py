
import sqlite3

conn = sqlite3.connect('EventList.sqlite3')
cur = conn.cursor()

fhand = open('doc/EventList.csv')

for line in fhand:
    valores = line.split(';')
    if valores[2][:2] == 'SE':
        cur.execute('INSERT INTO EventList (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2][:2]))
    else:
        cur.execute('INSERT INTO EventList (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2]))

conn.commit()
cur.close()
