import client
import channel
import server

def performNewAction(login):
    newAction = input("Do you want to perform a new action? (Y/n)")
    if newAction != "Y" and newAction !="n":
        while newAction != "Y" or newAction !="n":
            print("Invalid input")
            newAction = input("Do you want to perform a new action? (Y/n)")
        if newAction == "n":
            login = False
            print("Closing the application...")
    return login


username = input("Introduce username: ")
password = input("Introduce password: ")
client = client(username, password)
server = server()
channel = channel(server, client)
login = channel.checkUserExistance()

#The user doesn't exist in the database, add user or close the application
if (login==False):
    print("User is not in the database")
    add = input("Do you want to create an account? (Y/n)")
    if add == "Y":
        channel.addUser()
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
        channel.search()
        login = performNewAction()
    elif action == "send":
        channel.send()
        login = performNewAction()
    elif action == "add":
        channel.add()
        login = performNewAction()
    elif action == "update":
        channel.update()
        login = performNewAction()
    elif action == "delit":
        channel.deleteItem()
        login = performNewAction()
    elif action == "delacc":
        channel.deleteAccount()
        login = performNewAction()
    elif action == "logout":
        login = False
        print("Closing the application...")
    else:
        print("Not recognized option")











        