from encodings import utf_8
from flask import Flask,render_template,request,jsonify,redirect, url_for,Response,stream_with_context
import json
import pandas as pd
from flask import make_response
import os


import ast

import rsa


import sys
import logging
import traceback
from logging.config import dictConfig

version = '0.0.2'
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app():
  app = Flask(__name__)
  return app

app = create_app()

def __init__():
    #generate key and env variables
    os.environ["PBK_PATH"]                = "PEM/pbk.pem"
    os.environ["PVK_PATH"]                = "PEM/pvk.pem"
    os.environ["ENCRYPTED_FILE_PATH"]     = "Model/encryption.bin"
    os.environ["Login"]                   = ""
    # generateKey()    #LANCER QUE LA PREMIERE FOIS

#FUNCTIONS APP ROUTE -----------------------------------------------------------

@app.route("/")
def hello():
    return 'Hello, World!'

@app.route("/auth")#mapping de test
def auth():
    data = [{'login': 'paul', 'pwd': '123'}, {'login': 'paulo', 'pwd': '123'}]
    # data = json.loads(decrypt(os.getenv("ENCRYPTED_FILE_PATH")))


    data = pd.DataFrame(data,columns=["login","pwd"],index=[0]) if (len(data)<=1)  else pd.DataFrame(data,columns=["login","pwd"])
    data = data.to_dict(orient = 'records')
    print(data)
    de = {"status":"test",
            "data":data}
    response = jsonify(de)
    return makeRequestHeaders(response)


@app.route("/allUser")
def getAllUser():
    # addRootTry()
    data,status = getBDD()
    data = data.to_dict(orient = 'records')
    de = {"status":status,
            "data":data}
    response = jsonify(de)
    return makeRequestHeaders(response)


@app.route("/authentification",methods=['POST','GET'])
def authentification(login=None,pwd=None):
    if(login!= None and pwd != None):
        login = login
        pwd = pwd
    else:
        if(request.method == "GET"):
            login = request.args.get("login")
            pwd = request.args.get("pwd")
        else:
            json_data = json.loads(request.get_json())
            login =None
            pwd = None
            if json_data:
                if 'login' in json_data:
                    login = json_data['login']

                if 'pwd' in json_data:
                    pwd = json_data['pwd']

    print("login : ",login," pwd : ",pwd)
    data,status = getBDD()
    print("Data authentification after getBDD() : ",data)
    if(status != "error"):
        data = data[data['login']==login]
    
        if(data.empty):
            data = False
            status = "Mauvais Login"
        else:
            data = data[data['pwd']==pwd]
            if(data.empty):
                data = False
                status = "Mauvais Pwd"
            else:
                data = True
                #On enregistre le login actuel dans l'env
                os.environ["Login"] = login
    else:
        data = True
        #On enregistre le login actuel dans l'env
        os.environ["Login"] = login

    de = {"status":status,
            "data":data}
    print("de : ",de)
    # if(login!= None and pwd != None):
    #     return de["status"]
    response = jsonify(de)
    return makeRequestHeaders(response)

@app.route("/isAuth")
def isAuth():
    if(os.getenv("Login")==""):
        data = False
        status="error"
    else:
        data = os.getenv("Login")
        status = "OK"
    de = {"status":status,
            "data":data}
    response = jsonify(de)
    return makeRequestHeaders(response)

@app.route("/addUser",methods=['GET','POST'])
def addUser():
    if(request.method == "GET"):
        login = request.args.get("login")
        pwd=request.args.get("pwd")
    else:
        json_data = json.loads(request.get_json())
        login =None
        pwd = None
        if json_data:
            if 'login' in json_data:
                login = json_data['login']

            if 'pwd' in json_data:
                pwd = json_data['pwd']

    print("login : ",login," pwd : ",pwd)
    msg = authentification(login,pwd)
    print("auth login & pwd = ",login,pwd)
    status=json.loads(msg.data)["status"]

    print("MSG status : ",status)
    print("try : ",status=="Mauvais Login")
    data=None
    if(status=="OK" or status=="Mauvais Pwd"):
        data = False
        status = "User deja existant"

    elif(status=="error" or status=="Mauvais Login"):
        json_data = []
        json_d = {'login':login,'pwd':pwd}
        
        json_data.append(json_d)
        print("Json_data ",json_data)

        print("dans le elif")
        d,s = getBDD()
        if(s=="OK"):
            print("dans le OK")
            d = json.loads(d.to_json(orient="records"))
            for elem in d:
                json_data.append(elem)
            data=True
            status=s
        else:
            status = "dataBaseVide"
            data = True
        print("json data", json.dumps(json_data))
        encrypt(json.dumps(json_data),os.getenv("ENCRYPTED_FILE_PATH"))
    de = {"status":status,
            "data":data}
    print(de)
    response = jsonify(de)
    return makeRequestHeaders(response)

    
#--------------------------------------------------------------------------------


#FUNCTIONS GET ADD REMOVE -------------------------------------------------------
def addRootTry():
    j = {'login':"root",'pwd':"root"}
    encrypt(json.dumps(j),os.getenv("ENCRYPTED_FILE_PATH"))

def getBDD():
    try:
        data = json.loads(decrypt(os.getenv("ENCRYPTED_FILE_PATH")))
        status = "OK"
        print(data)
        data = pd.DataFrame(data,columns=["login","pwd"],index=[0]) if (len(data)<=1)  else pd.DataFrame(data,columns=["login","pwd"])
        print("dataframe data : ",data)
    except:
        data = False
        status = "error"
        print(data)

    
    return data,status
#--------------------------------------------------------------------------------


#FUNCTIONS RSA-------------------------------------------------------------------
def generateKey():
    # Use at least 2048 bit keys nowadays, see e.g. https://www.keylength.com/en/4/
    publicKey, privateKey = rsa.newkeys(2048) 

    # Export public key in PKCS#1 format, PEM encoded 
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 
    # print(publicKeyPkcs1PEM)
    
    # Export private key in PKCS#1 format, PEM encoded 
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8') 
    # print(privateKeyPkcs1PEM)
    

    # Save and load the PEM encoded keys as you like
    save_pem(publicKeyPkcs1PEM,os.getenv("PBK_PATH"))
    save_pem(privateKeyPkcs1PEM,os.getenv("PVK_PATH"))

def encrypt(msg,path):
    # Import public key in PKCS#1 format, PEM encoded 
    publicKeyReloaded = rsa.PublicKey.load_pkcs1(open_pem(os.getenv("PBK_PATH")).encode('utf8')) 
    plaintext = msg.encode('ascii')
    ciphertext = rsa.encrypt(plaintext, publicKeyReloaded)
    # print("Ciphertext: ", ciphertext)
    # print(type(ciphertext)) # ensure it is string representation

    with open(path, "wb") as f:
        f.write(ciphertext)

def decrypt(path):
    # Import private key in PKCS#1 format, PEM encoded 
    privateKeyReloaded = rsa.PrivateKey.load_pkcs1(open_pem(os.getenv("PVK_PATH")).encode('utf8')) 
    with open(path,"rb") as f:
        ciphertext = f.read()
    # print(ciphertext)
    try:
        decryptedMessage = rsa.decrypt(ciphertext, privateKeyReloaded)
        # print("Decrypted message: ", decryptedMessage)
        return decryptedMessage

    except:
        print("Error during rsa.decrypt")
        return False
    


def test2():



    # Import public key in PKCS#1 format, PEM encoded 
    publicKeyReloaded = rsa.PublicKey.load_pkcs1(open_pem("PEM/pbk.pem").encode('utf8')) 
    # Import private key in PKCS#1 format, PEM encoded 
    privateKeyReloaded = rsa.PrivateKey.load_pkcs1(open_pem("PEM/pvk.pem").encode('utf8')) 

    plaintext = "coucou je m'appelle paul !!".encode('ascii')
    print("Plaintext: ", plaintext)

    ciphertext = rsa.encrypt(plaintext, publicKeyReloaded)
    print("Ciphertext: ", ciphertext)
    
    decryptedMessage = rsa.decrypt(ciphertext, privateKeyReloaded)
    print("Decrypted message: ", decryptedMessage)


def save_pem(key, path=None):
        if not path:
            raise ValueError("Path has to be specified")

        if not key:
            raise ValueError("key need to be not empty")
        
        print("PEM WRITEEE")
        with open(path, "w") as fd:
            fd.write(key) 

def open_pem( path=None):
        if not path:
            raise ValueError("Path has to be specified")

        
        print('PEM OPENNNN')
        res=""
        with open(path, "r") as fd:
            res+=fd.read() 
        return res

#--------------------------------------------------------------------------------

#AUTHER FUNCTIONS ---------------------------------------------------------------
def makeRequestHeaders(response):
    try:
      myUrl = request.environ['HTTP_ORIGIN']
    except KeyError:
      print("KeyError lol")
      myUrl = '*'
    response.headers.add('Access-Control-Allow-Origin',myUrl)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Content-type','application/json')
    response.headers.add('charset','utf8')
    return response
#--------------------------------------------------------------------------------


if __name__ == "__main__":
    # __init__()
    app.run(debug=True,host='0.0.0.0',port=5050)