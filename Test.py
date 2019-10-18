import pymysql
from flaskext.mysql import MySQL
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'DBase'

mysql = MySQL(app)
#definisikan cursor untuk manipulasi database
conn = mysql.connect()
cur = conn.cursor()

url = 'https://webpac.lib.itb.ac.id/index.php/marc/view/137491/JSON'


def checkKey(dict, key):
#mengembalikan true jika key ada di dictionary dan false jika tidak
    if key in dict: 
        return True
    else: 
        return False

def isiDbase():
    for i in range (137000, 137100):
    #melakukan pencarian sesuai range yang ditetapkan
        try :
            url = 'https://webpac.lib.itb.ac.id/index.php/marc/view/{}/JSON'.format(i)
            print(url)

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
            #insert into database
            if (not(Judul == "null")):
                cur.execute("INSERT INTO book(Judul) Values (%s)")

            #mencari ISBN (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'020') :
                    ISBN = data[0]['fields'][j]['020']['subfields'][0]['a']
                    break
                else :
                    ISBN = "null"

            #insert into database
            if (not(ISBN == "null")):
                cur.execute("INSERT INTO book(ISBN) Values (%s)")

            #mencari Penulis (Jika tidak ada diberi nilai null)
            for j in range (0, len(data[0]['fields'])):
                if checkKey(data[0]['fields'][j],'100') :
                    Penulis = data[0]['fields'][j]['100']['subfields'][0]['a']
                    break
                else :
                    Penulis = "null"

            #insert into database
            if (not(Penulis == "null")):
                cur.execute("INSERT INTO book(Penulis) Values (%s)")

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
            if (not(Penerbit == "null")):
                cur.execute("INSERT INTO book(Penerbit) Values (%s)")
            #insert into database
            if (not(Tahun_terbit == "null")):
                cur.execute("INSERT INTO book(Tahun_terbit) Values (%s)")

        #menghandle exception
        except :
            continue

class index(Resource):
    def get(self):
        cur.execute("select * from book")
        return {'book': [i[0] for i in query.cursor.fetchall()]}


api.add_resource(index, '/index')

if __name__ == '__main__':
    #mengisi database
    isiDbase()

    app.run(port='5000')
