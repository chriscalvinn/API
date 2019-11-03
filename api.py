from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
import requests
import http.client

conn =  mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="dbase"
)

def isiDbase():
    cursor = conn.cursor()
    for i in range (137000, 137100):
    #melakukan pencarian sesuai range yang ditetapkan
        try :
            url = 'https://webpac.lib.itb.ac.id/index.php/marc/view/{}/JSON'.format(i)

            #memasukkan data JSON ke variabel data
            data = requests.get(url)
            data = json.loads(data.text)

            #mencari Judul (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'245') :
                    Judul = data[0]['fields'][j]['245']['subfields'][0]['a']
                    break
                else :
                    Judul = "null"
                    
            #mencari ISBN (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'020') :
                    ISBN = data[0]['fields'][j]['020']['subfields'][0]['a']
                    break
                else :
                    ISBN = "null"

            #mencari Penulis (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'100') :
                    Penulis = data[0]['fields'][j]['100']['subfields'][0]['a']
                    break
                else :
                    Penulis = "null"

            #mencari Penerbit dan Tahun Terbit (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'260') :
                    Penerbit = data[0]['fields'][j]['260']['subfields'][1]['b']
                    Tahun_terbit = data[0]['fields'][j]['260']['subfields'][2]['c']
                    break
                else :
                    Penerbit = "null"
                    Tahun_terbit = "null"

            #insert into database
            instance = (Judul, ISBN, Penulis, Penerbit, Tahun_terbit)
            query = """INSERT INTO book(
                Judul,
                ISBN,
                Penulis,
                Penerbit,
                Tahun_terbit
                )
                Values (%s,%s,%s,%s,%s)"""
            cursor.execute(query, instance)
            conn.commit()

        #menghandle exception
        except Exception as e:
            print(e)
            continue

    cursor.close()

class httphandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            cursor = conn.cursor()
            cursor.execute("select * from book")
            res = cursor.fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            result = []
            for row in res:
                data = {
                    'Judul': row[0],
                    'Penulis': row[1],
                    'Penerbit': row[2],
                    'ISBN': row[3],
                    'Tahun_terbit': row[4],
                    'Tersedia': row[5],
                    'Sedang_dipinjam': row[6],
                    'total': row[7],
                }
                result.append(data)
            data = json.dumps(result)
            self.wfile.write(bytes(data.encode('utf-8')))
            return
        except Exception as e:
            return e

port = 8080
with HTTPServer(("",port), httphandler) as httpd:
    print("serving at port ",port)
    httpd.serve_forever()
    isiDbase()
    mydb.close()
