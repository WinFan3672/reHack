from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data

import getpass
import time
import configparser
import traceback


def loadGame():
    def load(config):
        player = Player()
        player.startActions()
        player.name = config.get("Player", "name", fallback="unknownuser")
        player.password = config.get("Player", "password", fallback="root")
        player.firewall.solution = config.get("Player", "firewall", fallback="a")
    def getSaveFiles():
        files = {}
        for f in os.listdir("savegames"):
            try:
                with open("savegames/{}".format(f)) as file:
                    config = configparser.ConfigParser()
                    config.read("savegames/{}".format(f))
                    files[f] = config
            except:
                print(traceback.format_exc())
        return files
    i = 1
    cls()
    div()
    configs = getSaveFiles()
    for file in configs:
        config = configs[file]
        print("[{}] {} ({} Cr)".format(i, config.get("Player", "name", fallback="Unknown"), config.getint("Player", "credits", fallback=0)))
        print("    Date: {} {}".format(config.get("Player", "date", fallback="2010-06-01"), config.get("Player", "time", fallback="12:00")))
        print("    Last Saved: {}".format(config["Player"]["saved"]))
        i += 1
    br()


def credits():
    cls()
    div()
    print(
        "reHack was developed by the following contributors, both part- and full-time:"
    )
    for item in resourceInfo.contributors:
        print("* {}".format(item))
    if resourceInfo.formerContributors:
        div()
        print("The following people are former contributors:")
        for item in resourceInfo.formerContributors:
            print("* {}".format(item))
    div()
    print("LEGAL NOTICES")
    div()
    print("""reHack's gameplay is not intended as a suggestion of (or tutorial for) real hacking.
Any companies referenced are intended solely for parody.
Any resemblance to real companies is entirely coincidental.
The creators of reHack do not endorse any illegal activity of any kind. Please look into your country's jurdistiction if you're unsure.""")
    br()


def filter_string(str1, str2):
    for c in str2:
        str1 = str1.replace(c, "")
    return str1


def main():
    cls()
    div()
    print("Welcome to reHack.")
    print("Please register a user.")
    div()
    u = "admin"
    while u in data.BLOCKLIST:
        u = input("Enter a username $")
        u = u.lower()
        u = filter_string(u, "@\\/$ ")
        if u in data.BLOCKLIST:
            print("ERROR: This username is disallowed to prevent game instability.")
    p, cp = "x", ""
    while p != cp:
        p = getpass.getpass("Enter a password $")
        cp = getpass.getpass("Confirm your password $")
        if p != cp:
            print("ERROR: The passwords don't match.")
    p = PlayerNode(u, p)
    cls()
    div()
    print("You have officially registered as a reHack user.")
    print(
        "You will now connect you your own private node, run on our own infrastructure free-of-charge."
    )
    br()
    cls()
    print("Connecting to 127.0.0.1...")
    time.sleep(2.5)
    cls()
    div()
    print("ATTENTION: You have unread emails. Read them by running 'jmail'.")
    br()
    cls()
    p.main()


def start():
    while True:
        try:
            cls()
            div()
            with open("logo.txt") as f:
                print(f.read())
            div()
            print("[1] New Game")
            print("[2] Load Game")
            print("[3] Credits")
            print("[6] Exit")
            div()
            print(
                "Version: {}".format(
                    resourceInfo.friendlyVersion
                )
            )
            div()
            ch = int(input("$"))
            if ch == 1:
                main()
            elif ch == 2:
                loadGame()
            elif ch == 3:
                credits()
            elif ch == 6:
                return
            elif ch == 10:
                cls()
                PlayerNode("gordinator", "root").main()
        except:
            print(traceback.format_exc())
            br()
