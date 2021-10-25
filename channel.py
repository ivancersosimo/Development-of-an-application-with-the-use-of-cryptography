class channel:
    def __init__(self, server, client):
        self.server = server
        self.client = client

    def clientToServer(self,data):
        clientOutput = self.client.askInformation(data)
        return serverInput

    def serverToClient(self):
        return clientInput

    def checkUserExistance(self):
        data = self.client.checkUserExistance()
        serverInput = self.clientToServer(data)
        login = self.server.searchInformation(serverInput)
        return login

    def addUser(self):
        clientInformation = self.client.checkUserExistance()
        serverInput = self.clientToServer(clientInformation)
        self.server.storeInformation(serverInput)