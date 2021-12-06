class channel:
    def __init__(self, server, client, pki, client2Username = None):
        self.server = server
        self.client = client
        self.clientReceiverUsername = client2Username
        self.pki = pki

    def clientToServer(self,data):
        pubkey_path = self.pki.retrieve_key("server")
        clientOutput = self.client.askInformation(data,pubkey_path)
        return clientOutput

    def serverToClient(self, data):
        pubkey_path = self.pki.retrieve_key(self.client.username)
        serverOutput = self.server.sendInformation(data,pubkey_path)
        return serverOutput

    def checkUserExistance(self):
        data = self.client.checkUser()
        serverInput = self.clientToServer(data)
        login = self.server.searchInformation(serverInput)
        self.client.setExistance(login)
        return login

    def addUser(self):
        clientInformation = self.client.checkUser()
        serverInput = self.clientToServer(clientInformation)
        self.server.storeInformation(serverInput, existent = False)
        self.client.setExistance(True)

    def search(self,databaseName):
        clientInformation = self.clientToServer(databaseName)
        serverOutput = self.server.searchInformation(clientInformation)
        clientInput = self.server.sendInformation(serverOutput)
        client = self.client.receiveInformation(clientInput)
        if client:
            print("List of information retrieved (format: [username, password]): ")
            if client == -1:
                print("No information to retrieve")
            else:
                print(client)
            return client

    def addItem(self,data):
        serverInput = self.clientToServer(data)
        self.server.storeInformation(serverInput, existent = False)

    def update(self, data):
        serverInput = self.clientToServer(data)
        self.server.storeInformation(serverInput, existent = True)

    def deleteItem(self,data):
        serverInput = self.clientToServer(data)
        self.server.deleteItem(serverInput, all = False)
