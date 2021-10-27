from encryption_functions import symmetric_enc
from encryption_functions import symmetric_dec
class client:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.existance = False

    def setExistance(self, existance):
        self.existance = existance
        
    def askInformation(self, data):
        if len(data)==1:
            newData = [data[0],self.username]
        else:
            newData = [data[0],self.username,[data[1],data[2]]]
        encryptedData = symmetric_enc(newData)
        return encryptedData
    
    def checkUser(self):
        data = ["users",self.username, self.password]
        return data
    
    def receiveInformation(self,dataEncrypted):
        data = symmetric_dec(dataEncrypted)
        return data
