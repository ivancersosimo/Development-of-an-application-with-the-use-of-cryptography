from encryption_functions import symmetric_enc
class client:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.existance = False

    def setExistance(self, existance):
        self.existance = existance
        
    def askInformation(self, data):
        data.append(self.username)
        encryptedData = symmetric_enc(data)
        hashData = hash(data)
        clientOutput = []
        clientOutput.append(encryptedData)
        clientOutput.append(hashData)
        return clientOutput
    
    def checkUser(self):
        data = ["users", self.username, [self.username, self.password]]
        return data
