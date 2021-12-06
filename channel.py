import ast
class channel:
    def __init__(self, server, client, pki, client2Username = None):
        self.server = server
        self.client = client
        self.clientReceiverUsername = client2Username
        self.pki = pki

    def clientToServer(self,data):
        pubkey_path = self.pki.retrieve_key("Server")
        clientOutput,signature = self.client.askInformation(data,pubkey_path)
        return clientOutput,signature

    def serverToClient(self, data):
        pubkey_path = self.pki.retrieve_key(self.client.username)
        serverOutput,signature = self.server.sendInformation(data,pubkey_path)
        return serverOutput,signature

    def checkUserExistance(self):
        data = self.client.checkUser()
        serverInput,signature = self.clientToServer(data)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        login,verification = self.server.searchInformation(serverInput,signature,pubkey_path)
        if verification==True:
            self.client.setExistance(login)
            return login
        else:
            return -1

    def addUser(self):
        clientInformation = self.client.checkUser()
        serverInput,signature = self.clientToServer(clientInformation)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        output = self.server.storeInformation(serverInput,signature,pubkey_path, existent = False)
        if output == -1:
            print ("Not able to verify the signature. Aborting operation")
        elif output == True:
            self.client.setExistance(True)

    def search(self,databaseName):
        clientInformation,signature = self.clientToServer(databaseName)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        serverOutput,verification = self.server.searchInformation(clientInformation,signature,pubkey_path)
        if verification:
            clientInput,signature = self.serverToClient(serverOutput)
            pubkey_path = self.pki.retrieve_key("Server")
            client,verification = self.client.receiveInformation(clientInput,signature,pubkey_path)
            if client and verification:
                print("List of information retrieved (format: [username, password]): ")
                if client == -1:
                    print("No information to retrieve")
                else:
                    print(client)
                return client
            else:
                print("Not able to verify signature. Aborting operation")
                return -1
        else:
            print("Not able to verify signature. Aborting operation")
            return -1

    def addItem(self,data):
        serverInput,signature = self.clientToServer(data)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        self.server.storeInformation(serverInput,signature,pubkey_path, existent = False)

    def update(self, data):
        serverInput,signature = self.clientToServer(data)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        self.server.storeInformation(serverInput,signature,pubkey_path, existent = True)

    def deleteItem(self,data):
        serverInput,signature = self.clientToServer(data)
        pubkey_path = self.pki.retrieve_key(self.client.username)
        self.server.deleteItem(serverInput,signature,pubkey_path)

    def send(self,usernameReceiver,dataPath):
        self.clientReceiverUsername = usernameReceiver
        pubkey_path = self.pki.retrieve_key(self.clientReceiverUsername)
        dataEncrypted,signature = self.client.sendInformation(dataPath,pubkey_path)
        nameFile = self.client.username + "encryptedMessage.txt"
        with open(nameFile,"wb") as f:
            if f!=-1:
                dataEncrypted = str(dataEncrypted).encode('utf-8')
                f.write(dataEncrypted)
                f.close()
            else:
                print("File couldn't be read")
                return False
        with open("signatureEncryptedMessage.txt","wb") as f:
            if f!=-1:
                signature = str(signature).encode('utf-8')
                f.write(signature)
                f.close()
            else:
                print("File couldn't be read")
                return False
        print("File was successfully sent")



    def read(self,pathRead,pathSignature,usernameSender):
        with open(pathSignature,'rb') as f:
            signature = f.read().decode('utf-8')
            f.close()
        with open(pathRead,'rb') as f:
            message = f.read().decode('utf-8')
            f.close()
        signature = ast.literal_eval(signature)
        message = ast.literal_eval(message)
        pubkey_path = self.pki.retrieve_key(usernameSender)
        data,verification = self.client.receiveInformation(message,signature,pubkey_path)
        return data
