from encryption_functions import symmetric_enc
from encryption_functions import gen_symk
from encryption_functions import symmetric_dec
from encryption_functions import asymmetric_enc
from encryption_functions import asymmetric_dec
from encryption_functions import signMessage, verifySignature
import json
import ast
import os
from Crypto.Cipher import AES

class server:
    def __init__(self):
        self.databaseDecryptKey = open("keys/databaseKey.key","rb").read()
        self.privateKey_path = "keys/Server/server.pem"
        self.publicKey_path = "keys/Server/server_publick.pem"

    def decryptDatabase(self,database,signature):
        verification = verifySignature(database,signature,self.publicKey_path,datab = True)
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
        signature = signMessage(out,self.privateKey_path,database=True)
        return out,signature

    def sendInformation(self,data,publicKey_path):
        encryptedData = symmetric_enc(data)
        encryptedDataAsym = asymmetric_enc(encryptedData, publicKey_path)
        signature = signMessage(encryptedDataAsym,self.privateKey_path)
        return encryptedDataAsym,signature

    def searchInformation(self, dataEncryptedAsym,signature,pubkey_path): #Change everything
        #Function to search the information in the different databases, from an encrypted data.
        verification = verifySignature(dataEncryptedAsym,signature,pubkey_path)
        if verification == True:
            dataEncrypted = asymmetric_dec(dataEncryptedAsym,self.privateKey_path)
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
                        database = self.decryptDatabase(database,signature)
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
                        return serverOutput,verification
                    else:
                        if data[0] == "users":
                            return False, verification
                        else:
                            return -1, verification
        else:
            return -1,-1

                        

    def storeInformation(self, dataEncryptedAsym,signature,pubkey_path, existent):
        verification = verifySignature(dataEncryptedAsym,signature,pubkey_path)
        if verification == True:
            dataEncrypted = asymmetric_dec(dataEncryptedAsym,self.privateKey_path)
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
                        database = self.decryptDatabase(database,signature)
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
                                    return False
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
                            return False
                        database.update({data[1]: information})
                    with open(fileName,'w') as f:
                        if f == -1:
                            print("File could not be opened")
                            return False
                        else:
                            database,signature = self.encryptDatabase(database)
                            json.dump(database,f)
                            sigName = str(data[0])+ ".sig"
                            with open(sigName,'w') as g:
                                if g==-1:
                                    print("File could not be opened")
                                    return False
                                else:
                                    signature = str(signature)
                                    g.write(signature)
                            return True
        else:
            return -1

        
    def storeNewKey(self): 
        #Method for creating and storing a new key for encryption of databases
        #USE ONLY WHEN FIRST CREATING THE DATABASE OR WITH AN UPDATE ALL FILES METHOD
        newKey = gen_symk(16)
        with open("databaseKey.key","wb") as f:
            if f!=-1:
                f.write(newKey)
            else:
                print("File could not be opened")


    def deleteItem(self,dataEncryptedAsym,signature,pubkey_path):
        verification = verifySignature(dataEncryptedAsym,signature,pubkey_path)
        if verification:
            dataEncrypted = asymmetric_dec(dataEncryptedAsym, self.privateKey_path)
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
                            database = self.decryptDatabase(database,signature)
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
                                database,signature = self.encryptDatabase(database)
                                json.dump(database,f)
                                sigName = str(data[0])+ ".sig"
                                with open(sigName,'w') as g:
                                    if g==-1:
                                        print("File could not be opened")
                                        return False
                                    else:
                                        signature = str(signature).decode('utf-8')
                                        g.write(signature)
        else:
            print("Not able to verify the signature. Aborting operation")
            return -1
        