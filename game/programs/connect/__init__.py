from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
import data
import time
import json
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
def listDirTree(directory):
    d = []
    for item in directory:
        if isinstance(item, Folder):
            d.append([item.name,listDirTree(item.files)])
        else:
            d.append(item.name)
    return d
def printDirTree(tree, indent=1):
    for item in tree:
        if isinstance(item, str):
            print("    " * indent + item)
        elif isinstance(item, list) and len(item) == 2:
            folder_name = item[0]
            sub_tree = item[1]
            print("    " * indent + folder_name + "/")
            printDirTree(sub_tree, indent + 1)
def div():
    print("--------------------")
def connect(item):
    while True:
        ch = input("admin@{} $".format(item.address))
        ch = ch.split(" ")
        name = ch[0]
        args = ch[1:]
        if name in ["quit","exit"]:
            break
        elif name == "":
            continue
        elif name == "info":
            div()
            print("Address: {}".format(item.address))
            print("Hostname: {}".format(item.name))
            print("Users: {}".format(";".join([x.name for x in item.users]) if item.users else "None"))
            print("Has Linked Nodes: {}".format("Yes" if item.linked else "No"))
            div()
        elif name == "ls":
            f = item.files
            d = (listDirTree(f))
            print("/")
            printDirTree(d)
        elif name == "cls":
            cls()
        elif name == "help":
            div()
            print("help: list commands")
            print("cls: clears the screen")
            print("ls: lists all files on the file system.")
            print("info: print info about the host")
            print("scan: scans for related IP's.")
            print("exit: disconnect from host")
            div()
        elif name == "scan":
            for link in item.linked:
                n = data.getNode(link)
                if n:
                    print("{}: {}".format(n.name, n.address))
        else:
            print("ssh: syntax error.\nType `help` for a command list.")
def connectStart(address):
    BLOCKLIST = ["127.0.0.1"]
    resolved = False
    for item in data.NODES:
        if item.address == address:
            resolved = True
            item.visited = True
            if item.address in BLOCKLIST:
                resolved = False
            elif item.hacked and "main_hacked" in dir(item):
                item.main_hacked()
            elif item.hacked:
                print("Connecting to {}...".format(address))
                # time.sleep(2.5)
                connect(item)
            elif "main" in dir(item):
                item.main()
            else:
                print("ERROR: Access denied.")
    if not resolved:
        print("ERROR: Failed to resolve hostname.")
def main(args):
    if args:
        connectStart(args[0])
    else:
        div()
        print("connect <IP address>")
        div()
        print("Connect to a host and start executing commands on it.")
        print("Only works for hosts attacked with 'porthack'.")
        div()