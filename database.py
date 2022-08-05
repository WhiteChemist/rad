import psycopg2

def getHosts():
    connection_db = psycopg2.connect(dbname='radius',user='rocketdata',password='AwTq7F3xFhFLnuhyUpsZ4Z',host='192.168.77.235',port=5435)
    cursor = connection_db.cursor()
    cursor.execute('SELECT nasname, shortname, secret FROM public.nas')
    result = cursor.fetchall()
    return result

getHosts()