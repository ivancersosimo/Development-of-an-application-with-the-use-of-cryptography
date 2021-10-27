class channel:
    def __init__(self, server, client, client2Username = None):
        self.server = server
        self.client = client
        self.clientReceiverUsername = client2Username

    def clientToServer(self,data):
        clientOutput = self.client.askInformation(data)
        #TO BE IMPLEMENTED WITH ASYMMETRIC ENCRYPTION, next line is provisional until next delivery
        serverInput = clientOutput
        return serverInput

    def serverToClient(self, data):
        serverOutput = self.server.sendInformation(data)
        #TO BE IMPLEMENTED WITH ASYMMETRIC ENCRYPTION, next line is provisional until next delivery
        clientInput = serverOutput
        return clientInput

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
