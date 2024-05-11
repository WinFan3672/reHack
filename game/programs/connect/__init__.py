from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
import getpass
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
            d.append([item.name, listDirTree(item.files)])
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
        args = ch.split(" ")
        if args in [["quit"], ["exit"]]:
            break
        elif args == []:
            continue
        elif args == ["info"] and "info" in item.installedPrograms:
            div()
            print("Address: {}".format(item.address))
            print("Hostname: {}".format(item.name))
            print(
                "Users: {}".format(
                    ";".join([x.name for x in item.users]) if item.users else "None"
                )
            )
            print("Has Linked Nodes: {}".format("Yes" if item.linked else "No"))
            div()
        elif args in [["clear"], ["cls"]]:
            cls()
        elif args == ["help"]:
            div()
            print("help: list commands")
            print("cls: clears the screen")
            if "info" in item.installedPrograms:
               print("info: print info about the host")
            if "scan" in item.installedPrograms:
                print("scan: scans for related IP's.")
            print("exit: disconnect from host")
            div()
        elif args == ["scan"] and "scan" in item.installedPrograms:
            valid = [data.getNode(x) for x in item.linked if x]
            for node in valid:
                print("{}: {}".format(node.name, node.address))
            if not valid:
                print("ERROR: No links found.")
        elif args == ["user"] and "user" in item.installedPrograms:
            div()
            print("user [args]")
            div()
            print("user list: list users")
            print("user add <username> [password]: add a user")
            print("user admin <username>: toggle a user's admin status")
            print("user passwd <username>: change a user's password")
            div()
        elif args == ["user", "list"] and "user" in item.installedPrograms:
            for user in item.users:
                print("* {} ({})".format(user.name, "Administrator" if user.isAdmin else "User"))
            if not item.users:
                print("ERROR: No users.")
        elif args == ["user", "add"] and "user" in item.installedPrograms:
            div()
            print("user add <username> [password]")
            div()
            print("Creates a user.")
            print("NOTE: Not setting a password means that the user is effectively disabled.")
            div()
        elif "user" in args and "add" in args and len(args) in [3,4] and "user" in item.installedPrograms:
            args.remove("user")
            args.remove("add")
            if len(args) == 1:
                user = User(args[0])
            else:
                user = User(args[0], args[1])
            item.users.append(user)
            print("Successfully added user.")
        elif args == ["user", "admin"] and "user" in item.installedPrograms:
            div()
            print("user admin <username>")
            div()
            print("Toggles a user's admin status.")
            print("WARNING: Make sure admins have secure passwords.")
            div()
        elif "user" in args and "admin" in args and len(args) == 3 and "user" in item.installedPrograms:
            args.remove("user")
            args.remove("admin")
            user = item.get_user(args[0])
            if not user:
                print("ERROR: Invalid username.")
                return
            user.isAdmin = not user.isAdmin
            print("Current user status: {}".format("Administrator" if user.isAdmin else "User"))
        elif args == ["user", "passwd"] and "user" in item.installedPrograms:
            div()
            print("user passwd <username>")
            div()
            print("Changes a user's password (or removes it, disabling that account.)")
            div()
        elif "user" in args and "passwd" in args and len(args) == 3 and "user" in item.installedPrograms:
            args.remove("user")
            args.remove("passwd")
            user = item.get_user(args[0])
            if not user:
                print("ERROR: Invalid username.")
                return
            passwd = getpass.getpass("Password $")
            user.password = passwd if passwd else None
            print("Successfully changed user password.")
        else:
            print("ERROR: Bad command or file name.")


def connectStart(address, player):
    resolved = False
    for item in data.NODES:
        if item.address == address and item.check_health():
            resolved = True
            item.visited = True
            if item.hacked and "main_hacked" in dir(item):
                if item.playerPlease:
                    item.main_hacked(player)
                else:
                    item.main_hacked()
            elif "main" in dir(item):
                if item.playerPlease:
                    item.main(player)
                else:
                    item.main()
            else:
                print("ERROR: Access denied.")
    if not resolved:
        print("ERROR: Failed to resolve hostname.")


def main(args, player):
    if args == ["history"]:
        history = [x for x in data.NODES if x.visited]
        for node in history:
            print("{}: {}".format(node.name, node.address))
        if not history:
            print("No history to show.")
    elif args:
        connectStart(args[0], player)
    else:
        div()
        print("connect <IP address>")
        div()
        print("Connect to a host and start executing commands on it.")
        print("Only works for hosts attacked with 'porthack'.")
        div()
