from client import client
from channel import channel
from server import server

def performNewAction(login):
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
Client = client(username, password)
Server = server()
Channel = channel(Server, Client)
#login = Channel.checkUserExistance()
login = True

#The user doesn't exist in the database, add user or close the application
if (login==False):
    print("User is not in the database")
    add = input("Do you want to create an account? (Y/n)")
    if add == "Y":
        Channel.addUser()
    elif add =="n":
        print("App closing...")
    else:
        print("Invalid input. App closing...")

while login == True:
    action = input("Select action to perform: (input help for list of options)")
    if action == "help":
        print("List of options: ")
        print("search : search on the database")
        print("send : search information on the database and send it to another user")
        print("add : include a new item in the database")
        print("update : update item in the database")
        print("delit : delete item from the database") #Yet to be implemented
        print("delacc : delete account from the database") #Yet to be implemented
        print("logout : logout and close the application")
    elif action == "search":
        Channel.search()
        login = performNewAction()
    elif action == "send":
        usernameReceiver = input("Include the username of the receiver: ")
        Channel2 = channel(Server, Client, usernameReceiver)
        Channel.send()
        login = performNewAction()
    elif action == "add":
        
        inp = input("Database to access: ")
        user = input("Username to add: ")
        passw = input("Password to add: ")
        data = [inp, user, passw]
        Channel.addItem(data)
        login = performNewAction(login)
       
    elif action == "update":
        Channel.update()
        login = performNewAction()
    elif action == "delit":
        Channel.deleteItem()
        login = performNewAction()
    elif action == "delacc":
        Channel.deleteAccount()
        login = performNewAction()
    elif action == "logout":
        login = False
        print("Closing the application...")
    elif action == "adminOptionSetNewKey":
        print("Welcome, creator")
        Server.storeNewKey()
    else:
        print("Not recognized option")











        