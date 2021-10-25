from encryption_functions import symmetric_enc
class client:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.existance = False

    def setExistance(self, existance):
        self.existance = existance
        
    def askInformation(self, data):
        newData = [data[0],self.username,[data[1],data[2]]]
        encryptedData = symmetric_enc(newData)
        return encryptedData
    
    def checkUser(self):
        data = ["users", self.username, [self.username, self.password]]
        return data
