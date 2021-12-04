import pandas as pd
class PKI:
    def __init__(self):
        self.databasePath=pd.read_csv("publicKeys.csv")
    
    def retrieve_key(idOwner):
        pubkey_path=False #Until completely developed
        return pubkey_path