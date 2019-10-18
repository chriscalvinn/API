import requests
import json

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

        #menghandle exception
        except :
            print()
  
        print(Judul)
        print(ISBN)
        print(Penulis)
        print(Penerbit)
        print(Tahun_terbit)
