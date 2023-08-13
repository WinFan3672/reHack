import sys
from resource.classes import *
from resource.libs import *
import data
import time

def div():
    print("--------------------")
def br():
    div()
    input("Press ENTER to continue.")
def cls():
    """
    Clears the terminal screen.
    """
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")
    
def Help(args):
    div()
    print("help: list of programs")
    print("cls: clears the screen")
    print("ping: checks if a host is up")
    print("nmap: lists open ports associated with an IP")
    print("exit: returns to the main menu")
    div()
def Exit(args):
    sys.exit()
def Argtest(args):
    print(args)
def Ping(args):
    if args:
        s = False
        for item in args:
            print("64 bytes to  {}...".format(item))
            time.sleep(2.5)
            for i in data.NODES:
                if i.address == item:
                    print("64 bytes from {} received.".format(item))
                    s = True
        if not s:
            print("Unable to resolve hostname.")
    else:
        div()
        print("ping <hostname[s]>")
        div()
        print("Confirms whether or not a hostname (or IP address) is online.")
        print("You can pass more than one at once.")
        div()
def nmap(args):
    if args:
        args = args[0]
        s = False
        for item in data.NODES:
            if item.address == args:
                div()
                print("Found Target")
                print("Hostname: {}".format(item.name))
                print("Ports: {}".format(len(item.ports)))
                print("Min. Ports To Crack: {}".format(item.minPorts))
                if item.ports:
                    div()
                for i in item.ports:
                    print("[{}] PORT {}: {} ".format("OPEN" if i.open else "CLOSED", i.num, i.name))
                div()
                s = True
        if not s:
            print("Failed to resolve address.")
    else:
        div()
        print("nmap <ip address>")
        div()
        print("Connects to an IP address and lists all open ports on it.")
        print("This is fully safe and will not raise any alarms.")
        div()