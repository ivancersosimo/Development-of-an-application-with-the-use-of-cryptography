from encryption_functions import symmetric_enc, signMessage, symmetric_dec, asymmetric_enc, asymmetric_dec,verifySignature
class client:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.existance = False
        if self.username == "lucia":
            self.privateKey_path = "keys/client1/clientkey_1.pem"
        elif self.username == "ivan":
            self.privateKey_path = "keys/client2/clientkey_2.pem"
        else:
            self.privateKey_path = "keys/client3/clientkey_3.pem"

    def setExistance(self, existance):
        self.existance = existance
        
    def askInformation(self, data, publicKey_path):
        if len(data)==1:
            newData = [data[0],self.username]
        else:
            newData = [data[0],self.username,[data[1],data[2]]]
        encryptedData = symmetric_enc(newData)
        encryptedDataAsym = asymmetric_enc(encryptedData,publicKey_path)
        signature = signMessage(encryptedDataAsym,self.privateKey_path)
        return encryptedDataAsym,signature

    def sendInformation(self,dataPath,publicKey_path):
        with open(dataPath,"rb") as f:
            data = f.read().decode("utf-8")
        encryptedData = symmetric_enc(data)
        encryptedDataAsym = asymmetric_enc(encryptedData,publicKey_path)
        signature = signMessage(encryptedDataAsym,self.privateKey_path)
        return encryptedDataAsym,signature
    
    def checkUser(self):
        data = ["users",self.username, self.password]
        return data
    
    def receiveInformation(self,dataEncryptedAsym,signature,pubkey_path):
        verification = verifySignature(dataEncryptedAsym,signature,pubkey_path)
        if verification:
            dataEncrypted = asymmetric_dec(dataEncryptedAsym,self.privateKey_path)
            data = symmetric_dec(dataEncrypted)
            return data,verification
        else:
            return -1,verification
