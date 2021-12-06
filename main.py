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
    if newAction != "Y" and newAction != "y" and  newAction != "N" and newAction !="n":
        while newAction!="Y" and newAction != "y" and  newAction != "N" and newAction!="n":
            print("Invalid input")
            newAction = input("Do you want to perform a new action? (Y/n) \n")
            print(newAction)
    if newAction == "n" or newAction == "N":
        login = False
        print("Closing the application...")
    return login

username = input("Introduce username: ")
while len(username)==0:
    username = input("Wrong input, introduce a valid username: ")
password = input("Introduce password: ")
while len(password)==0:
    password = input("Wrong input, introduce a valid password: ")
hashPas = performHash(password)
Client = client(username, hashPas)
Server = server()
pki = pki()
Channel = channel(Server, Client,pki)
login = Channel.checkUserExistance()
#The user doesn't exist in the database, add user or close the application
if (login==False):
    print("User is not in the database")
    add = input("Do you want to create an account? (y/n)")
    if add == "y":
        Channel.addUser()
        login = True
        print("Welcome")
    elif add =="n":
        print("App closing...")
    else:
        print("Invalid input. App closing...")
elif login == True:
    print(" ")
    print("WELCOME")
    print(" ")
else:
    print("Wrong password or invalid verification. App closing...")

while login == True:
    action = input("Select action to perform (input help for list of options): ")
    if action == "help":
        print(" ")
        print("----------------------------------------------------------------------------------")
        print("List of options: ")
        print(" ")
        print("search : search on the database, retrieving all the credentials stored for your user")
        print("send: search information on the database and send it to another user")
        print("read: read a file sent by another user using this app")
        print("add : include a new item (usename and password) in the database")
        print("update : update item (password) in the database")
        print("delit : delete item from the database")
        print("logout : logout and close the application")
        print("----------------------------------------------------------------------------------")
        print(" ")
    elif action == "search":
        inp = input("Input search database (all your credentials from that database will be there): ").lower()
        data = Channel.search([inp])
        if data:
            inp = input("Do you want to store it on a txt file?(y/n)")
            if inp=="y" or inp =="Y":
                inp = input("Name of the file without extension:")
                while len(inp)==0:
                    inp = input("Invalid name, introduce the name of the file without extension:")
                nameFile = inp + ".txt"
                with open(nameFile,'wb') as f:
                    f.write(str(data).encode("utf-8"))
            elif inp!="y" and inp!="Y" and inp!="N" and inp!="n":
                while inp!="y" and inp!="n" and inp!="Y" and inp!="N":
                    inp = input("Not a valid input. Do you want to store the information on a txt file? (y/n)")
                if inp=="y" or inp =="Y":
                    inp = input("Name of the file without extension:")
                    while len(inp)==0:
                        inp = input("Invalid name, introduce the name of the file without extension:")
                    nameFile = inp + ".txt"
                    with open(nameFile,'wb') as f:
                        f.write(str(data).encode("utf-8"))
        login = performNewAction(login)
    elif action == "send":
        usernameReceiver = input("Type the username of the receiver: ")
        while len(usernameReceiver)==0:
            usernameReceiver = input("Invalid username, type the username of the receiver: ")
        dataSend = input ("Type the path of the .txt to be sent: ")
        while len(dataSend)==0:
            dataSend = input ("Invalid path of the file, type the path of the .txt to be sent: ")
        Channel.send(usernameReceiver,dataSend)
        login = performNewAction()
    elif action== "read":
        pathRead = input("Type the path of the .txt to be read: ")
        while len(pathRead)==0:
            pathRead = input("Invalid path, type the path of the .txt to be read: ")
        pathSignature = input("Type the path of the signature file (.sig) to be verified: ")
        while len(pathSignature) ==0:
            pathSignature = input("Invalid path, type the path of the signature file (.sig) to be verified: ")
        usernameSender = input("Type the username of the person that sent you the message: ")
        while len(usernameSender) == 0:
            usernameSender = input("Invalid username, type the username of the person that sent you the message: ")
        data = Channel.read(pathRead,pathSignature,usernameSender)
        if data!=-1:
            print(data)
            if data:
                inp = input("Do you want to store the unencrypted file in a txt file?(Y/n)")
                if inp=="Y" and inp =="y":
                    inp = input("Name of the file without extension:")
                    while len(inp)==0:
                        inp = input("Invalid input, introduce the name of the file without extension:")
                    nameFile = inp + ".txt"
                    with open(nameFile,'wb') as f:
                        f.write(str(data).encode("utf-8"))
                elif inp!="Y" and inp!="y" and inp!="n" and inp!="N":
                    while inp!="Y" and inp!="y" and inp!="n" and inp!="N":
                        inp = input("Invalid input, do you want to store the unencrypted file in a txt file?(y/n)")
                    if inp=="Y" and inp =="y":
                        inp = input("Name of the file without extension:")
                        while len(inp)==0:
                            inp = input("Invalid input, introduce the name of the file without extension:")
                        nameFile = inp + ".txt"
                        with open(nameFile,'wb') as f:
                            f.write(str(data).encode("utf-8"))
        else:
            print("There was an error verifying the signature")
        login = performNewAction()
    elif action == "add":
        inp = input("Database to access: ").lower()
        while len(inp) == 0:
            inp = input("Invalid input, type database to access: ").lower()
        if(inp!="users"):
            user = input("Username to add: ")
            while len(user)==0:
                user = input("Invalid input, type username to add: ")
            passw = input("Password to add: ")
            while len(passw) == 0:
                passw = input("Invalid input, type password to add: ")
            data = [inp, user, passw]
            Channel.addItem(data)
            login = performNewAction()
        else:
            print("Cannot access database")
            login = performNewAction()

    elif action == "update":
        inp = input("Database to access: ").lower()
        while len(inp) == 0:
            inp = input("Invalid input, type database to access: ").lower()
        if inp!="users":
            user = input("User to update: ")
            while len(user)==0:
                user = input("Invalid input, type username to update: ")
            passw = input("New password: ")
            while len(passw) == 0:
                passw = input("Invalid input, type new password to delete: ")
            data = [inp, user, passw]
            Channel.update(data)
        else:
            print("Cannot access database")
        login = performNewAction()

    elif action == "delit":
        inp = input("Database to access: ").lower()
        while len(inp) == 0:
            inp = input("Invalid input, type database to access: ").lower()
        if inp != "users":
            user = input("User to delete: ")
            while len(user)==0:
                user = input("Invalid input, type username to delete: ")
            passw = input("Password to delete: ")
            while len(passw) == 0:
                passw = input("Invalid input, type new password to delete: ")
            data =[inp, user, passw]
            Channel.deleteItem(data)
        else:
            print("Cannot access database")
        login = performNewAction()
    elif action == "logout":
        login = False
        print("Closing the application...")
    elif action == "adminOptionSetNewKey": #Admin function, do not use without an update all method or a hard reset
        print("Welcome, creator")
        Server.storeNewKey()
    else:
        print("Not recognized option")











        