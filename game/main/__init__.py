from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
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
def start():
    cls()
    div()
    print("Welcome To ReHack")
    div()
    print("[x] New Game")
    print("[x] Load Game")
    print("[3] Credits")
    print("[6] Exit")
    div()
    print("Version: {}\nReleased: {}".format(resourceInfo.friendlyVersion,resourceInfo.friendlyRelDate))
    div()
    try:
        ch = int(input("$"))
    except:
        start()
    if ch == 3:
        credits()
    elif ch == 6:
        return
    start()