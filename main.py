from client import client
from channel import channel
from pki import pki
from server import server
from os import system, name
from encryption_functions import performHash
    
def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

def performNewAction(login=True):
    newAction = input("Do you want to perform a new action? (Y/n) \n")
    if newAction != "Y" and newAction !="n":
        while newAction != "Y" or newAction !="n":
            print("Invalid input")
            newAction = input("Do you want to perform a new action? (Y/n) \n")
    if newAction == "n":
        login = False
        print("Closing the application...")
    return login

username = input("Introduce username: ")
password = input("Introduce password: ")
hashPas = performHash(password)
Client = client(username, hashPas)
Server = server()
pki = pki()
Channel = channel(Server, Client,pki)
login = Channel.checkUserExistance()
#The user doesn't exist in the database, add user or close the application
if (login==False):
    print("User is not in the database")
    add = input("Do you want to create an account? (Y/n)")
    if add == "Y":
        Channel.addUser()
        login = True
        print("Welcome")
    elif add =="n":
        print("App closing...")
    else:
        print("Invalid input. App closing...")
elif login == True:
    print("Welcome")
else:
    print("Wrong password or invalid verification. App closing...")

while login == True:
    action = input("Select action to perform (input help for list of options): ")
    if action == "help":
        print("List of options: ")
        print("search : search on the database, retrieving all the credentials stored for your user")
        #print("send: search information on the database and send it to another user") #Yet to be implemented
        print("add : include a new item (usename and password) in the database")
        print("update : update item (password) in the database")
        print("delit : delete item from the database") #Yet to be implemented
        print("logout : logout and close the application")
    elif action == "search":
        inp = input("Input search database (all your credentials from that database will be there): ").lower()
        data = Channel.search([inp])
        if data:
            inp = input("Do you want to store it on a txt file?(Y/n)")
            if inp=="Y":
                inp = input("Name of the file without extension:")
                nameFile = inp + ".txt"
                with open(nameFile,'wb') as f:
                    f.write(str(data).encode("utf-8"))
        login = performNewAction(login)
        clear()
    elif action == "send":
        usernameReceiver = input("Type the username of the receiver: ")
        dataSend = input ("Type the path of the .txt to be sent: ")
        Channel.send(usernameReceiver,dataSend)
        login = performNewAction()
        clear()
    elif action== "read":
        pathRead = input("Type the path of the .txt to be read: ")
        pathSignature = input("Type the path of the signature file (.sig) to be verified: ")
        usernameSender = input("Type the username of the person that sent you the message: ")
        data = Channel.read(pathRead,pathSignature,usernameSender)
        if data!=-1:
            print(data)
            if data:
                inp = input("Do you want to store the unencrypted file in a txt file?(Y/n)")
                if inp=="Y":
                    inp = input("Name of the file without extension:")
                    nameFile = inp + ".txt"
                    with open(nameFile,'wb') as f:
                        f.write(str(data).encode("utf-8"))
            
        else:
            print("There was an error verifying the signature")
        login = performNewAction()
        clear()
    elif action == "add":
        inp = input("Database to access: ").lower()
        if(inp!="users"):
            user = input("Username to add: ")
            passw = input("Password to add: ")
            data = [inp, user, passw]
            Channel.addItem(data)
            login = performNewAction()
            clear()
        else:
            print("Cannot access database")
            login = performNewAction()
            clear()

    elif action == "update":
        inp = input("Database to access: ").lower()
        if inp!="users":
            user = input("User to update: ")
            passw = input("New password: ")
            data = [inp, user, passw]
            Channel.update(data)
        else:
            print("Cannot access database")
        login = performNewAction()
        clear()

    elif action == "delit":
        inp = input("Database to access: ").lower()
        if inp != "users":
            user = input("User to delete: ")
            passw = input("Password to delete: ")
            data =[inp, user, passw]
            Channel.deleteItem(data)
        else:
            print("Cannot access database")
        login = performNewAction()
        clear()
    elif action == "logout":
        login = False
        print("Closing the application...")
    elif action == "adminOptionSetNewKey": #Admin function, do not use without an update all method or a hard reset
        print("Welcome, creator")
        Server.storeNewKey()
    else:
        print("Not recognized option")











        