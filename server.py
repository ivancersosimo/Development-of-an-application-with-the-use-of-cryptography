from encryption_functions import symmetric_enc
from encryption_functions import gen_symk
from encryption_functions import symmetric_dec
import json
import ast
import os
from Crypto.Cipher import AES

class server:
    def __init__(self):
        self.databaseDecryptKey = open("databaseKey.key","rb").read()

    def decryptDatabase(self,database):
        ciphertext = ast.literal_eval(database.get("ciphertext"))
        tag = ast.literal_eval(database.get("tag"))
        nonce = ast.literal_eval(database.get("nonce"))
        cipher = AES.new(self.databaseDecryptKey,AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext,tag).decode("utf-8")
        data = ast.literal_eval(data)
        return data

    def encryptDatabase(self,database):
        cipher = AES.new(self.databaseDecryptKey, AES.MODE_EAX)
        database = str(database).encode("utf-8")
        ciphertext, tag = cipher.encrypt_and_digest(database)
        nonce = cipher.nonce
        out = {"ciphertext":str(ciphertext),"tag":str(tag),"nonce":str(cipher.nonce)}
        return out

    def sendInformation(self,data):
        encryptedData = symmetric_enc(data)
        return encryptedData

    def searchInformation(self, dataEncrypted): #Change everything
        #Function to search the information in the different databases, from an encrypted data.
        data = symmetric_dec(dataEncrypted)
        fileName = str(data[0])+ ".json"
        if not os.path.exists(fileName):
            print("File could not be found")
        else:
            with open(fileName,'rb') as f:
                try:
                    err=False
                    database = json.load(f)
                except ValueError:
                    err = True
                    database = {}
                    pass
                if err== False:
                    database = self.decryptDatabase(database)
                #database = self.decryptDatabase(database)
                f.close()
                serverOutput = database.get(data[1])
                if serverOutput:
                    if data[0] == "users":
                        if data[2][0] == serverOutput[0]:
                            if data[2][1] == serverOutput[1]:
                                serverOutput= True
                            else:
                                serverOutput = "BADKEY"
                        else:
                            serverOutput = False
                    return serverOutput
                else:
                    if data[0] == "users":
                        return False
                    else:
                        return -1
                        

    def storeInformation(self, dataEncrypted, existent):
        data = symmetric_dec(dataEncrypted)
        fileName = str(data[0])+ ".json"
        if not os.path.exists(fileName):
            os.mknod(fileName)
        with open(fileName,'rb') as f:
            if f == -1:
                print("File could not be opened") 
            else:
                try:
                    err=False
                    database = json.load(f)
                except ValueError:
                    err = True
                    database = {}
                    pass
                if err== False:
                    database = self.decryptDatabase(database)
                f.close()
                if existent == False: 
                    if str(data[0])!="users":
                        information = database.get(data[1])
                        if information:
                            found = False
                            for i in range(len(information)):
                                if information[i][0] == data[2][0]:
                                    found = True
                            if found == False:
                                information.append(data[2])
                            else:
                                print('Already existent user, choose update option')
                        else:
                            information = [data[2]]
                        database.update({data[1]: information})
                    else:
                        database.update({data[1]:data[2]})
                elif existent == True:
                    information = database.get(data[1])
                    found = False
                    if information:
                        for i in range(len(information)):
                            if information[i][0] == data[2][0]:
                                information[i][1] = data[2][1]
                                found = True
                    if found == False:
                        print("Couldn't update an existent User")
                    database.update({data[1]: information})
                with open(fileName,'w') as f:
                    if f == -1:
                        print("File could not be opened")
                    else:
                        database = self.encryptDatabase(database)
                        json.dump(database,f)

        
    def storeNewKey(self): 
        #Method for creating and storing a new key for encryption of databases
        #USE ONLY WHEN FIRST CREATING THE DATABASE OR WITH AN UPDATE ALL FILES METHOD
        newKey = gen_symk(16)
        with open("databaseKey.key","wb") as f:
            if f!=-1:
                f.write(newKey)
            else:
                print("File could not be opened")


    def deleteItem(self,dataEncrypted, all=False):
        data = symmetric_dec(dataEncrypted)
        fileName = str(data[0])+ ".json"
        if os.path.exists(fileName):
            with open(fileName,'rb') as f:
                if f == -1:
                    print("File could not be opened")
                else:
                    try:
                        err=False
                        database = json.load(f)
                    except ValueError:
                        err = True
                        database = {}
                        pass
                    if err== False:
                        database = self.decryptDatabase(database)
                    f.close()
                    information = database.get(data[1])
                    if information:
                        try:
                            information.remove([data[2][0],data[2][1]])
                            database.update({data[1]: information})
                        except ValueError:
                            print("Wrong combination user/password")
                            pass
                    with open(fileName,'w') as f:
                        if f == -1:
                            print("File could not be opened")
                        else:
                            database = self.encryptDatabase(database)
                            json.dump(database,f)

        