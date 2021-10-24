import client
import channel
import server
username = input("Introduce username: ")
password = input("Introduce password: ")
client = client(username, password)
server = server()