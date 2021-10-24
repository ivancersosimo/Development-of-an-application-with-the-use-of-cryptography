from skeleton_simmetric import symmetric_enc
class client:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.existance = False

    def setExistance(self):
        self.existance = True
        
    def askInformation(self, data):
        encryptedData = symmetric_enc(data)
        hashData = hash(data)
        clientOutput = []
        clientOutput.append(encryptedData)
        clientOutput.append(hashData)
        return clientOutput
    
    def checkUserExistance(self):
        data = ["users", self.username, self.password]
        clientOutput = self.askInformation(data)
        return clientOutput
