from skeleton_simmetric import symmetric_enc
from skeleton_simmetric import gen_symk
from skeleton_simmetric import symmetric_dec
import json
class server:
    def __init__(self):
        self.databaseDecryptKey = open("databaseKey.key","rb").open()

    def sendInformation(self,data):
        encryptedData = symmetric_enc(data)
        hashData = hash(data)
        serverOutput = []
        serverOutput.append(encryptedData)
        serverOutput.append(hashData)
        return serverOutput

    def searchInformation(self, dataEncrypted):
        #Function to search the information in the different databases, from an encrypted data.
        data = symmetric_dec(dataEncrypted)
        fileName = data[0] + ".json"
        with open(fileName,'rb') as f:
            if f == -1:
                print("File could not be opened")
            else:
                database = json.load(f)
                f.close()
                serverOutput = database.get(data[1])
                if serverOutput:
                    if data[0] == "users":
                        if data[2] == serverOutput:
                            serverOutput = True
                    return serverOutput
                else:
                    if data[0] == "users":
                        return False
                    else:
                        return -1
                        

    def storeInformation(self, data, existent):
        fileName = data[0] + ".json"
        with open(fileName,'rb') as f:
            if f == -1:
                print("File could not be opened") 
            else:
                database = json.load(f)
                f.close()
                database.update({data[1]:data[2]})
                with open(fileName,'wb') as f:
                    if f == -1:
                        print("File could not be opened")
                    else:
                        f.write(database)

        
    def storeNewKey(self): 
        #Method for creating and storing a new key for encryption of databases
        #USE ONLY WHEN FIRST CREATING THE DATABASE OR WITH AN UPDATE ALL FILES METHOD
        newKey = gen_symk(16)
        with open("databaseKey.key","wb") as f:
            if f!=-1:
                f.write(newKey)
            else:
                print("File could not be opened")

