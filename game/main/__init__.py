from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data

import getpass
import time
import configparser
import traceback
import hashlib
import random
import json


def loadGame():
    def load(config):
        def mkSaveName():
            return hashlib.sha256(str(random.randint(1, 2^64) * time.time()).encode()).hexdigest()

        player = PlayerNode(config.get("Player", "name", fallback="UNKNOWN"), config.get("Player", "password", fallback="root"))
        player.startActions()
        player.firewall.solution = config.get("Player", "firewall", fallback="a")
        player.creditCount = config.getint("Player", "credits", fallback=0)
        player.saveName = config.get("Player", "savefile", fallback=mkSaveName())

        mission = config.get("Player", "mission", fallback="None")
        player.currentMission = data.getMission(mission, player) if mission != "None" else None

        programs = {x[0]: config.getboolean("Programs", x[0], fallback="False") for x in config.items("Programs")}
        missions = {x[0]: config.getboolean("Missions", x[0], fallback="False") for x in config.items("Missions")}

        addrs = {x[0]: x[1] for x in config.items("Node Addresses")}
        toraddrs = {x[0]: x[1] for x in config.items("Tor Node Addresses")}

        for program in data.PROGRAMS:
            if program.name in programs.keys():
                program.unlocked = programs[program.name]

        for note in config.items("Notes"):
            player.notes.append(Note(note[1]))

        player.saved_accounts = {x[0]:x[1] for x in config.items("Accounts")}
        
        for node in data.NODES:
            if node.uid in addrs.keys():
                node.address = addrs[node.uid]

        for node in data.TOR_NODES:
            if node.uid in toraddrs.keys():
                node.address = toraddrs[node.uid]

        for mission in data.MISSIONS:
            if mission.mission_id in missions.keys():
                mission.complete = missions[mission.mission_id]

        # for account in config.items("Bank Accounts"):
        #     acct = json.loads(account[1])
        #     a = data.BankAccount(acct["ip"], acct["number"], acct["pin"], acct["balance"])
        #     data.getNode(acct["ip"]).backend.add_account(a)
        #     player.bankAccounts.append(a)



        # br()
        return player
    def getSaveFiles():
        files = []
        for f in os.listdir("savegames"):
            try:
                config = configparser.ConfigParser()
                config.read("savegames/{}".format(f))
                files.append(config)
            except:
                pass
        return files
    i = 1
    cls()
    div()
    configs = getSaveFiles()
    for config in configs:
        print("[{}] {} ({} Cr)".format(i, config.get("Player", "name", fallback="Unknown"), config.getint("Player", "credits", fallback=0)))
        print("    Date: {} {}".format(config.get("Player", "date", fallback="2010-06-01"), config.get("Player", "time", fallback="12:00")))
        print("    Last Saved: {}".format(config["Player"]["saved"]))
        i += 1
    div()
    try:
        ch = int(input("$"))
    except:
        return
    if ch == 0:
        return
    config = configs[ch-1]
    player = load(config)
    cls()
    player.main()


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
