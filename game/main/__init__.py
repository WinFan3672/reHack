from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data
import getpass
import time

def credits():
    cls()
    div()
    print("reHack was developed by the following contributors, both part- and full-time:")
    for item in resourceInfo.contributors:
        print("* {}".format(item))
    if resourceInfo.formerContributors:
        div()
        print("The following people are former contributors:")
        for item in resourceInfo.formerContributors:
            print("* {}".format(item))
    br()
def main():
    cls()
    div()
    print("Welcome to reHack.")
    print("Please register a user.")
    div()
    u = input("Enter a username $")
    p, cp = "x",""
    while p != cp:
        p = getpass.getpass("Enter a password $")
        cp = getpass.getpass("Confirm your password $")
        if p != cp:
            print("ERROR: The passwords don't match.")
    p = PlayerNode(u, p)
    cls()
    div()
    print("You have officially registered as a reHack user.")
    print("You will now connect you your own private node, run on our own infrastructure free-of-charge.")
    br()
    cls()
    print("Connecting to 127.0.0.1...")
    # time.sleep(2.5)
    p.main()
        
def start():
    cls()
    div()
    print("Welcome To ReHack")
    div()
    print("[1] New Game")
    print("[x] Load Game")
    print("[3] Credits")
    print("[6] Exit")
    print("[10] Quick Create New Game")
    div()
    print("Version: {}\nReleased: {}".format(resourceInfo.friendlyVersion,resourceInfo.friendlyRelDate))
    div()
    try:
        ch = int(input("$"))
    except:
        start()
    if ch == 1:
      main()  
    elif ch == 3:
        credits()
    elif ch == 6:
        return
    elif ch == 10:
        PlayerNode("root","root").main()
    start()