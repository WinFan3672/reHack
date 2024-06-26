import sys
from resource.classes import *
from resource.libs import *
import data
import time
import json
import types
import inspect
import traceback
import game.programs.connect as connect
import game.programs.connect as CONNECT # used in LANConnect()
import uuid
import random
import copy
import getpass
import copy
import concurrent.futures
import re
import getpass
import code

def isTorAddon():
    return data.getProgram("tor_addon").unlocked

def pickSelection(a_list: list, amount=1, remove=True):
    """
    Picks items randomly from a_list, amount of picks specified by amount.
    If remove is True, the picked item is removed.
    NOTE: No changes to a_list is made.
    """
    l = copy.copy(a_list)
    random.shuffle(l)

    x = []
    for i in range(amount):
        z = random.choice(l)
        x.append(z)
        if remove:
            l.remove(z)

    return x

def help(args):
    div()
    print("Program List")
    div()
    for item in sorted(data.PROGRAMS):
        if item.unlocked:
            print("{}: {}".format(item.name, item.desc))
    div()


def Exit(args):
    sys.exit()

def nmap(args):
    if args:
        node = data.getAnyNode(args[0], True) if isTorAddon() else data.getNode(args[0], True)
        if node:
            node.nmap = True
            div()
            print("Hostname: {}".format(node.name))
            print("Exposed Ports: {}".format(len(node.ports)))
            print("Min. Ports: {}".format(node.minPorts))
            if node.hacked:
                print("Root Access: Yes")
            if node.firewall:
                print("Firewall: Active")
            if node.ports:
                div()
                print("PORT\tSTATE\tSERVICE")
                div()
                for port in node.ports:
                    print("{}\t{}\t{}".format(port.num, "Open" if port.open else "Closed", port.name))
            div()
        else:
            div()
            print("ERROR: Failed to resolve address.")
            div()
    else:
        div()
        print("nmap <address>")
        div()
        print("Discover open ports on a node.")
        print("NOTE: This tool does not start active traces.")
        div()

class PortBreakingTool(Base):
    def __init__(self, name, port, unlocked=False, price=0):
        super().__init__()
        self.name = name
        self.port = port
        self.program = Program(self.name, "Tool for breaking port {}".format(port),self.function, unlocked=unlocked, price=price)
    def function(self, args):
        if len(args) == 1:
            item = args[0]
            success = False
            node = data.getAnyNode(item, True) if isTorAddon() else data.getNode(item, True)
            if node:
                print(f"Attacking port {self.port}...")
                if node.firewall:
                    print("ERROR: Attack blocked by firewall.")
                else:
                    for port in node.ports:
                        if port.num == self.port:
                            time.sleep(2.5)
                            port.open = True
                            print("Successfully opened port {} @ {}".format(self.port, item))
                            success = True
            if not node:
                print("ERROR: Invalid IP address.")
            elif not success:
                print("Failed to attack port {}:".format(self.port))
                print("* Confirm port {} is valid.".format(self.port))
                print("* Confirm that `{}` is a valid IP.".format(item))
        else:
            div()
            print("{} <IP address>".format(self.name))
            div()
            print("Attacks port {} and opens it.".format(self.port))
            div()


def porthack(args):
    if len(args) == 1:
        node = data.getAnyNode(args[0], True) if isTorAddon() else data.getNode(args[0], True)
        if node:
            openPorts = 0
            for port in node.ports:
                openPorts += 1 if port.open else 0
            if openPorts >= node.minPorts:
                print("Overwhelming host...")
                if node.firewall:
                    print("ERROR: Attack blocked by firewall.")
                else:
                    hackTime = 7 / (openPorts+1)
                    time.sleep(hackTime)
                    node.hacked = True
                    print("Success: Root access installed.")
            else:
                print("ERROR: Insufficient open ports.")
        else:
            print("Failed to resolve hostname.")
    else:
        div()
        print("porthack <IP address>")
        div()
        print("Attacks a machine using open ports.")
        # print("You must unlock at least the minimum amount as defined")
        # print("by running 'nmap <hostname>'.")
        div()


class MessageBoardMessage(Base):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.text = text
    def read(self):
        cls()
        div()
        print(self.title)
        div()
        print(self.text)
        br()


class MessageBoard(Node):
    def __init__(
        self, name, address, uid, path, ports=[], minPorts=3, linked=[], users=[]
        ):
        ports = (
            ports
            if ports
            else [data.getPort(80), data.getPort(1433), data.getPort(24525)]
        )
        super().__init__(
            name,
            uid,
            address,
            linked=linked,
            users=users,
            ports=ports,
            minPorts=minPorts,
        )
        self.path = path
        self.ports = ports
        self.messages = []
        self.posts = [x for x in os.listdir("msgboard/{}".format(self.path))]
        self.compile()

    def main(self):
        while True:
            cls()
            div()
            print(self.name)
            div()
            i = 0
            for message in self.messages:
                print("[{}] {}".format(i, message.title))
                i += 1
            div()
            try:
                ch = int(input("$"))
                message = self.messages[ch]
                message.read()
            except:
                return
            div()
    def compile(self):
        for item in self.posts:
            with open("msgboard/{}/{}".format(self.path, item)) as f:
                m = MessageBoardMessage(item, f.read())
                self.messages.append(m)


class WebServer(Node):
    def __init__(
        self, name, uid, address, path, linked=[], hacked=False, minPorts=2, users=[]
        ):
        super().__init__(
            name,
            uid,
            address,
            linked=linked,
            hacked=hacked,
        )
        self.ports = [data.getPort(22), data.getPort(21), data.getPort(80)]
        self.path = path
        self.users = users
        self.minPorts = minPorts

    def main(self):
        with open("websites/{}".format(self.path)) as f:
            for line in f.read().rstrip("\n").split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)
class TorWebServer(Node):
    def __init__(
        self, name, uid, address, path, linked=[], hacked=False, minPorts=2, users=[], webmaster="null@null.null"
        ):
        super().__init__(
            name,
            uid,
            address,
            linked=linked,
            hacked=hacked,
        )
        self.ports = [data.getPort(80), data.getPort(9200)]
        self.path = path
        self.users = users
        self.minPorts = minPorts
        self.webmaster = webmaster

    def main(self):
        with open("onionsites/{}".format(self.path)) as f:
            for line in f.read().split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)
    def main_hacked(self):
        div()
        print("Tor web server status: 200 OK")
        print("Contact the webmaster: {}".format(self.webmaster))
        div()

def tree(folder, indent=0):
    print("{}{}".format("  " * indent, folder))
    for file in folder.files:
        if isinstance(file, Folder):
            tree(file, indent + 1)
        else:
            print("{}{}".format("  " * (indent + 1), file))            

def debuginfo(args, player):
    if args == ["passwd"]:
        with open("data/passwords.txt") as f:
            print(random.choice(f.read().split("\n")))
    elif args == ["lans"]:
        for node in [x for x in data.NODES + data.TOR_NODES if isinstance(x, RemoteLAN)]:
            print(node.uid)
    elif args == ["freecash"]:
        reward = 0
        for mission in [x for x in player.MISSIONS if x.complete]:
            reward += mission.reward
        player.creditCount += reward
        print("Gained {:,} Cr.".format(reward))
    elif args == ["trace"]:
        player.trace = Trace("debianftp", "Corporate", 5)
    elif args == ["ide"]:
        code.interact(local=locals() | globals(), banner="Python Interpreter: press Ctrl+D to exit",exitmsg="Exit Python interpreter.")
    elif args == ["cm"]:
        while player.currentMission:
            print("Completed: {}".format(player.currentMission.name))
            player.currentMission.end()
    elif args == ["pc"]:
        print(len([x for x in data.PROGRAMS if x.unlocked]))
    elif args == ["tor"]:
        for node in data.TOR_NODES:
            print("{} = {}".format(node.uid, node.address))
    elif "tor" in args and len(args) == 2:
        args.remove("tor")
        node = data.getTorNode(args[0])
        div()
        print("Name: {}".format(node.name))
        print("Unique ID: {}".format(node.uid))
        print("IP Address: {}".format(node.address))
        print("Linked Nodes: {}".format("; ".join(node.linked) if node.linked else "None"))
        print("Ports: {}".format("; ".join([x.name for x in node.ports]) if node.ports else "None"))
        print("Min. Ports To Hack: {}".format(node.minPorts))
        for user in node.users:
            print("User {}:{}".format(user.name, user.password))
        div()
    elif args == ["ip"]:
        div()
        print("debug ip [arguments]")
        div()
        print("Positional arguments:")
        print("    list: lists all nodes and their info")
        print("    info: get info about a node")
        div()
    elif args == ["tree"]:
        div()
        print("debug tree <address>")
        div()
        print("Prints a file tree of all files and folders on a system")
        div()
    elif "tree" in args and len(args) == 2:
        node = data.getNode(args[1])
        if not node:
            print("ERROR: Invalid node")
            return
        tree(data.createFolder(node))

    elif args == ["save"]:
        print("savegames/{}.rh_save".format(player.saveName))
    elif args == ["date"]:
        div()
        print("debug date <function> [args]")
        div()
        print("Positional arguments:")
        print("    set <year> <month> <day>: set the date to a specific date")
        print("    fwd <days>: Move forward in time <days> times")
        div
    elif args == ["date", "set"]:
        div()
        print("debug date set <year> <month> <day>")
        div()
        print("Set the date to a custom date.")
        div()
    elif "date" in args and "set" in args and len(args) == 5:
        newdate = GameDate(int(args[2]), int(args[3]), int(args[4])-1)
        if newdate < GameDate():
            print("ERROR: Cannot have a date older than {}".format(GameDate()))
            return
        player.date = newdate.clone()
        player.timeSinceNextDay = time.time()
    elif args == ["date", "fwd"]:
        div()
        print("debug date fwd <days>")
        div()
        print("Moves forward in time by <days> days.")
        div()
    elif "date" in args and "fwd" in args and len(args) == 3:
        count = int(args[2])
        for i in range(count):
            player.date += 1
            player.tick()
    elif args == ["ls"]:
        div()
        print("debug ls <uid>")
        div()
        print("Displays the (flattened) file list of a node.")
        div()
    elif "ls" in args and len(args) == 2:
        node = data.getNode(args[1])
        if node:
            print([str(x) for x in data.createFolder(node)])
    elif args == ["health"]:
        for node in data.NODES + data.TOR_NODES:
            if not node.check_health():
                print(node.uid)
    elif args == ["ip", "list"]:
        div()
        print("UID\t\tHOSTNAME")
        div()
        for x in data.NODES:
            print("{}\t\t{}".format(x.uid, x.name))
        div()
    elif args == ["ip", "count"]:
        print(len(data.NODES))
    elif args == ["ip", "info"]:
        div()
        print("debug ip info <uid>")
        div()
        print("Prints info about a node.")
        div()
    elif "ip" in args and "info" in args and len(args) == 3:
        node = data.getNode(args[2])
        if not node:
            raise Exception("Invalid node given.")
        div()
        print("Name: {}".format(node.name))
        print("Unique ID: {}".format(node.uid))
        print("IP Address: {}".format(node.address))
        print("Linked Nodes: {}".format("; ".join(node.linked) if node.linked else "None"))
        print("Ports: {}".format("; ".join([x.name for x in node.ports]) if node.ports else "None"))
        print("Min. Ports To Hack: {}".format(node.minPorts))
        for user in node.users:
            print("User {}:{}".format(user.name, user.password))
        div()
    elif args == ["gen"]:
        print("\n".join(data.GENERATED))
    elif args == ["lan"]:
        div()
        print("debug lan <uid>")
        div()
        print("Displays info about a LAN.")
        div()
    elif "lan" in args and len(args) == 2:
        node = data.getNode(args[1])
        if isinstance(node, LocalAreaNetwork):
            div()
            print("ADDR\tHOSTNAME")
            div()
            for x in node.devices:
                print("{}\t{}".format(x.address, x.name))
            div()
        else:
            print("ERROR: Invalid LAN.")
    elif args == ["buy"]:
        for prog in data.PROGRAMS:
            prog.unlocked = True
        print("Purchased all programs.")
    elif args == ["sm"]:
        div()
        print("debug sm <mission-id>")
        div()
        print("Start a mission immediately.")
        print("Adds the current mission to the rejects hub.")
        div()
        print("debug sm list: lists all missions")
        div()
    elif args == ["sm", "list"]:
        for mission in player.MISSIONS:
            print("{}: {}".format(mission.mission_id, mission.name))
    elif "sm" in args and len(args) == 2:
        args = args[1]
        newMission = data.getMission(args, player)
        if newMission:
            if player.currentMission:
                pass
            player.currentMission = newMission
            player.currentMission.start()
        else:
            print("ERROR: Invalid mission ID.")
    else:
        div()
        print("debug <args>")
        div()
        print("Positional arguments:")
        print("    passwd: print a random password that can be brute-forced")
        print("    ip: lists information about nodes")
        print("    sm: start a mission")
        print("    cm: complete an entire mission series.")
        print("    gen: lists all IP addresses generated randomly.")
        print("    buy: purchases all programs for free")
        print("    lan: displays info about a LAN")
        print("    health: list all dead nodes")
        print("    date: control the date and time")
        print("    pc: display how many programs are installed")
        print("    tree: display a node's file tree")
        print("    save: prints the player's save file")
        print("    ide: open a Python console with reHack's locals and globals")
        print("    lans: lists UIDs of all LANs with login screens ('Remote LANs')")
        div()
        print("WARNING: This program is not intended for use by anyone other than the developers.")
        print("It is meant to be used when debugging the game, not when playing it.")
        print("It WILL ruin the fun significantly if used incorrectly.")
        div()


class Email(Base):
    def __init__(self, sender, receiver, subject=None, body=None):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.read = False


class EmailData(Base):
    def __init__(self, autoresponse):
        super().__init__()
        self.inbox = []
        self.sent = []
        self.autoresponse = autoresponse

    def receive(self, email):
        self.inbox.append(email)
        if self.autoresponse:
            self.autoresponse.receiver = email.sender
            sendEmail(self.autoresponse)
            self.send(self.autoresponse)

    def send(self, email):
        self.sent.append(email)


class MailAccount(Base):
    def __init__(self, name, password=None, autoresponse=None):
        super().__init__()
        self.name = name
        self.password = password if password else makeRandomString()
        self.data = EmailData(autoresponse)

def sendEmail(email: Email):
    recipient = email.receiver
    parts = recipient.split("@")
    server = data.getNode(parts[1], True) 
    if isinstance(server, MailServer):
        account = None
        for item in server.accounts:
            if item.name == parts[0]:
                account = item
        if account:
            account.data.receive(email)
            server.emails.append(email)
        else:
            m = [
                "Your message to {} could not be delivered.".format(recipient),
                "Please check that the email address is valid and try again.",
                # "You can use the `mxlookup` utility for a list of email accounts on our server.",
                "",
                "FROM: {}".format(email.sender),
                "TO: {}".format(email.receiver),
                "SUBJECT: {}".format(email.subject),
                "",
                "EMAIL START",
                email.body,
                "EMAIL END",
            ]
            m = "\n".join(m)
            e = Email(
                "accounts-daemon@{}".format(parts[1]),
                email.sender,
                "Your message could not be delivered",
                m,
            )
            sendEmail(e)
    else:
        raise TypeError("Invalid mail server: {} ({}>{})".format(parts[1],email.sender, email.receiver))


def sendTorEmail(email: Email):
    recipient = email.receiver
    parts = recipient.split("@")
    server = None
    for item in data.TOR_NODES:
        if item.address == parts[1]:
            server = item
            break
    if isinstance(server, TorMailServer):
        account = None
        for item in server.accounts:
            if item.name == parts[0]:
                account = item
        if account:
            account.data.receive(email)
            server.emails.append(email)
        else:
            m = [
                "Your message to {} could not be delivered.".format(recipient),
                "The email address is invalid.",
                "Please check that the email address is valid and try again.",
                "",
                "FROM: {}".format(email.sender),
                "TO: {}".format(email.receiver),
                "SUBJECT: {}".format(email.subject),
                "",
                "EMAIL START",
                email.body,
                "EMAIL END",
            ]
            m = "\n".join(m)
            e = Email(
                "accounts-daemon@{}".format(parts[1]),
                email.sender,
                "Your message could not be delivered",
                m,
            )
            sendTorEmail(e)
    else:
        raise TypeError("Invalid mail server: {} ({}>{})".format(parts[1],email.sender, email.receiver))

class MailServer(Node):
    def __init__(
        self,
        name,
        uid,
        address,
        player,
        users=[],
        accounts=[],
        hideLookup=False,
        minPorts=4,
        web_address=None,
        **kwargs
        ):
        super().__init__(
            name,
            uid,
            address,
            ports=[
                data.getPort(21),
                data.getPort(22),
                data.getPort(25),
                data.getPort(80),
            ],
            minPorts=minPorts,
            player=player,
            **kwargs,
        )
        self.users = users
        self.accounts = [MailAccount("accounts-daemon")]
        self.accounts += [x for x in accounts if ininstance(x, MailAccount)]
        self.hideLookup = hideLookup
        self.emails = []
        self.web_address = web_address
        x = []
        for user in self.users:
            self.accounts.append(MailAccount(user.name, user.password))

    def main(self, args=None, player=None):
        if self.web_address:
            connect.main([self.web_address], data.getNode("localhost"))
        else:
            print("To access this mail server, log in with a mail client.")

    def clientMain(self, account, player):
        cls()
        print("Welcome to {}. For a command list, type HELP.".format(self.name))

        while True:
            ch = input("{}@{} $".format(account.name, self.address))

            if ch == "help":
                div()
                print("help: command list")
                print("cls: clear the screen")
                if not f"{self.name}@{self.address}" in player.saved_accounts.keys():
                    print("save: save this account for future use")
                print("list: list all emails")
                print("read <id>: read an email")
                print("save: save this email address's details in reHackOS")
                print("exit: disconnect from host")
                div()
            elif ch in ["quit", "exit"]:
                return
            elif ch in ["clear", "cls"]:
                cls()
            elif ch == "":
                pass
            elif ch == "list":
                if getEmails(account.data):
                    div()
                    i = 0
                    for item in getEmails(account.data):
                        print("{}: {} ({} --> {}) {}".format(
                            i,
                            item.subject,
                            item.sender,
                            item.receiver,
                            "[!]" if not item.read else "",
                        )
                              )
                        i += 1

                    div()
                else:
                    div()
                    print("Your inbox is empty.")
                    div()
            elif ch == "save":
                player.saved_accounts["{}@{}".format(account.name, self.address)] = account.password
                print("Successfully saved email account.")
                print("Check your email client for a list of saved accounts.")
            elif ch == "read":
                div()
                print("read <id>")
                div()
                print("Read an email.")
                div()
            elif ch.startswith("read "):
                try:
                    index = int(ch[5:])
                    if 0 <= index <= len(getEmails(account.data)):
                        email = getEmails(account.data)[index]
                        email.read = True
                        div()
                        print("FROM: {}".format(email.sender))
                        print("TO: {}".format(email.receiver))
                        print("SUBJECT: {}".format(email.subject))
                        div()
                        print(email.body)
                        div()
                    else:
                        print("ERROR: Invalid email.")
                except IndexError:
                    print("ERROR: Invalid email index.")
                except:
                    print(traceback.format_exc())
            else:
                print("ERROR: Invalid command.")

    def client(self, username, password, player):
        print("{}:{}".format(username, password))
        for account in self.accounts:
            if account.name == username and account.password == password:
                return self.clientMain(account, player)
        print("ERROR: Invalid account.")

    def lookup(self):
        return self.accounts if not self.hideLookup else []

    def create_user(self, username, password):
        self.accounts.append(MailAccount(username, password))

    def main_hacked(self):
        def grabEmails(self):
            return self.emails

        print("Mail Server Admin Panel")
        print("Run 'help' for a command list.")
        while True:
            ch = input("admin@{} $".format(self.address))
            args = ch.split(" ")[1:]
            if ch in ["quit", "exit"]:
                return
            elif ch == "help":
                div()
                print("help: command list")
                print("list: list all emails in server")
                print("read <id>: view an email")
                print("users: print all users")
                print("useradd <username>: add a user to the mail server")
                print("reset <user> <new-password>: reset a user's password")
                print("exit: disconnect from host")
                div()
            elif ch in ["cls", "clear"]:
                cls()
            elif ch == "useradd":
                div()
                print("useradd <username>")
                div()
                print("Create a mail account.")
                div()
            elif ch.startswith("useradd "):
                usr = ch[8:]
                self.accounts.append(MailAccount(usr))
                print("Successfully added user.")
            elif ch.startswith("reset "):
                ch = ch[6:]
                args = ch.split(" ")
                if len(args) == 2:
                    account = None
                    for acc in self.accounts:
                        if acc.name == args[0]:
                            account = acc
                    if account:
                        account.password = args[1]
                        print("Successfully reset password.")
                    else:
                        print("ERROR: Invalid account name.")
                else:
                    print("ERROR: Invalid syntax.")
            elif ch == "reset":
                div()
                print("reset <username> <password>")
                div()
                print("Reset a user's password.")
                div()
            elif ch == "users":
                for item in self.accounts:
                    print(item.name)
            elif ch.startswith("read "):
                try:
                    emails = grabEmails(self)
                    index = int(ch[5:])
                    if 0 <= index < len(emails):
                        email = emails[index]
                        div()
                        print("FROM: {}".format(email.sender))
                        print("TO: {}".format(email.receiver))
                        print("SUBJECT: {}".format(email.subject))
                        div()
                        print(email.body)
                        div()
                except Exception as e:
                    print("ERROR: {}".format(e))
            elif ch == "list":
                i = 0
                for item in grabEmails(self):
                    print(
                        "{}: {} ({} --> {})".format(
                            i, item.subject, item.sender, item.receiver
                        )
                    )
                    i += 1
            else:
                print("ERROR: Invalid command.")


class JmailServer(MailServer):
    def __init__(self, player):
        super().__init__(
            "JMail",
            "jmail",
            "jmail.com",
            player,
            [
                User("admin", "rosebud"),
                User(player.name, player.password),
                User("xwebdesign"),
                User("monicaf332","letmein"),
                User("mastervps-logs", "sunshine"),
            ],
            hideLookup=True,
        )
        self.ports = [data.getPort(25), data.getPort(80), data.getPort(22)]
        self.minPorts = 2

    def main(self, args=None, player=None):
        with open("websites/jmail.com") as f:
            for line in f.read().split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)

    def add_account(self, username):
        a = MailAccount(username)
        self.accounts.append(a)

    def create_user(self, username, password=None):
        self.accounts.append(MailAccount(username, password))


def mxlookup(args, player=None):
    if args:
        for arg in args:
            node = data.getNode(arg)
            if isinstance(node, MailServer):
                div()
                print(node.name)
                div()
                if node.lookup():
                    for account in node.lookup():
                        print("{}@{}".format(account.name, node.address))
                else:
                    print("The MX request returned no email addresses.")
                    print("It is likely that the mail server has enabled MX masking.")
            else:
                div()
                print("Invalid mail server: {}".format(arg))
        div()
    else:
        div()
        print("mxlookup [ip address(es)]")
        div()
        print("Lists all email addresses attached to a particular mail server.")
        div()


class ForwardingData(EmailData):
    def __init__(self, address):
        super().__init__()
        self.inbox, self.sent = [], []
        self.address = address

    def receive(self, email):
        email.receiver = self.address
        sendEmail(email)

    def send(self, email):
        self.sent.append(email)


class ForwardingAccount(MailAccount):
    def __init__(self, name, email):
        super().__init__(name)
        self.data = ForwardingData(email)


class AnonMail(MailServer):
    def __init__(self, player):
        super().__init__(
            "AnonMail",
            "anonmail",
            "anon.mail",
            player,
            [
                User("admin"),
                User("noreply"),
                User("welcome"),
                User("marketing"),
                User("ceo", "debugger"),
            ],
        )
        self.ports = []
        self.minPorts = 4
        x = 2**9
        for i in range(x):
            self.accounts.append(MailAccount(makeRandomString()))
    def main(self):
        connect.main(["www.anon.mail"], data.getNode("localhost"))
    def lookup(self):
        return [
            MailAccount(x.name) for x in self.users if x.name not in ["ceo", "noreply"]
        ]

    def create_user(self, username, password):
        acc = MailAccount(username, password)
        self.accounts.append(acc)
        return acc


def jmail(args, player):
    acc = "{}@jmail.com".format(player.name)
    mailman_base([acc, player.password], player)

class MailDotCom(MailServer):
    def __init__(self, name, address, player, users=[], adminPassword=None, **kwargs):
        super().__init__(name, address, address, player, users=users, **kwargs)
        self.ports = [
            data.getPort(21),
            data.getPort(22),
            data.getPort(25),
            data.getPort(80),
        ]
        self.minPorts = 4
        self.accounts = [
            MailAccount("admin", adminPassword),
            MailAccount("noreply", autoresponse=Email(
                "noreply@{}".format(self.address),
                "SENDER",
                "This inbox does not accept emails",
                "Hello. This inbox does not receive emails. It only sends them. Therefore, the email you have sent will be ignored.",
            )),
        ]
        for item in users:
            self.accounts.append(MailAccount(item.name, item.password))
        self.users = [User(x.name, x.password) for x in self.accounts]
        self.alive = True
        self.welcomed = False
    def main(self):
        connect.main(["mail.com"], data.getNode("localhost"))
    def lookup(self):
        return [MailAccount("admin")]
    def tick(self):
        self.alive = data.getNode("mailcommain").check_health()
        if not self.welcomed:
            self.welcomed = True
            sendEmail(Email("noreply@root.mail.com", "admin@{}".format(self.address), "Welcome To Your New Inbox", """Thank you for being a Mail.Com customer.
This is your new mail server. You can use commands such as USERADD and USERS to manage users, LIST and READ to read emails, and RESET to manage credentials securely.
You can also be rest assured that your server is secured to the highest degree, and (most importantly), works out of the box and won't fail.

That's a pretty good proposition, if we don't say so ourselves, and a fair price you paid for it too."""))
            sendEmail(Email("davepl@root.mail.com", "admin@{}".format(self.address), "Your Mail.Com Support Agent", """Dear administrator,
My name is Dave. I am head of the Enterprise Support team here at Mail.Com, and my job is to provide you with top-notch, high-priority, fast, and easy tech support regarding your mail server.
If your boss is calling you and asking questions, I can help. If your mail server is giving you cryptic errors, I can help. If a popular mail service is dropping your emails or sending them to spam, I can help.

If you need support with anything, feel free to shoot me an email. You can hit 'Reply' in your client, or just create a new email conversation. Even better, you can use your new Mail.Com server to do it :)"""))

    def check_health(self):
        return self.alive


def mailoverflow(args, player):
    if args:
        for arg in args:
            successes, failures = 0, 0
            for i in range(5000):
                try:
                    em = Email(
                        "{}@jmail.com".format(player.name),
                        arg,
                        str(i),
                        data.generateIP(),
                    )
                    sendEmail(em)
                    successes += 1
                except:
                    failures += 1
            print("{}: {}/{} Sent".format(arg, successes - failures, successes))
            argx = arg.split("@")
            node = data.getNode(argx[1])
            if node:
                for port in node.ports:
                    if port.num == 25:
                        if player.firewall:
                            print("Cannot open port 25: firewall active.")
                        else:
                            port.open = True
                            print("Opened port 25 on {}".format(node.address))
            else:
                print("WARNING: The email server was not found.")
                print(
                    "         Check your email address for thousands of bounced emails."
                )
    else:
        div()
        print("mailoverflow <list of email addresses>")
        div()
        print("Sends 5000 junk emails to each specified email address.")
        print("Also opens port 25 if it is exposed.")
        print(
            "WARNING: Double-check the email address. If the email server is valid but the username is not, the emails will bounce to your inbox."
        )
        print("WARNING: Your email account is used to send the emails.")
        div()

# def sweep(args):
#     print("Begin sweep...")
#     nodes = []
#     try:
#         for a in range(256):
#             for b in range(256):
#                 print("Begin {}.{}.x.x".format(a,b))
#                 for c in range(256):
#                     for d in range(256):
#                         node = data.getNode(f"{a}.{b}.{c}.{d}")
#                         if node:
#                             print("{}: {}".format(node.address,node.name))
#                             nodes.append(node)
#     except KeyboardInterrupt:
#         pass
#     print("Finished sweep.")
#     if nodes:
#         for node in nodes:
#             print("{}: {}".format(node.address,node.name))
#     else:
#         print("No nodes found.")


def store(args, player):
    def getPrograms(player):
        return sorted([x for x in data.PROGRAMS if not x.unlocked and x.inStore], key=lambda x: x.name)

    if args == ["list"]:
        div()
        if not getPrograms(player):
            print("ERROR: Store is empty")
            div()
        for item in getPrograms(player):
            print("{}".format(item.name))
            print("    {}\n    {} Cr.".format(item.desc, item.price))
            div()
    elif "buy" in args and len(args) == 2:
        try:
            pid = args[1]
            programs = getPrograms(player)
            valid = False
            for program in programs:
                if program.name == pid:
                    valid = True
                    print(installProgram(program))
            if not valid:
                print("ERROR: Invalid program.")
        except Exception as e:
            print("ERROR: {}".format(e))
    elif args in [["bal"], ["balance"]]:
        print("{} Cr.".format(player.creditCount))
    else:
        div()
        print("store <args>")
        div()
        print("Store for purchasing software.")
        div()
        print("store list: list all software for sale.")
        print("store buy <program name>: buy a program")
        print("store balance: prints out how many credits you have.")
        div()


def anonclient(args, player):
    if args == ["create"]:
        try:
            username, password = makeRandomString(), getpass.getpass(
                "Password for your new email account $"
            )
            node = data.getNode("anon.mail")
            if isinstance(node, AnonMail):
                node.create_user(username, password)
                print("Created a new user.")
                c = ""
                for i in range(len(password)):
                    c += "*"
                print("Address: {}@anon.mail\nPassword: {}".format(username, c))
            else:
                print("ERROR: Could not contact anon.mail (ERROR 404)")
        except Exception as e:
            print("ERROR: {}".format(e))
    else:
        div()
        print("anonmail [args]")
        div()
        print("Client for anonmail, the anonymous email forwarder.")
        div()
        print("anonmail create [email address]: create a new identity.")
        div()


def login(args):
    if len(args) == 2:
        node = None
        for item in data.NODES:
            if item.address == args[0]:
                node = item
        if node:
            account = None
            for user in node.users:
                if user.name == "admin":
                    account = user
            if account:
                if account.password == args[1]:
                    node.hacked = True
                    print("Successfully infected device.")
                    print("You can now connect to it as an admin.")
                else:
                    print("ERROR: The supplied password is incorrect.")
            else:
                print("ERROR: The server does not have an administrator account.")
        else:
            print("ERROR: Invalid node.")
    else:
        div()
        print("login <IP Address> <password>")
        div()
        print("Runs `porthack` using a known admin password.")
        div()


class ISPNode(Node):
    def __init__(self, name="International ISP Hub", address="1.1.1.1"):
        super().__init__(name, address, address)
        self.blocklist = ["localhost", "jmail", "anonmail"]
        self.ports = [
            data.getPort(21),
            data.getPort(22),
            data.getPort(1433),
            data.getPort(80),
        ]
        self.minPorts = 4
        self.linked = ["shodan"]
        self.users = [User("admin", "potholes")]
        self.finalMissionState = False
        self.isAction = False

    def check_health(self):
        if not self.finalMissionState:
            return not self.hacked
        else:
            return "core.sys" in [x.name for x in self.flatten(self.files)]

    def main(self):
        div()
        print("This is the International ISP Hub.")
        print("It is important to the function of the Internet.")
        div()
    def main_hacked(self):
        player = data.getNode("localhost")
        cls()
        div()
        print("IIH Console")
        div()
        print("[1] Reassign IP Address")
        print("[ ] Delete Note")
        print("[0] Exit")
        div()
        try:
            ch = int(input(">"))
        except:
            return
        if ch == "1":
            clear()
            address = input("Address $")
            node = data.getNode(address, True)
            if not node:
                cls()
                div()
                print("ERROR: Invalid node.")
                br()
                return


class XOSMailAccount(Base):
    def __init__(self, address, password):
        super().__init__()
        self.address = address
        self.password = password
        self.secret_key = str(uuid.uuid4())


class XOSDevice(Node):
    def __init__(
        self,
        name,
        uid,
        address,
        notes=[],
        accounts=[],
        password="alpine",
        model="xphone",
        ):
        super().__init__(name, uid, address)
        self.users = [User("admin", password)]
        self.ports = [
            data.getPort(21),
            data.getPort(23),
            data.getPort(1443),
        ]
        self.minPorts = 4
        self.notes = notes
        self.accounts = accounts
        self.model = model
        self.battery_health = random.randint(60, 99)

    def main(self):
        div()
        print("ERROR: You cannot access this xOS device without the root password.")
        print("The root password is only known by xOS employees.")
        div()

    def main_hacked(self):
        print("xOS Console: HELP for a command list")
        while True:
            ch = input("admin@{} $".format(self.address))
            if ch == "help":
                div()
                print("help: command list")
                print("info: print device information")
                print("notes: lists all notes on the device.")
                print("accounts: list all email accounts saved to the device.")
                print("cls: clear the screen")
                print("exit: disconnect from host")
                div()
            elif ch in ["quit", "exit"]:
                return
            elif ch == "accounts":
                if self.accounts:
                    for account in self.accounts:
                        div()
                        print("Email Addr. {}".format(account.address))
                        print("Password: {}".format(account.password))
                        print("Secret Key: {}".format(account.secret_key))
                    div()
                else:
                    print("ERROR: No email accounts are saved to the device.")
            elif ch == "info":
                inf = data.XOS_DEVICES[self.model]
                div()
                print("Model: {}".format(inf.get("name", "Unknown Device")))
                print("CPU Freq: {}".format(inf.get("cpu", "Unreported")))
                print("Total Memory: {}".format(inf.get("ram", "Unreported")))
                print("Storage: {}".format(inf.get("storage", "Unreported")))
                print("Battery Capacity: {}".format(inf.get("battery", "Unknown")))
                print("Battery Health: {}%".format(self.battery_health))
                div()
            elif ch in ["clear", "cls"]:
                cls()
            elif ch == "notes":
                if self.notes:
                    div()
                    for note in self.notes:
                        print("* {}".format(note.text))
                    div()
                else:
                    print("ERROR: No notes have been stored on the device.")
            else:
                print("ERROR: Invalid command.")


class WikiPage(Base):
    def __init__(self, host, name):
        self.host = host
        self.name = name
    def read(self):
        cls()
        div()
        with open("wikis/{}/{}".format(self.host, self.name)) as f:
            print(f.read().replace("div()", "--------------------").rstrip("\n"))
        br()

class WikiCategory(Base):
    def __init__(self, host, name, pageMode=False):
        self.name = name
        self.host = host
        self.pages = []
        self.pageMode = pageMode
    def add_page(self, page):
        p = WikiPage(self.host, page)
        self.pages.append(p)
    def add_category(self, page, pageMode=False):
        p = WikiCategory(self.host, page, pageMode)
        self.pages.append(p)
        return p
    def read(self):
        while True:
            cls()
            div()
            print(self.name)
            if self.pageMode:
                div()
                with open("wikis/{}/{}".format(self.host, self.name)) as f:
                    print(f.read().replace("div()", "--------------------").rstrip("\n"))
            div()
            i = 1
            for page in self.pages:
                print("[{}] {}".format(i, page.name))
                i += 1
            div()
            try:
                ch = int(input("$"))
                if ch == 0:
                    return
                page = self.pages[ch-1].read()
            except:
                return


class WikiServer(Node):
    def __init__(self, name, uid, address, folder, homepage="Main Page", private=False, **kwargs):
        super().__init__(name, uid, address, **kwargs)
        self.ports = [data.getPort(22), data.getPort(80), data.getPort(1433)]
        self.minPorts = 3
        self.folder = folder
        self.homepage = WikiCategory(folder, homepage, True)
        self.private = private
    def main(self):
        if self.private and not self.login_screen():
            return
        try:
            self.homepage.read()
        except FileNotFoundError:
            print(traceback.format_exc())
            print(os.getcwd())
            print(self.folder)
    def mainold(self):
        with open("wikis/{}/{}".format(self.folder, self.homepage)) as f:
            for line in f.read().split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)
        while True:
            ch = input("{} #".format(self.name))
            if ch == "help":
                div()
                print("help: list commands")
                print("list: list all articles")
                print("read <article>: read an article")
                print("cls: clear the terminal")
                print("exit: disconenct from host")
                div()
            elif ch == "list":
                div()
                for item in os.listdir("wikis/{}".format(self.folder)):
                    print(item)
                div()
            elif ch == "read":
                div()
                print("read <article>")
                div()
                print("Read an article.")
            elif ch.startswith("read "):
                try:
                    with open("wikis/{}/{}".format(self.folder, ch[5:])) as f:
                        cls()
                        for line in f.read().split("\n"):
                            if line == "div()":
                                div()
                            else:
                                print(line)
                except:
                    print("ERROR: Invalid page name.")
            elif ch in ["quit", "exit"]:
                return
            elif ch in ["cls", "clear"]:
                cls()
            else:
                print("ERROR: Invalid command.")


class Mission(Base):
    def __init__(
        self,
        player,
        mission_id,
        name,
        target,
        start_email,
        end_email=None,
        reward=0,
        next_id=None,
        start_function=None,
        end_function=None,
        ):
        super().__init__()
        self.mission_id = mission_id
        self.name = name
        self.reward = reward
        self.start_email = start_email
        self.end_email = end_email
        self.target = target
        self.next_id = next_id
        self.player = player
        self.start_function = start_function
        self.end_function = end_function
        self.complete = False
    
    def clone(self):
        return type(self)(self.player, self.mission_id, self.name, self.target, self.start_email, self.end_email, self.reward, self.next_id, self.start_function, self.end_function)

    def start(self):
        sendEmail(self.start_email)
        self.player.currentMission = self
        if callable(self.start_function):
            self.start_function()

    def check_end(self):
        return data.getNode(self.target).hacked

    def end(self):
        if self.end_email:
            sendEmail(self.end_email)
        if self.next_id:
            self.player.currentMission = data.getMission(self.next_id, self.player)
            if self.player.currentMission:
                self.player.currentMission.start()
        else:
            self.player.currentMission = None
        self.player.creditCount += self.reward
        self.complete = True
        if callable(self.end_function):
            self.end_function()

class BlankMission(Mission):
    def check_end(self):
        return True

class LANMission(Mission):
    def __init__(self, player, mission_id, name, target, lanserver, start_email, end_email, next_id=None, start_function=None, end_function=None, reward=0):
        super().__init__(player, mission_id, name, target, start_email, end_email, next_id=next_id, start_function=start_function, end_function=end_function, reward=reward)
        self.lanserver = lanserver
    def check_end(self):
        def getNode(node, uid):
            for x in node.devices:
                if x.uid == uid or x.address == uid:
                    return x
        node = data.getNode(self.lanserver)
        subNode = getNode(node, self.target)
        if subNode:
            return subNode.hacked
    def clone(self):
        return LANMission(self.player, self.mission_id, self.name, self.target, self.lanserver, self.start_email, self.end_email, self.next_id, self.start_function, self.end_function, self.reward)

class NestedLANMission(Mission):
    def __init__(self, player, mission_id, name, target, lanserver, sublanserver, start_email, next_id=None, start_function=None, end_function=None, reward=0):
        super().__init__(player, mission_id, name, target, start_email, next_id=next_id, start_function=start_function, end_function=end_function, reward=reward)
        self.lanserver = lanserver
        self.sublan = sublanserver
    def check_end(self):
        def getNode(node, uid):
            for x in node.devices:
                if x.uid == uid or x.address == uid:
                    return x
        node = data.getNode(self.lanserver).getNode(self.sublan)
        subNode = getNode(node, self.target)
        if subNode:
            return subNode.hacked
    def clone(self):
        return LANMission(self.player, self.mission_id, self.name, self.target, self.lanserver, self.sublanserver, self.start_email, self.end_email, self.next_id, self.start_function, self.end_function, self.reward)

def mission_program(args, player):
    if player.currentMission:
        if player.currentMission.check_end():
            div()
            print("Congratulations! You finished the mission!")
            print(
                "You have been awarded {} credits.".format(player.currentMission.reward)
            )
            if player.currentMission.end_email:
                print("NOTE: An ending email has been sent. Read it.")
            if player.currentMission.next_id:
                print("NOTE: This mission's follow-up mission has been started.")
                print("Check your email for instructions.")
            div()
            player.currentMission.end()
        else:
            print("ERROR: Mission incomplete.")
            print("Check your email for instructions.")
    else:
        print("ERROR: No current mission.")


class ConnectMission(Mission):
    def check_end(self):
        return data.getNode(self.target).visited


class NMapMission(Mission):
    def check_end(self):
        return data.getNode(self.target).nmap


def logview(args):
    if args:
        for arg in args:
            div()
            print("Trying {}...".format(arg))
            node = data.getNode(arg)
            if node:
                if node.hacked:
                    if node.logs:
                        for log in node.logs:
                            print("* {}: {}".format(log.address, log.text))
                    else:
                        print("No logs for provided node.")
                else:
                    print("ERROR: Access denied.")
            else:
                print("ERROR: Invalid node.")
        div()
    else:
        div()
        print("logivew <IP Address>")
        div()
        print("Views the logs of a node.")
        print("The node must be already hacked for this to work.")
        div()


class MissionServer(Node):
    def __init__(self, name, uid, address, missions=[]):
        super().__init__(name, uid, address)
        self.ports = [data.getPort(22), data.getPort(1433), data.getPort(23)]
        self.users = [User("admin")]
        self.minPorts = 4
        self.main_hacked = self.main
        self.missions = missions
    
    def main(self):
        self.player = data.getNode("localhost")
        self.missions = [x for x in self.missions if not x.complete]
        print("Welcome.")
        print("There are {} contracts available.".format(len(self.missions)))
        print("For a command list, type HELP.")
        while True:
            ch = input("{} #".format(self.name))
            if ch == "help":
                div()
                print("help: command list")
                print("cls: clear terminal")
                print("list: lists all available missions")
                print("current: displays the current mission")
                print("accept <id>: accept a mission.")
                print("cancel: cancel the current mission")
                print("exit: disconnect from host")
                div()
            elif ch in ["clear", "cls"]:
                cls()
            elif ch == "accept":
                div()
                print("accept <id>")
                div()
                print("Accept a mission.")
                div()
            elif ch.startswith("accept "):
                try:
                    index = int(ch[7:])
                    if not self.player.currentMission:
                        if 0 <= index <= len(self.missions):
                            self.player.currentMission = self.missions[index]
                            self.missions.pop(index)
                            self.player.currentMission.start()
                            print("Accepted mission.")
                            print("An email has been sent to your inbox.")
                        else:
                            print("ERROR: Invalid mission index.")
                    else:
                        print("ERROR: A mission has already been accepted.")
                        print("Complete it or cancel it first.")
                except Exception as e:
                    print("ERROR: {}".format(e))
            elif ch == "cancel":
                if self.player.currentMission:
                    rejects = data.getNode("rejected")
                    rejects.missions.append(self.player.currentMission.clone())
                    self.player.currentMission = None
                    print("Cancelled the mission.")
                    print("To start the mission again: rejects.rehack.org")
                else:
                    print("ERROR: No mission to cancel.")
            elif ch == "current":
                if self.player.currentMission:
                    div()
                    print("Name: {}".format(self.player.currentMission.name))
                    print("Reward: {} Cr.".format(self.player.currentMission.reward))
                    div()
                else:
                    print("No current mission.")
            elif ch in ["ls", "list"]:
                if self.missions:
                    i = 0
                    for mission in self.missions:
                        print(
                            "{}: {} ({:,} Cr.)".format(i, mission.name, mission.reward)
                        )
                        i += 1
                else:
                    print("There are no contracts available on this server.")
            elif ch in ["quit", "exit"]:
                return
            elif ch == "":
                continue
            else:
                print("ERROR: Invalid command.")


class BuyMission(Mission):
    def check_end(self):
        def is_sublist(sublist, main_list):
            n = len(sublist)
            return any(main_list[i:i+n] == sublist for i in range(len(main_list) - n + 1))
        return is_sublist(self.target, [x.name for x in data.PROGRAMS if x.unlocked])


def nodecheck(args):
    d = {
        Node: "standard",
        WebServer: "website",
        MailServer: "mailserver",
        WikiServer: "wiki",
        MessageBoard: "messageboard",
        JmailServer: "jmail",
        AnonMail: "anonmail",
        MailDotCom: "maildotcom",
        XOSDevice: "xos",
        MissionServer: "contract_hub",
        VersionControl: "version_control",
        type(None): "invalid",
        SignupService: "signup",
        VersionControl: "version_control",
        BankServer: "bank",
        BankBackEnd: "bank_backend",
        LocalAreaNetwork: "router",
        Forwarder: "forwarder",
        TorForwarder: "forwarder",
        TimeServer: "time_server",

    }
    if args:
        for arg in args:
            node = type(data.getNode(arg, True))
            print("{}: {}".format(arg, d.get(node, "unknown")))
    else:
        div()
        print("nodecheck [list of ip addresses]")
        div()
        print("Shows a node's type.")
        div()


def getEmails(account):
    return account.inbox


def mailman_base(args, player):
    if len(args) == 2:
        try:
            account = args[0]
            passwd = args[1]
            parts = account.split("@")
            node = data.getNode(parts[1])
            if isinstance(node, MailServer):
                node.client(parts[0], passwd, player)
            else:
                print("ERROR: Invalid mail server.")
        except Exception as e:
            print(f"ERROR: {e}")
    elif args == ["list"]:
        if player.saved_accounts:
            div()
            for item in player.saved_accounts.keys():
                print("{}".format(item))
            div()
        else:
            print("ERROR: No saved accounts.")
            print("To save an account, log in with mailman and run the `save` command.")
    elif len(args) == 1:
        try:
            email = args[0]
            passwd = player.saved_accounts[email]
            mailman_base([email, passwd], player)
        except KeyError:
            print("ERROR: You have not saved the email address.")
    else:
        div()
        print("mailman <email address> [password]")
        div()
        print("Email client.")
        div()
        print("mailman list: show list of saved accounts. If you have saved an email account, you do not need to enter the password.")
        div()

def tormail(args, player):
    if len(args) == 2:
        try:
            account = args[0]
            passwd = args[1]
            parts = account.split("@")
            if len(parts) != 2:
                print("ERROR: Invalid email account format.")
                return
            node = data.getTorNode(parts[1])
            if isinstance(node, MailServer):
                node.client(parts[0], passwd, player)
            else:
                print("404: Mail Server Not Found.")
        except:
            print(traceback.format_exc())
    elif len(args) == 1:
        try:
            email = args[0]
            passwd = player.saved_accounts[email]
            tormail([email, passwd], player)
        except:
            print("ERROR: That account is not saved.")
    else:
        div()
        print("tormail <email address> [password]")
        div()
        print("Tor email client.")
        div()
        print("mailman list: list all saved email addresses.")

def bruter(args, player):
    if args:
        for item in args:
            print("TRY: {}".format(item))
            node = data.getNode(item)
            if node:
                account = None
                for x in node.users:
                    if x.name == "admin":
                        account = x
                if account:
                    found = False
                    for passwd in data.PASSLIST:
                        node.create_log(player.address, "Attempted admin login")
                        if account.password == passwd:
                            print("Found password: {}".format(passwd))
                            program = None
                            for x in data.PROGRAMS:
                                if x.name == "login":
                                    program = x
                            if program:
                                program.execute([item, passwd])
                            found = True
                            break
                    if not found:
                        print("ERROR: Could not find password.")

                else:
                    print("ERROR: No admin account.")

            else:
                print("ERROR: Invalid node.")
    else:
        div()
        print("bruter [list of IP addresses]")
        div()
        print("Brute-forces the password of a server.")
        div()


def emailbruter(args, player):
    if args:
        for item in args:
            print("TRY: {}".format(item))
            parts = item.split("@")
            if len(parts) == 2:
                node = data.getNode(parts[1])
                if type(node) in [MailServer, MailDotCom, JmailServer, AnonMail]:
                    account = None
                    for acc in node.accounts:
                        if acc.name == parts[0]:
                            account = acc
                    if account:
                        if account.password:
                            found = False
                            for passwd in data.PASSLIST:
                                node.create_log(
                                    player.address,
                                    "Attempted account login for {}".format(
                                        account.name
                                    ),
                                )
                                if account.password == passwd:
                                    print("Found password: {}".format(passwd))
                                    player.saved_accounts[item] = passwd
                                    node.create_log(
                                        player.address,
                                        "Logged into account {}".format(account.name),
                                    )
                                    found = True
                                    break
                            if not found:
                                print("ERROR: Could not find password.")
                        else:
                            print("ERROR: Specified account is disabled.")
                    else:
                        print("ERROR: Invalid account")
                else:
                    print("ERROR: 404 Not Found")
            else:
                print("ERROR: Invalid email account.")
    else:
        div()
        print("emailbruter [list of email addresses]")
        div()
        print("Brute-forces the password of a mail account.")
        print("TIP: If you only know the IP of a server, try admin@<ip")
        div()


class GitServer(Node):
    def __init__(self, name, uid, address, ports=[], minPorts=0):
        super().__init__(name, uid, address, ports=ports, minPorts=minPorts)
        self.entries = []

    def add_entry(self, body, ip="127.0.0.1"):
        self.entries.append({"text": body, "origin": ip})

    def main_hacked(self):
        div()
        print(self.name)
        div()
        if self.entries:
            for item in self.entries:
                print("* {} ({})".format(item["body"], item["origin"]))
        else:
            print("No commits since 1/1/1970.")
        div()


class MasterVPS(Node):
    def __init__(self, player):
        super().__init__(
            "MasterVPS Central Server", "mastervps_central", "mastervps.service"
        )
        self.ports = [data.getPort(21), data.getPort(22), data.getPort(23)]
        self.minPorts = 2**16
        self.playerPlease = True
        self.main_hacked = self.main
        self.currentId = 2 ** 14
        self.currentId -= (2**random.randint(1,11))
        self.offerings = [
            {
                "name": "Basic",
                "node": Node("","","",ports=[data.getPort(22),data.getPort(6881)]),
                "description":"A basic node with no security.",
                "price":500,
                "secure": False,
            },
            {
                "name": "Basic+",
                "node": Node("","","",ports=[data.getPort(22),data.getPort(6881)], minPorts=2**16),
                "description":"A basic node with full security, including a firewall.",
                "price":750,
                "secure": True,
            },
            {
                "name": "FTP Server",
                "node": FTPServer("", "", ""),
                "description":"A server to drop your files",
                "price": 1000,
                "secure": False,
            },
            {
                "name": "FTP Server+",
                "node": FTPServer("", "", ""),
                "description": "A more secure FTP server",
                "price": 1500,
                "secure": True,
            },
            {
                "name": "xPhone",
                "node":XOSDevice("","",""),
                "description":"A standard xPhone 3.",
                "price":300,
                "secure": False,
            },
            {
                "name": "Mail Server",
                "node":MailServer("","","",player),
                "description":"A fully-fledged mail server.",
                "price":1500,
                "secure": False,
            },
            {
                "name": "Mail Server+",
                "node":MailServer("","","",player, hideLookup=True, minPorts=2**16),
                "description":"A fully-fledged mail server with full security.",
                "price":2500,
                "secure": True,
            },
        ]
        self.buckets = []
    def spinup(self, player):
        cls()
        div()
        i = 1
        for o in self.offerings:
            print("[{}] {} ({} Cr.)".format(i, o["name"], o["price"]))
            print("  {}".format(o["description"]))
            i += 1
        div()
        try:
            ch = int(input("$"))
            if ch == 0:
                return
            node = self.offerings[ch-1]
            if player.creditCount >= node["price"]:
                passwd = data.getPassword()
                player.creditCount -= node["price"]
                bucket = copy.deepcopy(node["node"])
                bucket.uid = "mastervps_{}".format(random.randint(1, 2**64))
                bucket.address = data.generateIP()
                bucket.users = [User("admin", passwd)]
                bucket.offering = node["name"]
                if node["secure"]:
                    bucket.firewall = Firewall(data.genString(16), 16)
                    bucket.minPorts = 65536
                data.NODES.append(bucket)
                self.buckets.append(bucket)
                sendEmail(Email("null@null.null", "mastervps-logs@jmail.com", node["name"], bucket.address))
                div()
                print("Success!")
                div()
                print("IP Address: {}".format(bucket.address))
                br()
            else:
                cls()
                div()
                print("ERROR: Not enough credits.")
                br()
        except ValueError:
            return
    def manage(self, player, node):
        cls()
        div()
        print("{} @ {}".format(node.offering, node.address))
        div()
        print("[1] Change Admin Password")
        print("[2] Spin-Down ({} Refund)".format("Full" if node.visited else "No"))
        div()
        ch = input("$")
        if ch == 1:
            for user in node.users:
                if user.name == "admin":
                    user.password = data.getPassword()
        elif ch == "2":
            data.NODES.remove(node)
            self.buckets.remove(node)
            if not node.visited:
                player.creditCount += self.offerings[node.offering]["price"]
            cls()
            div()
            print("Node spun down.")
            if not node.visited:
                print("Because the node was never used, a full refund has been credited to your account.")
            br()
    def manageBase(self, player):
        cls()
        div()
        print("My Buckets")
        div()
        for node in self.buckets:
            print("{} @ {}".format(node.offering, node.address))
        br()
    def main(self, player):
        while True:
            cls()
            div()
            print("Balance: {} Cr.".format(player.creditCount))
            div()
            print("[1] New Bucket...")
            if self.buckets:
                print("[2] My Buckets")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "0":
                return
            elif ch == "1":
                self.spinup(player)
            elif ch == "2" and self.buckets:
                self.manageBase(player)

def firewall(args):
    if "test" in args and len(args) == 2:
        node = data.getNode(args[1], True)
        if node:
            if node.firewall:
                print("Firewall active.")
            else:
                print("Firewall inactive.")
        else:
            print("ERROR: Invalid IP address.")
    elif "crack" in args and len(args) == 2:
        node = data.getNode(args[1], True)
        if node:
            if node.firewall:
                guessed_letters = 0
                while guessed_letters < len(node.firewall.solution):
                    s = ""
                    i = 0
                    for x in range(guessed_letters):
                        s += node.firewall.solution[i]
                        i += 1
                    for x in range(len(node.firewall.solution) - guessed_letters):
                        s += "*"
                    print("Solution: {}\r".format(s))
                    time.sleep(node.firewall.time)
                    guessed_letters += 1
                print("Solution: {}".format(node.firewall.solution))
                firewall(["solve", node.address, node.firewall.solution])
            else:
                print("ERROR: No firewall active.")
        else:
            print("ERROR: Invalid IP address.")
    elif "solve" in args and len(args) == 3:
        node = data.getNode(args[1], True)
        if node:
            if node.firewall:
                if node.firewall.solution == args[2]:
                    print("SUCCESS: Firewall disabled.")
                    node.firewall = None
                else:
                    print("ERROR: Incorrect solution.")
            else:
                print("ERROR: No firewall active.")
        else:
            print("ERROR: Invalid IP address.")
    else:
        div()
        print("firewall [args]")
        div()
        print("firewall test <IP address>: check if a firewall is present and active")
        print("firewall crack <IP address>: crack a firewall solution")
        print("firewall solve <IP address> <solution>: solve a firewall")
        div()
class Sweeper:
    def __init__(self):
        self.nodes = []

    def sweep_range(self, a, b):
        for c in range(256):
            for d in range(256):
                node = data.getNode(f"{a}.{b}.{c}.{d}")
                if node:
                    self.nodes.append(node)
                if [a, b, c, d] == [255, 255, 255, 255]:
                    return True  # Indicate that stopping condition is met
        return False  # Stopping condition not met

    def sweep(self):
        print("Begin sweep...")
        stop_sweep = False

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for a in range(256):
                for b in range(256):
                    print("Begin {}.{}.x.x".format(a, b))
                    future = executor.submit(self.sweep_range, a, b)
                    if future.result():
                        stop_sweep = True
                        break
                if stop_sweep:
                    break

        print("Finished sweep.")
        if self.nodes:
            for node in self.nodes:
                print("{}: {}".format(node.address, node.name))
        else:
            print("No nodes found.")

def sweep(args):
    sweeper = Sweeper()
    sweeper.sweep()

class GlobalDNS(Node):
    def __init__(self):
        super().__init__("Global DNS Service", "gdns", "8.8.8.8",minPorts=2**16,ports=[data.getPort(65536)])
    def main(self):
        print("This is the Global DNS Server.")
        print("It is important for the function of the Internet.")

class VersionControl(Node):
    def __init__(self, name, uid, address, commits = [], publicView=False, *args, **kwargs):
        super().__init__(name, uid, address, ports=[data.getPort(1433),data.getPort(80),data.getPort(22),data.getPort(21)],minPorts=4, *args, **kwargs)
        self.commits = [Commit("Initial commit", "127.0.0.1")] + [x for x in commits if isinstance(x,Commit)]
        self.hacked = publicView
    def main(self):
        print("This is a Git server.")
        print("Git is a version control system that allows developers to collaborate")
        print("and review, merge, roll back, and much more, changes to source code.")
        div()
        print("403: This server does not permit public viewing of commits.")
        div()
    def main_hacked(self):
        if self.commits:
            div()
            print("Commit History for {}".format(self.name))
            div()
            for x in self.commits:
                print("* {}".format(x))
            div()
        else:
            div()
            print("ERROR: No commit history.")
            div()

def save(args, player):
    try:
        player.save()
    except:
        print(traceback.format_exc())

def filterDomainSafeCharacters(inputString):
    return ''.join(re.findall(r'[a-z0-9\-_]', inputString.lower()))

class DomainExpert(Node):
    def __init__(self):
        super().__init__("DomainExpert Admin Panel","dexpertmain","service.domain.expert")
        self.ports = [data.getPort(22),data.getPort(80),data.getPort(1433)]
        self.minPorts = 2**16
        self.firewall = Firewall(makeRandomString(),15)
        self.playerPlease = True
        self.domains = []
        self.pricing = {
            "com":100,
            "org":150,
            "net":200,
            "mail":350,
            "me":50,
            "uk":150,
            "us":165,
            "fail":75,
        }
    def main(self, player):
        print("Welcome. Type 'help' for a command list.")
        while True:
            ch = input("DomainExpert #")
            args = ch.split(" ")
            if ch in ["help","?"]:
                div()
                print("help: prints help")
                print("opt: list all domain offerings")
                print("list: list all owned domains")
                print("balance: prints balance")
                print("purchase <domain>: purchase a domain")
                print("assign <domain> <IP address>: assign a purchased domain to a MasterVPS node")
                print("exit: disconenct from host")
                div()
            elif ch == "":
                continue
            elif ch == "nodes":
                node = data.getNode("mastervps_central")
                if node.buckets:
                    div()
                    for x in node.buckets:
                        print("{} ({})".format(x.address,x.offeringType))
                    div()
                else:
                    div()
                    print("No purchased nodes.")
                    print("Purchase a node from 'mastervps.me'.")
                    div()
            elif ch == "assign":
                div()
                print("assign <domain> <ip address>")
                div()
                print("Assign an owned domain to a MasterVPS node.")
                print("Run 'nodes' for a list.")
            elif "assign" in args and len(args) == 3:
                master = data.getNode("mastervps_central")
                if args[1] in [x.getName() for x in self.domains]:
                    if args[2] in [x.address for x in master.buckets]:
                        d = [x for x in self.domains if x.getName() == args[1]][0] ## Hacky workaround because the normal way doesn't work.
                        node = data.getNode(args[2])
                        d.addr = copy.copy(node.address)
                        node.address = d.getName()
                        print("Successfully connected {} to {}.".format(args[2],args[1]))

                    else:
                        print("ERROR: Invalid IP address.")
                else:
                    print("ERROR: Invalid domain.")
            elif ch == "purchase":
                div()
                print("purchase <domain>")
                div()
                print("Purchase a domain.")
                div()
            elif ch.startswith("purchase "):
                ch = ch[9:]
                dom = ch.split(".")
                if len(dom) == 2:
                    if dom[1] in self.pricing.keys():
                        if player.creditCount >= self.pricing[dom[1]]:
                            node = data.getNode(".".join(dom))
                            if node:
                                print("ERROR: Domain is already taken.")
                            else:
                                player.creditCount -= self.pricing[dom[1]]
                                d = Domain(dom[0], dom[1])
                                self.domains.append(d)
                                print("Successfully purchased {} for {} Cr.".format(".".join(dom),self.pricing[dom[1]]))
                        else:
                            print("ERROR: Cannot afford domain of this type.")
                    else:
                        print("ERROR: Invalid domain ending.")
                        print("For a list, type 'opt'.")
                else:
                    print("ERROR: Format must be <name>.<ending>.")
            elif ch == "list":
                if self.domains:
                    for x in self.domains:
                        n = ".".join([x.name,x.base])
                        if x.assign:
                            print("{} --> {}".format(n,x.assign))
                        else:
                            print("{} (Unassigned)".format(n))
                else:
                    print("No owned domains.")
            elif ch in ["clear","cls"]:
                cls()
            elif ch == "opt":
                div()
                for item in self.pricing:
                    print("{}: {} Cr.".format(item, self.pricing[item]))
                div()
            elif ch in ["quit","exit"]:
                return
            elif ch in ["bal","balance"]:
                print("{} Cr.".format(player.creditCount))
            else:
                print("ERROR: Invalid command.")
    def main_hacked(self, player):
        print("ERROR: The admin panel has been disabled by the site administrator.")

def tor(args, player):
    if args == ["history"]:
        history = [x for x in data.TOR_NODES if x.visited]
        for node in history:
            print("{}: {}".format(node.name, node.address))
        if not history:
            print("No history to show.")
    elif args:
        for arg in args:
            node = data.getTorNode(arg)
            if node:
                node.visited = True
                if node.hacked and "main_hacked" in dir(node):
                    if item.playerPlease:
                        node.main_hacked(player)
                    else:
                        node.main_hacked()
                else:
                    if node.playerPlease:
                        node.main(player)
                    else:
                        node.main()
                node.visited = True
            else:
                print("ERROR: Onionsite '{}' not found.".format(arg))
    else:
        div()
        print("tor [onionsite]")
        div()
        print("Connects to a Tor node.")
        div()

class SignupService(Node):
    def __init__(self, uid, address, agent_id, usernames=True, junkMail = [], usePlayerName=False, signup_function=None, private=[]):
        super().__init__("Signup Service", uid, address, ports=[data.getPort(80), data.getPort(21), data.getPort(22)], minPorts=65536)
        self.name = "Signup Service"
        self.agent_id = agent_id
        self.usernames = usernames
        self.junkMail = junkMail
        self.playerPlease = True
        self.usePlayerName = usePlayerName
        self.private = private
        self.signup_function = signup_function
        self.enabled = True
    def disable(self):
        self.enabled = False
    def enable(self):
        self.enabled = True
    def get_node(self, address):
        return data.getAnyNode(address)

    def send_mail(self, username):
        address = data.getNode(self.agent_id).address
        for email in [copy.deepcopy(x) for x in self.junkMail]:
            email.receiver = "{}@{}".format(username, address)
            sendEmail(email)
    def main(self, player):
        node = self.get_node(self.agent_id)
        if not self.enabled:
            print("ERROR: This signup service has been disabled by the admin.")
            return
        if self.private:
            private = [data.getAnyNode(x).address for x in self.private]
            print("This signup service is configured to only accept allowed members.")
            print("This is enforced using an email address check.")
            eml = input("Email address $")
            if not eml:
                eml = "{}@jmail.com".format(player.name)

            domain = eml.split("@")[1]
            if domain not in private:
                print("ERROR: Your email address provider is not in the whitelist.")
                return
            elif eml not in player.saved_accounts.keys():
                print("ERROR: You have not saved that email account in your OS keyring.")
                print("To do this, log into that account with your email client and run `save`.")
                return
        if not node:
            print("404 Not Found")
            return
        print("Welcome to the signup server for {}.".format(node.name))

        if self.usePlayerName:
            username = player.name
        elif not self.usernames:
            username = data.genString(16)
        else:
            username = "" 
        while not username:
            username = input("Enter Your Username $")
            if not username:
                print("ERROR: Must type a username.")
            if username in [x.name for x in node.users]:
                print("ERROR: That user already exists.")
                username = ""
                if self.usePlayerName:
                    return

        password = ""
        while not password:
            password = getpass.getpass("Enter a password $")
            if not password:
                print("ERROR: You must type a password.")
        node.create_user(username, password)
        print("Successfully added user.")
        if isinstance(node, MailServer):
            print("Your email address is: {}@{}".format(username, node.address))
            self.send_mail(username)
        else:
            print("Your username is: {}".format(username))
            print("The service URL is: {}".format(node.address))
        print("Your password is: [HIDDEN]")
        if callable(self.signup_function):
            self.signup_function()
    def main_hacked(self, player):
        cls()
        print("Apache Forwarder v1.0: Console")
        while True:
            args = input("$").split(" ")
            if args == ["help"]:
                print("Command help:")
                print("node: display URL of the node connected")
                print("wl: list all whitelisted email domains")
                print("wl <email domain>: add/remove an email domain to the whitelist")
            elif args == []:
                pass
            else:
                print("ERROR: Run `help` for a command list.")


class LocalAreaNetwork(Node):
    def __init__(self, name, uid, address, minPorts=2, **kwargs):
        super().__init__(name, uid, address, ports = [data.getPort(1), data.getPort(22)], minPorts=minPorts, **kwargs)
        self.devices = []
        self.devices += [Router(self.devices)]
        self.alive = True
        self.locked = False
    def tick(self):
        for node in self.devices:
            node.tick()
    def check_health(self):
        return self.alive
    def add_device(self, device):
        if not self.locked:
            self.devices.append(device)
    def main(self):
        if self.hacked:
            print("ERROR: A LAN client such as `lanconnect` is required to connect to a LAN router and access its network.")
        else:
            print("ERROR: Access denied.")
    def getNode(self, uid):
        for node in self.devices:
            if node.uid == uid or node.address == uid:
                return node

    def generateIP(self):
        iplist = [x.address for x in self.devices]
        nums = [0, 1]
        nums[1] += len(iplist)
        while nums[1] > 255:
            nums[0] += 1
            nums[1] -= 255

        return "192.168.{}.{}".format(nums[0], nums[1])

class RemoteLAN(LocalAreaNetwork):
    """
    A subclass of LocalAreaNetwork that allows users to log in and connect to the LAN.
    Note that each user gets the same LAN connection (for now, probably).
    """
    def main(self):
        if self.login_screen():
            LANConnect([], data.getNode("player"), True)(self, data.getNode("player"))


class Router(Node):
    def __init__(self, devices):
        super().__init__("Router", "router", "192.168.0.0", ports=[data.getPort(80), data.getPort(22)])
        self.hacked = True
        self.ports = [data.getPort(1)]
        self.ports[0].open = True
        self.devices = devices
    def main_hacked(self):
        div()
        print("ADDR\t\tHOSTNAME")
        div()
        for x in [x for x in self.devices if x.check_health()]:
            print("{}\t\t{}".format(x.address, x.name))
        div()
def LANConnect(args, player, returnMode=False):
    def main(node, player):
        def ssh(node):
            if node.hacked and data.checkPort(node, 22):
                CONNECT.connect(node)
            else:
                print("ERROR: Access denied.")
        def ftp(node):
            if node.hacked and data.checkPort(node, 21):
                folderView(data.createFolder(node), True)
            elif data.checkPort(node, 21) and node.readAccess:
                folderView(data.createFolder(node))
            else:
                print("ERROR: Access denied.")
        def hack(node):
            if not node:
                print("ERROR: Invalid address.")
                return
            if node.minPorts > len([x for x in node.ports if x.open]):
                print("ERROR: Too few open ports.")
                return
            print("INSTALLING EXPLOIT...")
            time.sleep(2.5 / (len(node.ports) + 1))
            print("EXPLOIT INSTALLED.")
            node.hacked = True
        def nmap(node):
            if not node:
                print("ERROR: Invalid address.")
                return
            div()
            print("Hostname: {}".format(node.name))
            print("Exposed Ports: {}".format(len(node.ports)))
            print("Min. Ports To Crack: {}".format(node.minPorts))
            if node.hacked:
                print("ROOT ACCESS ACQUIRED")
            if node.ports:
                div()
                print("PORT\tSTATE\tNAME")
                div()
                for p in node.ports:
                    print("{}\t{}\t{}".format(p.num, "OPEN" if p.open else "CLOSED", p.name))
            div()
        def connect(node, player):
            if node.hacked and "main_hacked" in dir(node):
                if node.playerPlease:
                    node.main_hacked(player)
                else:
                    node.main_hacked()
            else:
                if node.playerPlease:
                    node.main(player)
                else:
                    node.main()
        def getNode(node, address):
            for x in node.devices:
                if x.address == address:
                    return x
        def breakPort(node, num):
            if not node:
                print("ERROR: Invalid address.")
                return
            for port in node.ports:
                if port.num == num:
                    print("ATTACKING PORT {}...".format(num))
                    time.sleep(2.5 / len(node.ports) + 1)
                    port.open = True
                    print("SUCCESSFULLY ATTACKED PORT.")
                    return

        programs = sorted([x.name for x in data.PROGRAMS if x.unlocked])
        unlocked = {}
        for x in ["porthack", "sshkill", "ftpkill", "webworm", "nmap", "lancrack", "ftp", "ssh", "irc"]:
            unlocked[x] = x in programs
        cls()
        print("Welcome to {}.".format(node.name))
        print("For a command list, type HELP.")
        while True:
            ch = input("{} $".format(node.address))
            if ch == "":
                pass
            elif ch in ["clear","cls"]:
                cls()
            elif ch == "debug":
                for x in node.devices:
                    print("{}".format(x.address))
            elif ch == "info":
                print(unlocked)
                print(programs)
            elif ch == "sshkill" and unlocked["sshkill"]:
                div()
                print("sshkill <address>")
                div()
                print("Breaks port 22 for <address>.")
                div()
            elif ch.startswith("sshkill ") and unlocked["sshkill"]:
                ch = ch[8:]
                target = getNode(node, ch)
                breakPort(target, 22)
            elif ch == "ftpkill" and unlocked["ftpkill"]:
                div()
                print("ftpkill <address>")
                div()
                print("Breaks port 21 for <address>.")
                div()
            elif ch.startswith("ftpkill ") and unlocked["ftpkill"]:
                ch = ch[8:]
                target = getNode(node, ch)
                breakPort(target, 21)            
            elif ch == "webworm" and unlocked["webworm"]:
                div()
                print("webworm <address>")
                div()
                print("Breaks port 80 for <address>.")
                div()
            elif ch.startswith("webworm ") and unlocked["webworm"]:
                ch = ch[8:]
                target = getNode(node, ch)
                breakPort(target, 80)
            elif ch == "connect":
                div()
                print("connect <address>")
                div()
                print("Connects to a node.")
                div()
            elif ch.startswith("connect "):
                target = getNode(node, ch[8:])
                if target:
                    connect(target, player)
                else:
                    print("ERROR: Invalid hostname.")
            elif ch == "nmap":
                div()
                print("nmap <address>")
                div()
                print("Lists all open ports on <address> as well as other related info.")
                div()
            elif ch.startswith("nmap "):
                ch = ch[5:]
                target = getNode(node, ch)
                nmap(target)
            elif ch == "porthack":
                div()
                print("porthack <address>")
                div()
                print("Uses open ports to gain admin access to <address>.")
                div()
            elif ch.startswith("porthack "):
                ch = ch[9:]
                hack(getNode(node, ch))
            elif ch == "lancrack" and unlocked["lancrack"]:
                div()
                print("lancrack <address>")
                div()
                print("Tool for breaking port 1.")
                div()
            elif ch.startswith("lancrack ") and unlocked["lancrack"]:
                ch = ch[9:]
                breakPort(getNode(node, ch), 1)
            elif ch == "help":
                topics = ["help", "clear", "connect", "lanconnect"] + [x for x in unlocked.keys() if unlocked[x]] + ["exit"]
                div()
                print("\n".join(topics))
                div()
            elif ch == "lanconnect":
                div()
                print("lanconnect <address>")
                div()
                print("Connect to a LAN within the current LAN.")
                div()
            elif ch.startswith("lanconnect "):
                ch = ch[11:]
                n = getNode(node, ch)
                if isinstance(n, LocalAreaNetwork):
                    LANConnect(n, player)
                else:
                    print("ERROR: Invalid hostname.")
            elif ch == "ftp" and unlocked["ftp"]:
                div()
                print("ftp <address>")
                div()
                print("Browses files over FTP.")
                div()
            elif ch.startswith("ftp ") and unlocked["ftp"]:
                n = getNode(node, ch[4:])
                if n:
                    ftp(n)
                else:
                    print("ERROR: Invalid address.")
            elif ch == "ssh" and unlocked["ssh"]:
                div()
                print("ssh <address>")
                div()
                print("Run commands over SSH.")
                div()
            elif ch.startswith("ssh ") and unlocked["ssh"]:
                n = getNode(node, ch[4:])
                if n:
                    ssh(n)
                else:
                    print("ERROR: Invalid address.")
            elif ch == "irc":
                div()
                print("irc <server>")
                div()
                print("IRC Client.")
                div()
            elif ch.startswith("irc "):
                n = getNode(node, ch[4:])
                if n:
                    irclogin(n)
                else:
                    print("ERROR: Invalid address.")
            elif ch in ["quit","exit"]:
                return
            else:
                print("ERROR: Invalid program.")


    def findNode(address):
        for n in data.NODES:
            if n.address == address:
                return n
    if returnMode:
        return main
    if isinstance(args, LocalAreaNetwork):
        if not args.hacked:
            print("ERROR: Access denied.")
            # return
        main(args, player)
    elif len(args) == 1:
        if isinstance(args, Node):
            pass
        else:
            node = findNode(args[0])
        if not node:
            print("ERROR: Invalid address.")
            return 
        if not isinstance(node, LocalAreaNetwork):
            print("ERROR: The network is not a LAN.")
            return
        if not node.hacked:
            print("ERROR: Access denied.")
            return
        main(node, player)

    else:
        div()
        print("lanconnect <ip address>")
        div()
        print("Connects to a LAN and pretends to be a device on it, while remaining hidden.")
        div()

class NodeTrackerNode(Base):
    def __init__(self, address, hostname):
        self.address = address
        self.hostname = hostname

class NodeTrackerLanNode(Base):
    def __init__(self, lan_address, address, hostname):
        self.lan_address = lan_address
        self.address = address
        self.hostname = hostname

class NodeTrackerTorNode(Base):
    def __init__(self, address, hostname):
        self.address = address
        self.hostname = hostname

class NodeTracker(Node):
    def __init__(self, name, uid, address):
        super().__init__(name, uid, address)
        self.nodes = []
    def add_node(self, uid):
        if isinstance(uid, Node):
            n = uid
        else:
            n = data.getNode(uid)
        nt = NodeTrackerNode(n.address, n.name)
        self.nodes.append(nt)
    def add_lan_node(self, lan_uid, uid):
        lan = data.getNode(lan_uid)
        node = lan.getNode(uid)
        self.nodes.append(NodeTrackerLanNode(lan.address, node.address, node.name))
    def add_tor_node(self, uid):
        if isinstance(uid, Node):
            n = uid
        else:
            n = data.getTorNode(uid)
        self.nodes.append(NodeTrackerTorNode(n.address, n.name))
    def main(self):
        print("This is a Node Tracker. Node Tracker registers a list of IP addresses and watches them to keep track of them.")
        print("It is used all around the Intelligence Community (and outside of it) for many purposes, including:")
        print("- Maintaining lists of employee LAN's in a company")
        print("- Keeping an internal directory of important servers without running a web server, which requires more maintenance")
        print("- Surveillance of foreign military cyber-targets")
        print("(c) 2010 Central Intelligence Agency, all rights reserved.")
    def main_hacked(self):
        for node in self.nodes:
            if isinstance(node, NodeTrackerNode):
                print("# {} --> {}".format(node.hostname, node.address))
            elif isinstance(node, NodeTrackerLanNode):
                print("# {} --> {} --> {}".format(node.hostname, node.lan_address, node.address))
            elif isinstance(node, NodeTrackerTorNode):
                print("# {} --> {}".format(node.hostname, node.address))


class BankTransfer(Base):
    def __init__(self, fromAcc, toAcc, fromBank, toBank, amount):
        self.fromAcc = fromAcc
        self.toAcc = toAcc
        self.fromBank = fromBank
        self.toBank = toBank
        self.amount = amount
    def __str__(self):
        return "Account {} (Bank={}) transferred {:,} Cr. to account {} (Bank={})".format(self.fromAcc, self.fromBank, self.amount, self.toAcc, self.toBank)
class BankAccount(Base):
    def __init__(self, ip, number, pin, balance):
        self.ip = ip
        self.number = number
        self.pin = pin
        self.balance = balance
        self.transactions = []
    def __str__(self):
        return "Account {} (Origin={}; Balance={:,} Cr.)".format(self.number, self.ip, self.balance)
    def check(self, number, pin):
        return self.number == number and self.pin == pin

class BankBackEnd(Node):
    def __init__(self, name, uid, address):
        super().__init__(name, uid, address)
        self.accounts = [BankAccount(self.address, 000000, self.gen_pin(), 0)]
    def get_next_num(self):
        nums = [x.number for x in self.accounts]
        running = True
        while running:
            num = random.choice(range(11111111,99999999))
            running = num in nums # Ensures no duplicates
        return num
    def gen_pin(self):
        s = ''
        for x in range(6):
            s += random.choice(list("1234567890"))
        return s
    def get_account(self, number, pin):
        for acc in self.accounts:
            if number == acc.number:
                if acc.pin == acc.pin:
                    return acc
                else:
                    return "BADPASSWORD"
        return "INVALID"
    def add_account(self, address, number=0, pin='', balance=0):
        for account in self.accounts:
            if account.number == number:
                account = BankAccount(address, number, pin, balance)
                return account
        acc = BankAccount(address, number if number else self.get_next_num(), pin if pin else self.gen_pin(), balance)
        self.accounts.append(acc)
        return acc
    def main(self):
        print("ERROR: Access denied.")
    def main_hacked(self):
        print("Welcome to {}.".format(self.name))
        print("For a command list, type HELP.")
        while True:
            ch = input("$")
            if ch in ["help", "?"]:
                div()
                print("help: lists commands")
                print("clear/cls: clears terminal")
                div()
                print("list: lists all accounts and their balances")
                print("passwd: display PIN's of all accounts")
                div()
                print("exit/quit: disconnects from host")
                div()
                print("NOTE: The frontend(s) are used to manage accounts, not this console.")
                div()
            elif ch == "":
                pass
            elif ch == "passwd":
                div()
                print("ACC      PIN")
                div()
                for acc in self.accounts:
                    print("{}      {}".format(acc.number, acc.pin))
                div()
            elif ch == "list":
                div()
                print("ACC\tBALANCE")
                div()
                for acc in self.accounts:
                    print("{}\t{:,}".format(acc.number, acc.balance))
                div()
            elif ch in ["clear", "cls"]:
                cls()
            elif ch in ["quit", "exit"]:
                return
            else:
                print("ERROR: Invalid command.")

class BankServer(Node):
    def __init__(self, name, uid, address, backend, admin_password):
        super().__init__(name, uid, address)
        self.backend = data.getNode(backend)
        self.users = [User("admin", admin_password)]
        self.playerPlease = True
        self.main_hacked = self.main

        if not isinstance(self.backend, BankBackEnd):
            raise Exception("Invalid backend server")
    def new_account(self, player):
        acc = self.backend.add_account(self.address)
        cls()
        div()
        print("New Account")
        div()
        print("New account generated.")
        print("Account Number: {}".format(acc.number))
        print("PIN: {}".format(acc.pin))
        print("Balance: {:,} Cr.".format(acc.balance))
        div()
        print("Your OS has saved your details to storage.")
        print("The `account` command lists all saved accounts in all banks.")
        br()
        player.bankAccounts.append(acc)
    def transaction_history(self, acc):
        cls()
        div()
        if len(acc.transactions) == 0:
            print("No transaction history to show.")
        for transaction in acc.transactions:
            print(transaction)
        br()
    def manage_account(self, acc):
        running = True
        while running:
            try:
                cls()
                div()
                print("Manage Account")
                print("AccNo: {}".format(acc.number))
                print("PIN: [HIDDEN]")
                print("Bank IP: {}".format(self.address))
                print("Balance: {:,} Cr.".format(acc.balance))
                div()
                print("[1] Transaction History")
                print("[ ] Make Transaction")
                print("[3] Disconnect")
                div()
                ch = int(input("$"))
                if ch == 1:
                    self.transaction_history(acc)
                elif ch == 3:
                    running = False
            except:
                pass

    def existing_account(self):
        cls()
        try:
            number = int(input("ENTER YOUR ACCOUNT NUMBER: "))
            pin = int(getpass.getpass("ENTER YOUR PIN: "))
            acc = self.backend.get_account(number, pin)
            if acc == "INVALID":
                print("ERROR: Invalid account number.")
                br()
            elif acc == "BADPASSWORD":
                print("ERROR: The PIN you entered is incorrect.")
                br()
            else:
                self.manage_account(acc)
        except:
            pass
    def main(self, player):
        running = True
        while running:
            cls()
            div()
            print(self.name)
            div()
            print("[1] New Account")
            print("[2] Existing Account")
            print("[3] Administration")
            print("[4] Disconnect")
            div()
            try:
                ch = int(input("$"))
            except:
                ch = 0
            if ch == 1:
                self.new_account(player)
            elif ch == 2:
                self.existing_account()
            elif ch == 3:
                cls()
                div()
                print("ERROR")
                div()
                print("Administration is accessible through the backend server: {}".format(self.backend.address if self.hacked else "[REDACTED]"))
                br()
            elif ch == 4:
                running = False


def accountList(args, player):
    for acc in player.bankAccounts:
        print(acc)


def bankhack(args, player):
    if len(args) == 2:
        try:
            accno = int(args[1])
        except:
            print("ERROR: Bank account must be a number.")
            return
        bank = data.getNode(args[0])
        if isinstance(bank, BankServer):
            print("Connected to backend.")
            print("Searching for account...")
            account = None
            for acc in bank.backend.accounts:
                if acc.number == accno:
                    account = acc
            if not account:
                print("ERROR: Invalid account number.")
                return
            print("Begin brute-force...")
            print("Generating PINs...")
            pinList = [str(x) for x in range(0, 1000000)]
            pins = []
            print("Converting PINs...")
            for p in pinList:
                while len(p) < 6:
                    p = "0" + p
                pins.append(p)
            for pin in pins:
                if account.pin == pin:
                    print("Found PIN: {}".format(pin))
                    break
        elif isinstance(bank, BankBackEnd):
            print("ERROR: Provided a backend server.")
            print("Bank backends have low security, and can easily be hacked.")
            print("From there, the `list` command can get the PIN of any user.")
        else:
            print("ERROR: Invalid bank server.")
    else:
        div()
        print("bankhack <ip address> <accno>")
        div()
        print("Brute-forces the PIN of a bank account.")
        print("NOTE: The IP address must be the bank FRONTEND server, not the backend.")
        div()

def tormail_base(args, player):
    if len(args) == 2:
        email = args[0]
        if not "@" in email:
            print("ERROR: Invalid email address.")
            return

        parts = email.split("@")
        if len(parts) != 2:
            print("ERROR: Invalid email address.")
            return

        node = data.getTorNode(parts[1])

        if not isinstance(node, MailServer):
            print("ERROR: Invalid mail server.")
            return
    elif len(args) == 1:
        eml = args[0]
        if eml in player.saved_accounts.keys():
            tormail_base([eml, player.saved_accounts[eml]])
        else:
            print("ERROR: Email account is not saved.")
    else:
        div()
        print("tormail <email address> [password]")
        div()
        print("Email client for Tor email addresses.")
        div()

class TorMailServer(MailServer):
    pass

class TorSignupService(SignupService):
    def send_mail(self, username):
        address = data.getTorNode(self.agent_id).address
        emails = [copy.deepcopy(x) for x in self.junkMail]
        for email in emails:
            email.receiver = "{}@{}".format(username, address)
            sendTorEmail(email)


class Reply(Base):
    def __init__(self, username, text):
        self.username = username
        self.text = text

class Topic(Base):
    def __init__(self, username, title, text):
        self.username = username
        self.title = title
        self.text = text
        self.replies = []
    def reply(self, username, text):
        reply = Reply(username, text)
        self.replies.append(reply)
    def view(self):
        cls()
        div()
        print(self.title)
        print("Author: {}".format(self.username))
        div()
        print(self.text)
        if self.replies:
            div()
        for reply in self.replies:
            print("{}: {}".format(reply.username, reply.text))
        br()

class Board(Base):
    def __init__(self, name, private=False, boardPassword="password"):
        self.name = name
        self.private = private
        self.boardPassword = boardPassword
        self.topics = []
    def add_topic(self, username, title, text, sticky=False):
        topic = Topic(username, title, text)
        if sticky:
            self.topics.insert(0, topic)
        else:
            self.topics.append(topic)
        return topic
    def add_board(self, name):
        board = Board(name)
        self.topics.append(board)
        return board


class Forum(Node):
    def __init__(self, name, uid, address, webmaster="null", admin_password=None, private=False, **kwargs):
        super().__init__(name, uid, address, minPorts=3, ports=[data.getPort(21), data.getPort(22), data.getPort(25), data.getPort(24525)], **kwargs)
        self.playerPlease = True
        self.webmaster = webmaster ## Email address of webmaster
        self.boards = [Board("General Discussion")]
        self.private = private
    def login(self, player):
        while True:
            cls()
            div()
            print(self.name)
            div()
            print("[1] Login")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "1":
                username, passwd = input("Username: "), getpass.getpass("Password: ")
                for user in self.users:
                    if user.name == username and user.password == passwd:
                        return True
                div()
                print("ERROR: Invalid credentials.")
                br()
                return False
            elif ch == "0":
                return False
    def main(self, player):
        if self.private:
            if not self.login(player):
                return
        while True:
            cls()
            div()
            print(self.name)
            if self.hacked:
                print("Webmaster: {}".format(self.webmaster))
            div()
            i = 1
            for board in self.boards:
                print("[{}] {} ({} topics)".format(i, board.name, len(board.topics)))
                i += 1
            print("[0] Exit")
            div()
            try:
                ch = int(input(">"))
            except ValueError:
                return
            try:
                if ch == 0:
                    return
                self.board_view(self.boards[ch - 1], player)
            except IndexError:
                pass
    def mission_view(self, board, mission, player):
        while True:
            cls()
            div()
            print("Name: {}".format(mission.name))
            print("Reward: {}".format(mission.reward))
            div()
            print("[1] Accept")
            print("[0] Cancel")
            div()
            ch = input(">")
            if ch == "1":
                if player.currentMission:
                    cls()
                    div()
                    print("Current mission canceled.")
                    print("You can find it here: rejects.rehack.org")
                    br()
                    data.getNode("rejected").missions.append(player.currentMission)
                player.currentMission = mission
                board.topics.remove(mission)
                return
    def get_board(self, title):
        for board in self.boards:
            if board.name == title:
                return board
    def board_view(self, board, player):
        if board.private:
            cls()
            div()
            passwd = input("Enter Board Password $")
            if passwd != boar.boardPassword:
                print("ERROR: Invalid password.")
                br()
                return
        while True:
            cls()
            div()
            print(board.name)
            div()
            i = 1
            for topic in board.topics:
                if isinstance(topic, Topic):
                    print("[{}] {} ({}; {} replies)".format(i, topic.title, topic.username, len(topic.replies)))
                elif isinstance(topic, Mission):
                    print("[{}] {} ({} Cr.)".format(i, topic.name, topic.reward))
                elif isinstance(topic, Program):
                    if not topic.unlocked:
                        print("[{}] {} ({} Cr.)".format(i, topic.name, topic.price))
                elif isinstance(topic, Board):
                    print("[{}] {} ({} Topics)".format(i, topic.name, len(topic.topics)))
                i += 1
            print("[0] Return")
            div()
            try:
                ch = int(input(">"))
            except ValueError:
                return
            if ch == 0:
                return
            else:
                try:
                    topic = board.topics[ch - 1]
                    if isinstance(topic, Topic):
                        topic.view()
                    elif isinstance(topic, Mission):
                        self.mission_view(board, topic, player)
                    elif isinstance(topic, Board):
                        self.board_view(topic, player)
                    else:
                        print("ERROR: Invalid topic.")
                        br()
                except IndexError:
                    pass
    def add_board(self, title):
        board = Board(title)
        self.boards.append(board)
        return board
    def create_user(self, username, password):
        user = User(username, password)
        self.users.append(user)


class Comment(Base):
    def __init__(self, author, text):
        self.author = author
        self.text = text
class NewsStory(Base):
    def __init__(self, title, author, date, text):
        self.title = title
        self.author = author
        self.date = date
        self.text = text
        self.comments = []
    def read(self):
        cls()
        div()
        print(self.title)
        print("Date: {}".format(self.date))
        print("Author: {}".format(self.author))
        div()
        print(self.text.rstrip("\n"))
        if self.comments:
            div()
            print("Comments")
            div()
            for comment in self.comments:
                print("{}: {}".format(comment.author, comment.text))
        br()
    def reply(self, author, text):
        self.comments.append(Comment(author, text))

class NewsServer(Node):
    def __init__(self, name, uid, address, webmaster="null"):
        super().__init__(name, uid, address, ports=[data.getPort(21), data.getPort(22), data.getPort(25), data.getPort(80)], minPorts=4)
        self.webmaster = webmaster
        self.stories = []
    def add_story(self, title, author, date, text):
        story = NewsStory(title, author, date, text)
        self.stories.append(story)
        return story
    def main(self):
        while True:
            cls()
            div()
            print(self.name)
            div()
            i = 0
            for story in self.stories:
                print("[{}] {} ({} by {})".format(i, story.title, story.date, story.author))
                i += 1
            div()
            try:
                ch = int(input("$"))
                story = self.stories[ch]
                story.read()
            except:
                return

class Shodan(Node):
    def __init__(self):
        super().__init__("SHODAN", "shodan", data.generateIP(), minPorts = 65536)
    def main(self):
        print("SHODAN breaks the fourth wall.")
    def check_logs(self, node):
        player = data.getNode("localhost")
        for log in node.logs:
            if log.address == player.address:
                return True
    def autocrat(self):
        ## This function is called at the end of the Project Autocrat mission.
        player = data.getNode("localhost")
        email = Email(
            "admin@mht.mail.com",
            "{}@jmail.com".format(player.name),
            "Important!",
            """Hello.
An anonymous tip has told me that YOU recently hacked into the CIA
and are the perpetrator of the Project Autocrat leak. Let's just say 
that the CIA will NOT be happy. Lucky for you, I'm a journalist.
I run MHT, a popular news website that reports on this kinda stuff.
I'm also anonymous, just like you are, so it'd be really shitty 
of me to reveal who you are. I've just let you know that there
will be a MASSIVE media storm over the next 3 months. I've been
in the game long enough to know what these people are like, constantly
fishing for new stories, and recycling when they can't catch any.

Anyway, I wish you luck, and I an very happy to take the attention
away from you. You can live in peace without being stormed by idiots
wanting to know more. 

The Project Autocrat leaks are insane, though. A ten-year conspiracy 
that basically predicted the modern ad-driven surveillance business 
model before it happened? A lot of people have a lot to answer for,
that's for sure. 

Have a lovely day, and check out my story on mht.com for the full story.""")
        sendEmail(email)
        mht = data.getNode("mht")
        mhtftp = data.getNode("mhtftp")
        with open("msgboard/mht.com/autocrat") as f:
            story = mht.add_story("Project Autocrat: A 10-Year Conspiracy To Spy On The American Population", "Admin",  player.date.clone(), f.read())
            story.reply("rehack", "First to report on an important issue, as always!")
            story.reply("bit", "I'm buying BTC while it's still cheap")
            story.reply("e.snowden", "bad day at the office indeed (fyi im an nsa agent)")
            story.reply("5chan", "My forum boutta get DOSed from the amount of discussion about this")
            story.reply("5chan", "It's been 3 minutes and 5chan is down already, wtf")
            mhtftp.create_file("autocrat.docx", data.AUTOCRAT, "pub")

        irc = data.getNode("rhirc")
        irc_general = irc.get_channel("#general")
        irc_news = irc.get_channel("#news")

        irc_news.add_message("admin", "Project Autocrat has leaked! See it on mht.com and download autocrat.docx BEFORE it gets taken down!")
        irc_news.add_message("admin", "That being said, it is on our drop server for all to grab, in /incoming, courtesy of {}".format(player.name))
        irc_general.add_message("datastream", "So it was {} who did it?".format(player.name))
        irc_general.add_message("insolvent", "this agent is brand-new, yet they did what no-one could")
        irc_general.add_message("datastream", "they got away for now")
        irc_general.add_message("datastream", "there'lll be CIA agents in this channel taking notes")
        irc_general.add_message("admin", "hey {}, don't worry, reHack doesn't have any of your personal info, not even a name".format(player.name))
        irc_general.add_message("bit", "there's a media storm a-brewin', i can feel it")
        irc_general.add_message("admin", "we all can")
        irc_general.add_message("datastream", "admin, are you the owner of reHack or just a maintainer of the irc?")
        irc_general.add_message("admin", "just an admin, not the owner")
        irc_general.add_message("data_expunged", "that would be me :)")
        irc_general.add_message("bit", "the man the myth the legend, [DATA EXPUNGED]")
        irc_general.add_message("data_expunged", "just a bit of advice for you bit, try to stay anonymous ok?")
        irc_general.add_message("data_expunged", "the amount of scary emails I get from the NSA is scary")
        irc_general.add_message("admin", "scary email is scary")
        irc_general.add_message("data_expunged", "as a reminder to ALL agents, if the CIA offer you work, DECLINE IMMEDIATELY")
        irc_general.add_message("data_expunged", "If they offer money, STILL DECLINE, we are ALTRUISTS not hackers for hire")
        irc_general.add_message("admin", "what about the credits thing?")
        irc_general.add_message("data_expunged", "what I mean to say is that we have morals, unlike the CIA/FBI/NSA/MI6/etc.")
        irc_general.add_message("bit", "today's leaks show that haha")
        irc_general.add_message("data_expunged", "y'all should get back to work")
        irc_general.add_message("admin", "aye aye captain")
        irc_general.add_message("data_expunged", "you say that again and you get canned")
        irc_general.add_message("admin", "aye aye captain")
        irc_general.add_message("server", "removed admin rights from admin for 1d")
        irc_general.add_message("server", "gave admin rights to data_expunged for 1d")
        irc_news.allow("data_expunged")
        irc_news.add_message("data_expunged", "strike 1/3 for admin")
        irc_general.add_message("newsbot", "new #news item: 'strike 1/3 for admin'")
        irc_general.add_message("server", "admin is now known as aye_aye_captain")
        irc_general.add_message("data_expunged", "I give up. Change it back and I revert my changes")
        irc_general.add_message("server", "bit is now known as admin")
        irc_general.add_message("server", "data_expunged renamed admin to bit")
        irc_general.add_message("server", "data_expunged renamed aye_aye_captain to admin")
        irc_general.add_message("server", "data_expunged removed admin ban from admin")
        irc_general.add_message("data_expunged", "now get back to work, y'all have drained my patience")

        dm = irc.add_direct_message(["insolvent", player.name])
        dm.add_message("insolvent", "Hello, we have noticed your talent, and would like to invite you to SCSI group")
        dm.add_message("insolvent", "We've already added your username and password to SCSI-net, our LAN that you can connect to from anywhere.")
        dm.add_message("insolvent", "If you're unfamiliar with LAN's, the router is located at 192.168.0.0, and you can connect to our various services from it.")
        dm.add_message("insolvent", "In order to hide our true location on the Internet, we require you to connect through a client instead of connecting to an address.")
        dm.add_message("insolvent", "Download SCSI-NET client: {}".format(data.getTorNode("scsiclient").address))

        scsi = data.getTorNode("scsi")
        scsi.create_user(player.name, player.password)


    def tick(self):
        player = data.getNode("localhost")
        mht = data.getNode("mht")
        if player.trace:
            print("({}) Active trace for {}".format(int(player.trace.endTime - time.time() + 1), data.getAnyNode(player.trace.node).address))
            if time.time() > player.trace.endTime:
                player.catchTrace()
        if time.time() - player.timeSinceNextDay > 600:
            player.timeSinceNextDay = time.time()
            player.date.next_day()

        for action in player.actions:
            action.run(player.date)
            player.actions = [x for x in player.actions if x.time != player.date]

        # if player.date == GameDate(2010, 7, 11) and not self.enwiredEvent:
        #     self.enwiredEvent = True
        #     jmail = data.getNode("jmail")
        #     jmail.create_user("renwired", "renderware")
        #     renwired = NewsServer("RenWired: Re-EnWired", "renwired", "re.enwired.com", "jacon@enwired.mail")
        #     with open("msgboard/xdg.net/return") as f:
        #         returnStory = renwired.add_story("EnWired Is Back: RenWired", "Jacob Marksman", player.date.clone(), f.read())
        #     returnStory.reply("cop-out", "You're a terrible writer")
        #     data.NODES.append(renwired)
        #     with open("msgboard/mht.com/renwired") as f:
        #         renwired_story = mht.add_story("Is EnWired back, or is it a ruse?", "Admin", player.date.clone(), f.read())
        #         renwired_story.reply("replit", "I think I believe Jacob; he seems like a nice guy and he shares the passion his father possesses")
        #         renwired_story.reply("code", "Nonesense; this is 100% a cop-out")
        #         renwired_story.reply("sizzle", "'he seems like a nice guy' = red flag")
        #         renwired_story.reply("replit", "let's not start a flame war")
        #
        # if player.date == GameDate(2010, 7, 12) and not self.xdgNet:
        #     self.xdgNet = True
        #     renwired = data.getNode("renwired")
        #     renwired.name = "XDG.Net: A better kind of news"
        #     renwired.address = "xdg.net"
        #     with open("msgboard/mht.com/xdgn") as f:
        #         xdgn = mht.add_story("RenWired Has Become xdg.net", "Admin", player.date.clone(), f.read())
        #         xdgn.reply("code", "that was fast")
        #         xdgn.reply("admin", "code: my thoughts exactly")
        #         xdgn.reply("sizzle", "mht is such a shill, 2/3 of the article is about the previous one!")
        #         xdgn.reply("replit", "sizzle: +1")
        #         xdgn.reply("bit", "sizzle: +1")
        #         xdgn.reply("rehack", "sizzle: that's ridiculous, your claim is baseless")
        #         xdgn.reply("admin", "rehack, sizzle: what makes you think I am/am not a shill?")
        #         xdgn.reply("sizzle", "admin: 100% you got financial compensation for being on Fox News")
        #         xdgn.reply("rehack", "sizzle: fox easily could have aired their story and claimed they made the discovery")
        #         xdgn.reply("admin", "rehack: thanks for the clarification; im going through some stuff rn so the money was well-appreciated")
        #         xdgn.reply("admin", "besides, making the Murdochs slightly less rich is always a good thing")
        #         xdgn.reply("sizzle", "admin: what stuff? i feel bad now")
        #         xdgn.reply("admin", "don't worry, it's nothing too serious, just some run-of-the-mill hardships")
        #         xdgn.reply("bit", "is there anything we can do to help?")
        #         xdgn.reply("admin", "I make my money through licensing MHT articles, so not really")
        #         xdgn.reply("admin", "you can check out my forum though: forum.mht.com")
        #
        #     with open("msgboard/xdg.net/workspaces07") as f:
        #         story = renwired.add_stock("NanoSoft Workspaces 2007: First Impressions", "Michael Olufsen", player.date.clone(), f.read())


def ssh(args):
    if len(args) == 1:
        node = data.getAnyNode(args[0], True) if isTorAddon() else data.getNode(args[0], True)
        if node:
            if node.hacked and data.checkPort(node, 22):
                connect.connect(node)
            else:
                print("ERROR: Access denied.")
        else:
            print("ERROR: Invalid hostname.")
    else:
        div()
        print("ssh <address>")
        div()
        print("Connect to a remote host over SSH.")
        div()

def ftp(args):
    if len(args) == 1:
        node = data.getAnyNode(args[0], True) if isTorAddon() else data.getNode(args[0], True)
        if node:
            if node.hacked and data.checkPort(node, 21):
                folderView(data.createFolder(node), True)
            elif data.checkPort(node, 21) and node.readAccess:
                folderView(data.createFolder(node), node.hacked)
            else:
                print("ERROR: Access denied.")
        else:
            print("ERROR: Invalid hostname.")
    else:
        div()
        print("ftp <address>")
        div()
        print("Browses files on a remote host over FTP.")
        div()

class Forwarder(Node):
    name = "Apache Forwarder v1.0"
    def __init__(self,  uid, address, forwarding_url, show_origin=True):
        super().__init__(self.name, uid, address, minPorts=1, ports=[data.getPort(80)])
        self.forwarding_url = forwarding_url
        self.playerPlease = True
        self.show_origin = show_origin
        self.users = [User("admin")]

    def get_node(self, address):
        return data.getNode(self.forwarding_url)
    def connect(self, node, player):
        if node.hacked and node.playerPlease:
            node.main_hacked(player)
        elif node.hacked:
            node.main_hacked()
        elif node.playerPlease:
            node.main(player)
        else:
            node.main()
    def main(self, player):
        self.connect(self.get_node(self.forwarding_url), player)
    def main_hacked(self, player):
        print("\n".join([
            "$ Apache Forwarder v1.0",
            "$ Apache Forwarder is an open-source forwarding server that forwards all traffic to another location.",
            "$ It supports Tor as well as the clearnet, allowing for:",
            "$ - Tor --> Tor",
            "$ - Tor --> Clearnet*",
            "$ - Clearnet --> Tor*",
            "$ - Clearnet --> Clearnet",
            "$ * Using this option de-anonymises users of the proxy. Users connecting over Tor proper are fine.",
            "$ This node points to: {}".format(self.get_node(self.forwarding_url).address if self.show_origin else "[DATA HIDDEN BY ADMIN]"),
        ]))

class TorForwarder(Forwarder):
    def get_node(self, address):
        return data.getTorNode(address)

class TorRelay(Node):
    def __init__(self, name, uid, address, webmaster):
        super().__init__(name, uid, address, ports[data.getTorNode(22), data.getPort(9200)], minPorts=2)
        self.webmaster = webmaster
    def main_hacked(self):
        print("Tor Relay")
        print("HTTP STATUS: 200 OK")
        print("WEBMASTER EMAIL: {}".format(self.webmaster))


class FTPServer(Node):
    def __init__(self, node, uid, address, **kwargs):
        super().__init__(node, uid, address, ports=[data.getPort(21)], **kwargs)
        self.pub = self.create_folder("pub")
        self.inc = self.create_folder("incoming", True)
        self.inc.create_file("ReadMe.txt", data.INCOMING_README)
    def main(self):
        print("ERROR: An FTP client is required to connect to this server.")
class PublicFTPServer(Node):
    def __init__(self, node, uid, address, acceptUpload=True, **kwargs):
        super().__init__(node, uid, address, ports=[data.getPort(21)], **kwargs)
        self.pub = self.create_folder("pub")
        self.inc = self.create_folder("incoming", acceptUpload)
        self.inc.create_file("ReadMe.txt", data.INCOMING_README)
        self.readAccess = True
    def main(self):
        print("ERROR: An FTP client is required to connect to this server.")

def folderView(self, writeAccess=False):
    while True:
        cls()
        div()
        print("Index of {} (Permissions: {})".format(self.name, "rw" if writeAccess else "r"))
        div()
        i = 1
        for file in self.files:
            if isinstance(file, Folder):
                typ = "Folder"
            elif isinstance(file, File):
                typ = "File"
            elif isinstance(file, EncryptedFile):
                typ = "Encrypted File"
            elif isinstance(file, ZippedFolder):
                typ = "Compressed Folder"
            else:
                typ = "Corrupt"
            print("[{}] {} ({})".format(i, file.name, "Folder: {} files".format(len(file.files)) if isinstance(file, Folder) else typ))
            i += 1
        div()
        try:
            ch = int(input("$"))
            if ch == 0:
                return
            file = self.files[ch-1]
            if isinstance(file, Folder):
                if writeAccess:
                    folderView(file, True)
                else:
                    folderView(file, file.writeAccess)
            elif type(file) in [File, EncryptedFile, ZippedFolder]:
                fileView(file, self, True if writeAccess else self.writeAccess)
        except:
            # print(traceback.format_exc())
            # br()
            return

def get_origin(origin):
    # return origin
    try:
        return data.getAnyNode(origin).address
    except:
        return "Unknown"

def fileView(self, folder, writeAccess=False):
    cls()
    div()
    print("{}\nOrigin: {}".format(self.name, get_origin(self.origin)))
    div()
    print("[1] View File")
    print("[2] Upload File")
    if writeAccess and folder:
        print("[3] Delete File")
    else:
        print("[ ] Delete File")
    if isinstance(self, EncryptedFile):
        print("[4] Decrypt" if self.password else "[4] Extract")
        print("[5] View Header")
    if isinstance(self, ZippedFolder):
        print("[4] Extract Contents")
        print("[5] Browse Folder")
    div()
    ch = input("$")
    if ch == "1":
        cls()
        div()
        print(self.data)
        br()
    elif ch == "2":
        target = input("Target IP $")
        cls()
        div()
        node = data.getNode(target, True)
        if node and data.checkPort(node, 21):
            inc = data.getFile(node, "incoming", "Folder")
            if inc and inc.writeAccess:
                inc.files.append(self.clone())
                print("Successfully uploaded file.")
            else:
                print("ERROR: Cannot upload to server")
        else:
            print("ERROR: Invalid FTP server")
        br()            
    elif ch == "3" and writeAccess:
        folder.files = [x for x in folder.files if x.name != self.name]
    elif ch == "4" and isinstance(self, EncryptedFile):
        if self.password:
            passwd = getpass.getpass("Password $")
        else:
            passwd = None
        if self.check(passwd):
            if folder.writeAccess:
                folder.files.append(self.file)
                cls()
                div()
                print("Successfully decrypted file.")
                br()
            else:
                cls()
                div()
                print("ERROR: No write access.")
                br()
        else:
            cls()
            div()
            print("ERROR: Invalid password.")
            br()
    elif ch == "4" and isinstance(self, ZippedFolder):
        if writeAccess:
            folder.add_file(self.folder)
            cls()
            div()
            print("Successfully extracted folder.")
            br()
    elif ch == "5" and isinstance(self, EncryptedFile):
        node = data.getNode(self.header["origin"])
        origin = node.address if node else "Unknown"
        cls()
        div()
        print("File name: {}".format(self.header["name"]))
        print("Origin: {}".format(origin))
        print("Software: {}".format(self.header["software"]))
        br()
    elif ch == "5" and isinstance(self, ZippedFolder):
        folderView(self.folder)

def history(args, player):
    div()
    print("Internet History")
    div()
    connect.main(["history"], player)
    div()
    print("Tor History")
    div()
    tor(["history"], player)
    div()

def note(args, player):
    if args in [["list"], ["ls"]]:
        i = 0
        for note in player.notes:
            print("{}. {}".format(i, note.text))
            i += 1
    elif args == ["del"]:
        div()
        print("note del <id>")
        div()
        print("Deletes a note.")
        div()
    elif "del" in args and len(args) == 2:
        try:
            player.notes.pop(int(args[1]))
        except IndexError:
            print("ERROR: Invalid note.")
    elif args == ["add"]:
        div()
        print("note add <text>")
        div()
        print("Adds a note.")
        div()
    elif "add" in args:
        note = " ".join(args[1:])
        player.notes.append(Note(note))
        print("Added note (ID: {}).".format(len(player.notes) - 1))
    elif args == ["share"]:
        div()
        print("note share <id> <address")
        div()
        print("Share a note over FTP.")
        div()
    elif "share" in args and len(args) == 3:
        try:
            note = int(args[1])
            node = data.getNode(args[2], strict=True)
            if not data.checkPort(node, 21):
                print("400: Connection refused")
                return
            inc = data.getFile(node, "incoming", "Folder")
            if not inc or not inc.writeAccess:
                print("ERROR: FTP server does not permit uploading.")
                return
            inc.add_file(File(player.notes[note].text, player.notes[note].text))
        except:
            print(traceback.format_exc())
    else:
        div()
        print("note [args]")
        div()
        print("Manage notes.")
        div()
        print("note ls: list all notes")
        print("note add <text>: add a note")
        print("note del <id>: delete a note")
        print("note share <id> <address>: Share a note to an FTP server")
        div()

class IRCMessage(Base):
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text
    def __str__(self):
        return "{}: {}".format(self.sender, self.text)

class IRChannel(Base):
    def __init__(self, name, description, private=False, readOnly=False):
        self.name = name
        self.description = description
        self.messages = []
        self.private = private
        self.allowlist = ["server"]
        self.readOnly = readOnly
    def allow(self, user):
        self.allowlist.append(user)
        self.add_message("server", "Gave voice to {}".format(user))
    def add_message(self, sender, text):
        if not self.readOnly or sender in self.allowlist:
            self.messages.append(IRCMessage(sender, text))


class IRCServer(Node):
    def __init__(self, name, uid, address, private=False, *args, **kwargs):
        super().__init__(name, uid, address, ports=[data.getPort(6667), data.getPort(22), data.getPort(80), data.getPort(21)], minPorts=4, *args, **kwargs)
        self.channels = []
        self.private = private
    def add_channel(self, *args, **kwargs):
        channel = IRChannel(*args, **kwargs)
        self.channels.append(channel)
        return channel
    def add_direct_message(self, senders, channel_name=None):
        channel = IRChannel(channel_name if channel_name else "@{}".format(senders[0]), "Direct Message", True)
        channel.allowlist = senders
        self.channels.append(channel)
        return channel
    def get_channel(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
    def main(self):
        print("ERROR: An IRC client is needed to access this server.")

class MailDotComTracker(NodeTracker):
    def __init__(self):
        super().__init__("Mail.Com Instance Tracker", "maildotcomtracker", "tracker.mail.com")
    def tick(self):
        self.nodes = []
        for node in [x for x in data.NODES if isinstance(x, MailDotCom)]:
            self.add_node(node.uid)


class FileDeletedCheck(Base):
    def __init__(self, filename, folder="/"):
        super().__init__()
        self.filename = filename
        self.folder = folder
    def check(self, node):
        node = data.getAnyNode(node)
        if self.folder == "/":
            files = data.createFolder(node)
        else:
            files = data.getFile(node, node.folder, "Folder")
        for file in node.files:
            if file.name == self.filename:
                return False
        return True

class FileCopiedCheck(Base):
    def __init__(self, filename, text=None, origin=None, folder="/"):
        self.filename = filename
        self.text = text
        self.origin = origin
        self.folder = folder
    def check(self, node):
        node = data.getAnyNode(node)
        if self.folder == "/":
            folder = data.createFolder(node)
        else:
            folder = data.getFile(node, self.folder, "Folder")

        for file in folder.flatten():
            if file.name == self.filename and (not self.origin or file.origin == self.origin) and (not self.text or file.data == self.text):
                return True

class ZippedFileCopiedCheck(Base):
    def __init__(self, filename, origin=None, folder="/"):
        self.filename = filename
        self.origin = origin
        self.folder = folder

    def check(self, node):
        node = data.getAnyNode(node)
        if self.folder == "/":
            folder = data.createFolder(node)
        else:
            folder = data.getFile(node, self.folder, "Folder")

        for file in folder.flatten():
            if file.name == self.filename and (not self.origin or file.origin == self.origin):
                return True

class FileCheck(Base):
    def __init__(self, node: str):
        super().__init__()
        self.node = node
        self.checks = []
    def add(self, check):
        self.checks.append(check)

class FileCheckMission(Mission):
    def check_end(self):
        if not isinstance(self.target, FileCheck):
            raise TypeError("Target must be an instance of FileCheck")
        node = data.getAnyNode(self.target.node)
        if not node:
            return False
        for check in self.target.checks:
            if not check.check(self.target.node):
                return False
        return True

def date(args, player):
    print("{} {}".format(player.date, data.extrapolateTime(time.time() - player.timeSinceNextDay)))

class HostKillMission(Mission):
    def check_end(self):
        node = data.getAnyNode(self.target, True)
        return not node

def openftp(args):
    if len(args) == 1:
        node = data.getNode(args[0], True)
        if not node:
            print("ERROR: Node not found (404)")
            return
        if not node.hacked:
            print("ERROR: Access denied (403)")
            return
        if data.checkPort(node, 21):
            print("ERROR: FTP server already exists (500)")
            return
        node.ports.append(data.getPort(21))
        print("Successfully opened FTP server.")
    else:
        div()
        print("openftp <address>")
        div()
        print("Starts an FTP server in a node that doesn't have one, allowing you to wreak true havoc.")
        div()
def chmod(args):
    player = data.getNode("localhost")
    if len(args) == 3:
        node = data.getNode(args[0], True)
        if not node:
            print("ERROR: Invalid address")
            return
        if not node.hacked:
            print("ERROR: Access denied")
            return
        mode = args[1]
        if mode not in ["r", "rw"]:
            print("ERROR: Mode must be either `r` or `rw`")
            return

        if args[2] == "/":
            folder = data.createFolder(node)
        else:
            folder = data.getFile(node, args[2], "Folder")

        if not folder:
            print("ERROR: Folder does not exist.")
            return

        folder.setWriteAccess(True if mode == "rw" else False)

    else:
        div()
        print("chmod <address> <r|rw> <folder>")
        div()
        print("Set the permissions for a folder and its contents on a remote node.")
        div()
        print("Examples:")
        print("- chmod example.com rw /")
        print("    - Sets read/write permissions for all files inside of /")
        print("- chmod example.com r /")
        print("    - Makes every file in the node read-only")
        div()

class FunctionMission(Mission):
    def check_end(self):
        if callable(self.target):
            return self.target()

class SearchEngine(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searchArea = []
    def add(self, node):
        self.searchArea.append(node)
    def test(self):
        for node in self.searchArea:
            if not data.getAnyNode(node):
                print("FAIL: {}".format(node))
    def get_nodes(self):
        nodes = [data.getAnyNode(x) for x in self.searchArea if x is not None]
        return nodes
    def main(self):
        self.test()
        while True:
            ch = input("Type search term or 'exit' >").lower()
            if ch in ["quit", "exit"]:
                return
            elif ch == "":
                print("ERROR: Must enter a search query.")
            else:
                div()
                print("Search results for '{}':".format(ch))
                div()
                self.search(ch)
                div()
    def search(self, ch):
        for node in self.get_nodes():
            if ch in node.name.lower() or ch in node.address.lower():
                print("{}: {}".format(node.name, node.address))


class LinkTree(Node):
    def __init__(self, *args, motd="This is a default MOTD.", **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = [data.getPort(21), data.getPort(22), data.getPort(80)]
        self.minPorts = 3
        self.motd = motd
        self.linked = []
    def add_link(self, uid):
        self.linked.append(uid)
    def main(self):
        div()
        print(self.motd)
        div()
        for link in self.linked:
            node = data.getAnyNode(link)
            if node:
                print("* {}: {}".format(node.name, node.address))
        div()

class Patient(Base):
    def __init__(self, forename, surname, age=None, address=None, conditions=None):
        self.forename = forename
        self.surname = surname
        self.age = age if age else random.randint(18, 65)
        self.address = address
        self.conditions = conditions if conditions else []
        self.emails = []

class MedicalDatabase(Node):
    def __init__(self, **kwargs):
        super().__init__("United States Federal Medical Database", "meddb", "db.medic.gov", **kwargs)
        self.people = []
        self.emails = []
        self.trace = Trace(self.uid, "Government", 35)

    def main(self):
        username, password = input("Username $"), getpass.getpass("Password $")
        for user in self.users:
            if username == user.name and password == user.password:
                self.main_hacked()
                return
        print("ERROR: Incorrect credentials. Please try again.")
    def main_hacked(self):
        while True:
            cls()
            div()
            print(self.name)
            div()
            print("[1] New Patient")
            print("[2] Manage Patient")
            print("[3] Delete Patient")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "1":
                self.new_patient()
            elif ch == "2":
                self.manage_patient()
            elif ch == "3":
                self.delete_patient()
            elif ch == "0":
                return

    def choose_patient(self):
        while True:
            cls()
            div()
            i = 1
            for person in self.people:
                print("[{}] {}, {} ({} Y.O)".format(i, person.surname, person.forename, person.age))
                i += 1
            div()
            try:
                ch = int(input("$"))
                if ch == 0:
                    return
            except:
                return
            return self.people[ch-1]
    def new_patient(self):
        cls()
        forename, surname = input("Forename $"), input("Surname $")
        if not forename or not surname:
            print("ERROR: Some data was incomplete.")
            br()
            self.new_patient()
        try:
            age = int(input("Age $"))
        except:
            print("ERROR: Age formatted incorrectly.")
            self.new_patient()
        address = input("Address (Optional) $")

        patient = Patient(forename, surname, age, address if address else None)

        self.people.append(patient)

        print("Successfully added new record.")
        br()

    def confirm(self, message="Confirm Action"):
        cls()
        div()
        print(message)
        div()
        print("[1] Yes")
        print("[0] No")
        div()
        ch = input("$")
        return ch == "1"

    def message(self, message):
        cls()
        div()
        print(message)
        br()
    def delete_patient(self):
        patient = self.choose_patient()
        if patient:
            if self.confirm("Confirm deletion of {}, {}".format(patient.surname, patient.forename)):
                self.people.remove(patient)
                self.message("Successfully deleted patient.")
            else:
                self.message("Action canceled.")

    def manage(self, patient):
        while True:
            cls()
            div()
            print("Name: {}, {}".format(patient.surname, patient.forename))
            print("Age: {}".format(patient.age))
            print("Address: {}".format(patient.address))
            print("Condition(s): {}".format("; ".join(patient.conditions) if patient.conditions else "None"))
            div()
            print("[1] Add Condition")
            print("[ ] Remove Condition")
            print("[3] Share Records (Email)")
            if self.hacked and patient.emails:
                print("[4] View Logged Email Addresses")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "1":
                cls()
                condition = input("Enter Condition Name $")
                if condition:
                    patient.conditions.append(condition)
                    self.message("Action completed.")
                else:
                    self.message("Action canceled.")
            elif ch == "2":
                self.message("This feature has been disabled by the admin for the following reason: Maintenance")
            elif ch == "3":
                email = input("Email Address $")
                if data.checkEmailAddress(email):
                    eml = Email("records-daemon@db.medic.gov", email, "Medical Records For {}, {}".format(patient.surname, patient.forename), """Name: {}, {}\nAge: {}\nAddress: {}\nConditions: {}""".format(patient.surname, patient.forename, patient.age, patient.address, "; ".join(patient.conditions) if patient.conditions else "None"))
                    sendEmail(eml)
                    self.emails.append(email)
                    self.message("Email Sent!\nNOTE: The email address in question has been logged for security purposes and cannot be removed.")
                else:
                    self.message("ERROR: Invalid email account.")
            elif ch == "4" and self.hacked and patient.emails:
                self.message("\n".join(patient.emails))
            elif ch == "0":
                return

    def manage_patient(self):
        patient = self.choose_patient()
        if patient:
            self.manage(patient)


def ircmain(server, username):
    def view(channel, username):
        cls()
        div()
        print("{}: {}".format(channel.name, channel.description))
        div()
        for message in channel.messages:
            print("{}: {}".format(message.sender, message.text))
        msg = input("{} > ".format(username))
        if msg in ["/quit", "/exit"]:
            return
        else:
            if msg:
                channel.add_message(username, msg)
            view(channel, username)
    channels = [x for x in server.channels if not x.private or username in x.allowlist]
    while True:
        cls()
        div()
        print(server.name)
        div()
        i = 1
        for channel in channels:
            print("[{}] {}: {}".format(i, channel.name, channel.description))
            i += 1
        # print("[0] Exit")
        div()
        try:
            ch = int(input("$"))
        except:
            return
        if 0 < ch <= len(channels):
            view(channels[ch-1], username)

def irclogin(node):
    loginUser = None
    if node.private and not node.hacked:
        cls()
        div()
        print("Sign Into {}".format(node.name))
        div()
        username, password = input("Username $"), getpass.getpass("Password $")
        for user in node.users:
            if user.name == username and user.password == password:
                loginUser = user
        if not loginUser:
            print("ERROR: Invalid credentials.")
            return
    if loginUser:
        ircmain(node, loginUser.name)
    else:
        ircmain(node, "anonymous")
def irc(args):
    if len(args) == 1:
        server = args[0]
        node = data.getNode(server, True)
        if isinstance(node, IRCServer):
            irclogin(node)
        else:
            print("ERROR: Invalid server.")


    else:
        div()
        print("irc <server address>")
        div()
        print("IRC Client.")
        div()

def logclear(args):
    player = data.getNode("localhost")
    if args:
        node = data.getNode(args[0], True)
        if not node:
            print("ERROR: Invalid address.")
            return
        if not node.hacked:
            print("ERROR: Access denied.")
            return
        for log in node.logs:
            if log.address == player.address:
                node.logs.remove(log)
    else:
        div()
        print("logclear <address>")
        div()
        print("Deletes all logs mentioning your IP address.")
        div()

def installProgram(program):
    player = data.getNode("localhost")
    program = data.getObject(data.PROGRAMS, program)
    if not program:
        return "There was a problem parsing this package."
    if program.unlocked:
        return "Program already purchased."
    if player.creditCount < program.price:
        return "Insufficient funds to purchase program."
    program.unlocked = True
    player.creditCount -= program.price
    return "Successfully installed {}".format(program.name)



class ProgramInstaller(Node):
    """
    This node allows you to install a program when you connect to it.
    """
    def __init__(self, name, uid, address, program, **kwargs):
        super().__init__(name, uid, address, **kwargs)
        self.program = program
    def main(self):
        player = data.getNode("localhost")
        program = data.getObject(data.PROGRAMS, self.program)
        if not program:
            print("There was a problem parsing this package.")
            return
        cls()
        div()
        print("Install {}?".format(program.name))
        div()
        print("Price: {} Cr.".format(program.price))
        print("Description: {}".format(program.desc))
        div()
        ch = input("[Y/n] $").lower()
        if ch == "y":
            print(installProgram(program))
def darkstore(args):
    player = data.getNode("localhost")
    programs = [x for x in data.PROGRAMS if x.name in data.DARKSTORE and not x.unlocked]
    
    if args == ["list"]:
        for program in programs:
            div()
            print("{}".format(program.name))
            print("\t{}".format(program.desc))
            print("\t{} Cr.".format(program.price))
        div()
        if not programs:
            print("The store is empty.")
            div()
    elif len(args) == 1:
        prog = args[0]
        for program in programs:
            if program.name == prog:
                print(installProgram(program))
    else:
        div()
        print("darkstore <program>")
        div()
        print("Purchase a program from DarkStore, the ONLY trustworthy Darknet software store.")
        div()
        print("darkstore list: list all available programs.")
        div()
def scsi(args):
    player = data.getNode("localhost")
    scsi = data.getTorNode("scsi")
    tor([scsi.address], player)
    scsi.address = data.generateTorURL("scsi")


def unhack(args):
    if len(args) == 1:
        node = data.getNode(args[0], True)
        if not node:
            print("ERROR: Invalid address.")
            return
        if node.hacked:
            node.hacked = False
            print("Successfully removed root access.")
        else:
            print("ERROR: Access denied.")
    else:
        div()
        print("unhack <ip address>")
        div()
        print("Removes root access (acquired from porthack/login/etc) from a node.")
        div()

def bal(args):
    player = data.getNode("localhost")
    store(["balance"], player)

def autohack(args):
    sshkill = data.getProgram("sshkill", False)
    ftpkill = data.getProgram("ftpkill", False)
    webworm = data.getProgram("webworm", False)
    if args == ["check"]:
        good = True
        if not sshkill:
            good = False
            print("ERROR: `sshkill` is not installed. Cannot open port 22.")
        if not ftpkill:
            good = False
            print("ERROR: `ftpkill` is not installed. Cannot open port 21.")
        if not webworm:
            good = False
            print("ERROR: `webworm` is not installed, cannot open port 80.")
        if good:
            print("All programs installed.")
    elif len(args) == 1:
        node = data.getNode(args[0], True)
        if node:
            ports = [x.num for x in node.ports]
            if 21 in ports and ftpkill:
                ftpkill.function([node.address])
            if 22 in ports and sshkill:
                sshkill.function([node.address])
            if 80 in ports and webworm:
                webworm.function([node.address])
            porthack([node.address])
        else:
            print("ERROR: Invalid address.")
    else:
        div()
        print("autohack <address>")
        div()
        print("Semi-automatically hacks into nodes.")
        print("Supports ports: 21, 22, 80")
        div()
        print("autohack check: check if all needed programs are installed")
        div()
        print("AD: For an autohack w/ more port options and firewall cracking: {}".format(data.getTorNode("autohack2").address))
        div()

class NodeKillCheck:
    def check(self, node):
        return not data.getAnyNode(node).check_health()

class UserNodeCheck:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
    def check(self, node):
        for user in node.users:
            if user.name == self.username and (not self.password or self.password == user.password):
                return True


class NodeCheck:
    def __init__(self, node):
        self.node = node
        self.checks = []
    def add(self, check):
        self.checks.append(check)

class NodeCheckMission(Mission):
    def check_end(self):
        if not isinstance(self.target, NodeCheck):
            raise TypeError("Mission target must be a NodeCheck")
        node = data.getAnyNode(self.target.node)
        if not node:
            return False
        for check in self.target.checks:
            if not check.check(node):
                return False
        return True


class Stock(Base):
    def __init__(self, name, symbol, price=1.0):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.prevPrice = price
    def change_price(self, percent):
        multiplier = 1 + percent / 100
        self.prevPrice = int(self.price)
        self.price *= multiplier
        self.price = int(self.price)
    def get_value(self, market, shares):
        return market.get_stock(self.symbol).price * shares

class StockMarketAccount(Base):
    def __init__(self, market, username, password, stocks={}):
        self.username = username
        self.password = password
        self.stocks = stocks
        self.market = market
    def get_value(self):
        val = 0
        for symb in self.stocks:
            val += self.market.get_stock(symb).price * self.stocks[symb]
        return val

class StockMarket(Node):
    def __init__(self, *args, adminPassword=None, minPorts=63336, **kwargs):
        super().__init__(*args, users=[User("admin", adminPassword)], ports=[data.getPort(80), data.getPort(22), data.getPort(21)], minPorts=minPorts, **kwargs)
        self.stocks = []
        self.accounts = []
        self.free_stocks = {}
        self.folder = self.create_folder("StockMarket")
        self.folder.create_file("ReadMe.txt", "For support on how to manage the Stock Market server, contact Stock Market Solutions: sms.us")
    def check_locked(self):
        return "LOCKFILE" in [x.name for x in self.folder.flatten()]
    def main(self):
        player = data.getNode("localhost")
        while True:
            cls()
            div()
            print(self.name)
            div()
            print("[1] New Account")
            print("[2] Existing Account")
            if self.hacked:
                print("[3] Admin Panel")
            div()
            try:
                ch = int(input(">"))
            except:
                return
            if ch == 1:
                self.new_account(player)
            elif ch == 2:
                self.existing_account_login(player)
            elif ch == 3 and self.hacked:
                self.admin_panel(player)
    def admin_panel(self, player):
        if self.check_locked():
            cls()
            div()
            print("ERROR: The server is down for maintenance. Check back later.")
            print("NOTE: To remove the maintenance lock, delete /StockMarket/LOCKFILE.")
            br()
            return

        while True:
            if self.check_locked():
                return
            cls()
            div()
            print("Admin Panel")
            div()
            print("[1] Shut Down Exchange")
            div()
            try:
                ch = int(input(">"))
            except:
                return
            if ch == 1:
                self.shut_down(player)
    def shut_down(self, player):
        cls()
        div()
        print("Confirm?")
        div()
        print("Are you sure you wish to shut down the exchange?")
        print("This cannot be undone through this panel and requires additional access.")
        div()
        print("[1] YES")
        print("[0] No")
        div()
        ch = input(">")
        if ch == "1":
            self.folder.create_file("LOCKFILE", "Delete this file to re-open the stock market.")
            cls()
            div()
            print("Success")
            div()
            print("New sessions will be rejected. Existing sessions will disappear shortly.")
            print("To start up again, delete the LOCKFILE from the /StockMarket directory. You can use an FTP server.")
            br()
            return
    def get_stock(self, symbol):
        for stock in self.stocks:
            if stock.symbol == symbol:
                return stock
    def new_account(self, player):
        if self.check_locked():
            cls()
            div()
            print("ERROR: The server is down for maintenance. Check back later.")
            br()
            return
        cls()
        div()
        print("Create Account")
        div()
        username, password = input("Username $"), getpass.getpass("Password $")
        if username and password:
            account = StockMarketAccount(self, username, password, {x.symbol:0 for x in self.stocks})
            for stock in self.free_stocks:
                account.stocks[stock] = self.free_stocks[stock]
            self.accounts.append(account)
            cls()
            div()
            print("Successfully created account.")
            br()
        else:
            div()
            print("ERROR: Both a username and password are required.")
            br()
    def existing_account_login(self, player):
        if self.check_locked():
            cls()
            div()
            print("ERROR: The server is down for maintenance. Check back later.")
            br()
            return
        cls()
        div()
        print("Log In")
        div()
        username, password = input("Username $"), getpass.getpass("Password $")
        for account in self.accounts:
            if username == account.username and password == account.password:
                self.existing_account(player, account)
    def existing_account(self, player, account):
        while True:
            cls()
            div()
            print(account.username)
            div()
            print("Balance: {} Credits".format(player.creditCount))
            print("Portfolio: {} Credits".format(account.get_value()))
            div()
            print("[1] View Market")
            print("[2] View Portfolio")
            print("[3] Buy Shares")
            print("[4] Sell Shares")
            print("[0] Log Off")
            div()
            try:
                ch = int(input(">"))
            except:
                continue
            if ch == 1:
                self.view_market(player)
            elif ch == 2:
                self.view_portfolio(player, account)
            elif ch == 3:
                self.buy_shares(player, account)
            elif ch == 4:
                self.sell_shares(player, account)
            elif ch == 0:
                return
    def buy_shares(self, player, account):
        cls()
        symb = input("Enter Symbol $").upper()
        stock = self.get_stock(symb)
        if not stock:
            print("ERROR: Invalid stock.")
            br()
            return
        max_shares = int(player.creditCount / stock.price)
        if not max_shares:
            print("ERROR: Cannot afford any shares.")
            br()
            return
        try:
            shares = int(input("Enter Shares To Buy (Max: {}) $".format(max_shares)))
        except:
            shares = max_shares
        shares = shares if shares <= max_shares else max_shares
        account.stocks[symb] += shares
        player.creditCount -= stock.price * shares
        div()
        print("Successfully purchased {} shares for {} Credits.".format(shares, stock.price*shares))
        br()
        
    def view_market(self, player):
        cls()
        for stock in self.stocks:
            div()
            print("{} ({})".format(stock.name, stock.symbol))
            div()
            print("Opening Price: {}".format(stock.price))
            print("Last Opening Price: {}".format(stock.prevPrice))
        br()
    def view_portfolio(self, player, account):
        cls()
        div()
        for symb in account.stocks:
            value = account.stocks[symb] * self.get_stock(symb).price
            print("{}: {} Shares (Value: {})".format(symb, account.stocks[symb], value))
        br()
    def add_stock(self, stock):
        self.stocks.append(stock)
        for account in self.accounts:
            account.stocks[stock.symbol] = 0
    def add_free_stock(self, symbol, amount):
        self.free_stocks[symbol] = amount

    def sell_shares(self, player, account):
        cls()
        symb = input("Enter Symbol $").upper()
        stock = self.get_stock(symb)
        if not stock:
            print("ERROR: Invalid stock.")
            br()
            return
        try:
            shares = int(input("Enter Shares To Sell (Owned: {}) $".format(account.stocks[symb])))
        except:
            shares = account.stocks[symb]
        owned_shares = account.stocks[symb]
        shares = shares if shares <= owned_shares else owned_shares
        account.stocks[symb] -= shares
        player.creditCount += shares * stock.price
        cls()
        div()
        print("Successfully sold {} shares for {} Credits.".format(shares, shares * stock.price))
        br()

def autohack2(args):
    player = data.getNode("localhost")
    sshkill = data.getProgram("sshkill", False)
    ftpkill = data.getProgram("ftpkill", False)
    webworm = data.getProgram("webworm", False)
    lancrack = data.getProgram("lancrack", False)
    mailoverflow = data.getProgram("mailoverflow", False)
    torrentpwn = data.getProgram("torrentpwn", False)
    sqldump = data.getProgram("sqldump", False)
    if args == ["check"]:
        if not sshkill:
            print("ERROR: `sshkill` is not installed. Cannot open port 22.")
        if not ftpkill:
            print("ERROR: `ftpkill` is not installed. Cannot open port 21.")
        if not webworm:
            print("ERROR: `webworm` is not installed. Cannot open port 80.")
        if not lancrack:
            print("ERROR: `lancrack` is not installed. Cannot break port 1.")
        if not mailoverflow:
            print("ERROR: `mailoverflow` is not installed. Cannot break port 25.")
        if not sqldump:
            print("ERROR: `sqldump` is not installed. Cannot break port 1443.")
        if not torrentpwn:
            print("ERROR: `torrentpwn` is not installed. Cannot break port 6881.")
        if not None in [sshkill, ftpkill, webworm, lancrack, mailoverflow, sqldump, torrentpwn]:
            print("All programs installed.")
    elif len(args) == 1:
        node = data.getNode(args[0], True)
        if node:
            ports = [x.num for x in node.ports]
            if node.firewall:
                firewall(["crack", node.address])
            if len(ports) < node.minPorts:
                bruter([node.address], player)
            else:
                for port in node.ports:
                    if port.num == 21 and ftpkill and not port.open:
                        ftpkill.function([node.address])
                    if port.num == 22 and sshkill and not port.open:
                        sshkill.function([node.address])
                    if port.num == 80 and webworm and not port.open:
                        webworm.function([node.address])
                    if port.num == 25 and mailoverflow and not port.open:
                        mailoverflow.function([node.address])
                    if port.num == 1 and lancrack and not port.open:
                        lancrack.function([node.address])
                    if port.num == 1433 and sqldump and not port.open:
                        sqldump.function([node.address])
                    if port.num == 6881 and torrentpwn and not port.open:
                        torrentpwn.function([node.address])     
                porthack([node.address])
        else:
            print("ERROR: Invalid address.")
    else:
        div()
        print("autohack2 <address>")
        div()
        print("Semi-automatically hacks into nodes.")
        div()
        print("Version: 2.0")
        print("Supports ports: 1, 21, 22, 80, 25, 6881")
        print("Fully Automatic: Yes")
        div()
        print("autohack2 check: check if all required programs are installed")
        div()

def tor_addon(args):
    print("Addon on and working.")
    print("All port breaking tools (plus nmap and porthack) will now support Tor nodes.")

class TimeServer(Node):
    """
    An NTP time server.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, ports=[data.getPort(123), data.getPort(22), data.getPort(21)], minPorts=2, **kwargs)
    def main(self):
        date([], data.getNode("localhost"))

class WorldRouter(Node):
    """
    This node is initialised after the final mission is completed.
    """
    def __init__(self):
        super().__init__("Router", "router", "192.168.0.0")
    def main(self):
        div()
        print("ADDR\t\tHOSTNAME")
        div()
        print("192.168.0.0\t\tRouter")
        for node in data.NODES + data.TOR_NODES:
            print("{}\t\t{}".format(node.address, node.name))
        div()
    def check_health(self):
        return not self.hacked

class Newsgroup:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.content = []
    def view(self):
        while True:
            cls()
            div()
            print(self.name)
            div()
            i = 1
            for content in self.content:
                print("[{}] {}".format(i, self.get_content(content)))
                i += 1
            div()
            try:
                sel = int(input(">"))
                content = self.content[sel - 1]
            except:
                return
            if isinstance(content, Newsgroup):
                content.view()
            elif isinstance(content, Email):
                cls()
                div()
                print("FROM: {}".format(content.sender))
                print("TO: {}".format(content.receiver))
                print("SUBJECT: {}".format(content.subject))
                div()
                print(content.body)
                br()
            elif type(content) in [File, ZippedFolder, EncryptedFile]:
                fileView(content, Folder(""))
    def get_content(self, content):
        if isinstance(content, Newsgroup):
            return "{} - {} {}".format(content.name, content.desc, "" if content.content else "(Empty)")
        elif isinstance(content, Email):
            return content.subject
        elif type(content) in [File, EncryptedFile, ZippedFolder]:
            return content.name
    def add_newsgroup(self, newsgroup):
        if not isinstance(newsgroup, Newsgroup):
            raise TypeError("Must be a Newsgroup")
        self.content.append(newsgroup)
        return newsgroup
    def add_message(self, message):
        if not isinstance(message, Email):
            raise TypeError("Message is not an Email")
        self.content.append(message)
    def add_file(self, file):
        if not type(file) in [File, ZippedFolder, EncryptedFile]:
            raise TypeError
        self.content.append(file)

class Usenet(Node):
    def __init__(self, name, uid, address, minPorts=2, **kwargs):
        super().__init__(name, uid, address, ports = [data.getPort(119), data.getPort(22)], minPorts=minPorts, **kwargs)
        self.news = Newsgroup(name, "Root newsgroup of {}".format(address))
        self.users = self.users if self.users else [User("admin", "admin")]
    def main(self):
        if self.login_screen():
            self.news.view()
    def add_newsgroup(self, newsgroup):
        self.news.add_newsgroup(newsgroup)
        return newsgroup
