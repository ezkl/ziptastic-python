import redis
import csv
import sqlite3

conn = sqlite3.connect("zipcodes.db")
c = conn.cursor()

c.execute('''create table if not exists zipcodes (id integer primary key, zipcode integer, city text, state text, country text)''')


zipAdapter = csv.reader(open('free-zipcode-database.csv', 'rb'), delimiter=",", quotechar="'")
for row in zipAdapter:
    #insert_string = '''insert into zipcodes values(NULL, {0}, '{1}', '{2}', '{3}')'''.format(row[1].strip('"'), 
    #	                                                                           row[3].strip('"'), 
    #	                                                                           row[4].strip('"'), 
    #	                                                                           row[12].strip('"'))
    #print insert_string

    try:

        c.execute('''insert into zipcodes values(NULL, ?, ?, ?, ?)''',(row[1].strip('"'), 
    	                                                                           row[3].strip('"'), 
    	                                                                           row[4].strip('"'), 
    	                                                                           row[12].strip('"')))
    except Exception as e:
    	print e.message
    	break
    conn.commit()


	#print row[12].strip('"')
	#print row[1].strip('"')
	
	#print row[3].strip('"')
	#print row[4].strip('"')

r = redis.Redis(host='localhost', port=6379, db=0)
results = c.execute('select DISTINCT(zipcode), city, state, country from zipcodes')

for result in results:
    data = dict(zip(('country', 'state', 'city'), (result[3], result[2], result[1])))
    key = "zip:" + str(result[0])
    r.hmset(key, data)    

c.close()