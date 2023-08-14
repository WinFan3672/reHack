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
    for item in data.PROGRAMS:
        if item.unlocked:
            print(item.name)
    div()
def Exit(args):
    sys.exit()
def Argtest(args):
    print(args)
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
                if item.hacked:
                    print("HOST VULNERABILITY ACTIVE.")
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
def webworm(args):
    if args:
        for item in args:
            success = False
            print("TRYING {}...".format(item))
            for node in data.NODES:
                if node.address == item:
                    print("ATTACKING PORT 80...")
                    for port in node.ports:
                        if port.num == 80:
                            time.sleep(2.5)
                            port.open = True
                            print("SUCCESSFULLY OPENED PORT 80 @ {}".format(item))
                            success = True
                if not success:
                    print("Failed to attack port 80:")
                    print("* Confirm that the IP is correct.")
                    print("* Confirm that `{}` is a valid IP.".format(item))
    else:
        div()
        print("webworm <IP address(es)>")
        div()
        print("Attacks port 80 and opens it.")
        div()
def Directory(args):
    div()
    print("This is a list of reHack-related IP addresses.")
    div()
    print("ISP Database: 1.1.1.1")
    print("Mission Server: 255.255.255.0")
    print("Program Shop: 255.255.255.1")
    print("Credits Machine: 255.255.255.255")
    div()
    print("It has come to the attention of reHack.Org that agents are sharing their missions server")
    print("login credentials to friends and family. DO NOT DO THIS.")
    print("If you are found doing this, you will 'disappear' and never return.")
    div()
def sshkill(args):
    if args:
        for item in args:
            success = False
            print("TRYING {}...".format(item))
            for node in data.NODES:
                if node.address == item:
                    print("ATTACKING PORT 22...")
                    for port in node.ports:
                        if port.num == 22:
                            time.sleep(2.5)
                            port.open = True
                            print("SUCCESSFULLY OPENED PORT 22 @ {}".format(item))
                            success = True
                if not success:
                    print("Failed to attack port 22:")
                    print("* Confirm that the IP is correct.")
                    print("* Confirm that `{}` is a valid IP.".format(item))
    else:
        div()
        print("sshkill <IP address(es)>")
        div()
        print("Attacks port 22 and opens it.")
        div()
def porthack(args):
    if args:
        valid = False
        for item in data.NODES:
            if args[0] == item.address:
                valid = True
                openPorts = 0
                for port in item.ports:
                    openPorts += 1 if port.open else 0
                if openPorts >= item.minPorts:
                    print("OVERWHELMING HOST...")
                    time.sleep(7)
                    item.hacked = True
                    print("SUCCESS! YOU CAN NOW CONNECT TO THE HOST.")
                else:
                    print("ERROR: Insufficient open ports.")
        if not valid:
            print("Failed to resolve hostname.")
    else:
        div()
        print("porthack <IP ADDRESS>")
        div()
        print("Attacks a machine using open ports on it.")
        print("You must unlock at least the minimum amount as defined\nby nmap'ing the host.")