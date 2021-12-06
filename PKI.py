import pandas as pd
class PKI:
    def __init__(self):
        self.databasePath= "keys/publicKeys.csv"

    def retrieve_key(idOwner):
        with open(self.databasePath, 'rb') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        pubkey_path=False
        header = next(csv_reader)
        for row in csv_reader:
            if (row[0] == idOwner):
                pubkey_path = row[1]
            elif row[0] == "Default" and pubkey_path == False:
                pubkey_path = row[1]

        return pubkey_path
