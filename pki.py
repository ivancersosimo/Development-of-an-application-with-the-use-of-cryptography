import pandas as pd
class pki:
    def __init__(self):
        self.databasePath= "keys/publicKeys.csv"

    def retrieve_key(self,idOwner):
        database = pd.read_csv(self.databasePath, delimiter =";")
        pubkey_path=False
        for row in database.values:
            if row[0] == idOwner:
                pubkey_path = row[1]
            elif row[0] == 'Default' and pubkey_path == False:
                pubkey_path = row[1]
        return pubkey_path