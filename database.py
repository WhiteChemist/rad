import psycopg2

def getHosts():
    connection_db = psycopg2.connect(dbname='radius',user='rocketdata',password='AwTq7F3xFhFLnuhyUpsZ4Z',host='192.168.77.235',port=5435)
    cursor = connection_db.cursor()
    cursor.execute('SELECT nasname, shortname, secret FROM public.nas')
    result = cursor.fetchall()
    cursor.close()
    connection_db.close()
    return result

def validateNas(nas_identifier, nas_ip_address,secret):
    connection_db = psycopg2.connect(dbname='radius',user='rocketdata',password='AwTq7F3xFhFLnuhyUpsZ4Z',host='192.168.77.235',port=5435)
    cursor = connection_db.cursor()
    cursor.execute('SELECT nasname, shortname, secret FROM public.nas WHERE nasname={0} AND shortname={1} AND secret={2}'.format(nas_ip_address,nas_identifier,secret))
    result = cursor.fetchone()
    cursor.close()
    connection_db.close()
    return True if result.count>0 else False
    

