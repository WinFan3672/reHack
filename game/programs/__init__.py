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
import uuid
import random
import copy
import getpass
import copy
import concurrent.futures
import re
import getpass


def pickSelection(a_list, amount=1):
    l = copy.copy(a_list)
    random.shuffle(l)

    x = []
    for i in range(amount):
        z = random.choice(l)
        x.append(z)
        l.remove(z)

    return x


def sendEmail(email):
    recipient = email.receiver
    parts = recipient.split("@")
    server = None
    for item in data.NODES:
        if item.address == parts[1]:
            server = item
            break
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
                "The email address is invalid.",
                "Please check that the email address is valid and try again.",
                "You can use the `mxlookup` utility for a list of email accounts on our server.",
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


def objToDict(obj, addItemType=True):
    """
    Recursively convert an object and all its attributes to a dictionary.
    """
    if isinstance(obj, (int, float, bool, str)):
        return obj
    if inspect.isclass(obj):
        return {"__class__": obj.__name__}

    if isinstance(obj, (tuple, list)):
        return [objToDict(x) for x in obj]

    if isinstance(obj, dict):
        if addItemType:
            obj2 = {"@itemType": type({}).__name__}
        obj2.update(obj)
        obj = obj2
        return {key: objToDict(value) for key, value in obj.items()}
    obj_dict = {}
    if addItemType:
        obj_dict["@itemType"] = type(obj).__name__
    for attr in dir(obj):
        if attr.startswith("__") and attr.endswith("__"):
            continue
        if attr == "dic":
            continue
        if getattr(obj, attr) is None:
            obj_dict[attr] = "<class 'none'>"
            continue
        if callable(getattr(obj, attr)):
            obj_dict[attr] = f"<function '{attr}'>"
            continue
        value = getattr(obj, attr)
        obj_dict[attr] = objToDict(value)
    return obj_dict


def Help(args):
    div()
    for item in sorted(data.PROGRAMS):
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
                item.nmap = True
                div()
                print("Hostname: {}".format(item.name))
                print("Exposed Ports: {}".format(len(item.ports)))
                print("Min. Ports To Crack: {}".format(item.minPorts))
                if item.hacked:
                    print("HOST VULNERABILITY ACTIVE.")
                if item.firewall:
                    print("WARNING: FIREWALL ACTIVE.")
                if item.ports:
                    div()
                    print("PORT\tSTATE\tNAME")
                    div()
                for i in sorted(item.ports, key=lambda x:x.num):
                    print("{}\t{}\t{}".format(i.num, "OPEN" if i.open else "CLOSED", i.name))
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


class PortBreakingTool(Base):
    def __init__(self, name, port, unlocked=False, price=0):
        super().__init__()
        self.name = name
        self.port = port
        self.program = Program(self.name, self.function, unlocked=unlocked, price=price)

    def function(self, args):
        if len(args) == 1:
            item = args[0]
            success = False
            node = data.getNode(item)
            if node:
                print(f"ATTACKING PORT {self.port}...")
                if node.firewall:
                    print("ERROR: Attack blocked by firewall.")
                else:
                    for port in node.ports:
                        if port.num == self.port:
                            time.sleep(2.5)
                            port.open = True
                            print(
                                "SUCCESSFULLY OPENED PORT {} @ {}".format(
                                    self.port, item
                                )
                            )
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
                    if item.firewall:
                        print("ERROR: Attack blocked by firewall.")
                    else:
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
        print("You must unlock at least the minimum amount as defined")
        print("by running 'nmap <hostname>'.")
        div()


class MessageBoardMessage(Base):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.text = text


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

    def main(self):
        div()
        print(self.name)
        for item in os.listdir("msgboard/{}".format(self.path)):
            div()
            print("* " + item)
            with open("msgboard/{}/{}".format(self.path, item)) as f:
                for line in f.read().split("\n"):
                    if line == "div()":
                        div()
                    else:
                        print(line)
        div()

    def add_message(self, message):
        if isinstance(message, MessageBoardMessage):
            self.messages.append(message)
        else:
            raise TypeError("The message you tried to add is invalid.")


class WebServer(Node):
    def __init__(
        self, name, uid, address, path, linked=[], hacked=False, minPorts=2, users=[]
    ):
        super().__init__(
            name,
            uid,
            address,
            files=[Folder("WebServer", [File("index.html")])],
            linked=linked,
            hacked=hacked,
        )
        self.ports = [data.getPort(22), data.getPort(21), data.getPort(80)]
        self.path = path
        self.users = users
        self.minPorts = minPorts

    def main(self):
        with open("websites/{}".format(self.path)) as f:
            for line in f.read().split("\n"):
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
            files=[Folder("Tor",[File("torserver.elf")]), Folder("WebBrowser", [File("index.html")])],
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

def debuginfo(args, player):
    if args == ["player"]:
        d = objToDict(player)
        x = json.dumps(d, indent=4)
        print(x)
    elif args == ["passwd"]:
        with open("data/passwords.txt") as f:
            print(random.choice(f.read().split("\n")))
    elif args == ["mission"]:
        while player.currentMission:
            print("Completed: {}".format(player.currentMission.name))
            player.currentMission.end()
    elif args == ["ip"]:
        div()
        print("debug ip [arguments]")
        div()
        print("Positional arguments:")
        print("    list: lists all nodes and their info")
        print("    info: get info about a node")
        div()
    elif args == ["ip", "list"]:
        div()
        print("UID\t\tHOSTNAME")
        div()
        for x in data.NODES:
            print("{}\t\t{}".format(x.uid, x.name))
        div()
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
    else:
        div()
        print("debug <args>")
        div()
        print("Positional arguments:")
        print("    player: print out player class")
        print("    passwd: print a random password that can be brute-forced")
        print("    ip: lists information about nodes")
        print("    mission: complete an entire mission series.")
        print("    gen: lists all IP addresses generated randomly.")
        print("    lan: displays info about a LAN")
        div()
        print("WARNING: This program is not intended for use by anyone other than the developers.")
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
        )
        self.users = users
        self.accounts = [MailAccount("accounts-daemon")]
        self.accounts += [x for x in accounts if ininstance(x, MailAccount)]
        self.hideLookup = hideLookup
        self.emails = []
        x = []
        for user in self.users:
            self.accounts.append(MailAccount(user.name, user.password))

    def main(self, args=None, player=None):
        print("To access this mail server, log in with a mail client.")

    def lookup(self):
        return self.accounts if not self.hideLookup else []

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
                        "{}: {} ({}-->{})".format(
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


# def MailDotCom(name, address, player, users=[]):
#     s = MailServer(name, address, address, player)
#     s.lookup = lambda:return [MailAccount("admin")]
#     s.ports = [data.getPort(21), data.getPort(22), data.getPort(25), data.getPort(80)]
#     s.minPorts = 4
#     s.accounts = [MailAccount("admin")]
#     for item in users:
#         s.accounts.append(MailAccount(item.name))
#     return s


class MailDotCom(MailServer):
    def __init__(self, name, address, player, users=[]):
        super().__init__(name, address, address, player)
        self.ports = [
            data.getPort(21),
            data.getPort(22),
            data.getPort(25),
            data.getPort(80),
        ]
        self.minPorts = 4
        self.accounts = [MailAccount("admin")]
        for item in users:
            self.accounts.append(MailAccount(item.name, item.password))

    def lookup(self):
        return [MailAccount("admin")]


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
        return [x for x in data.PROGRAMS if not x.unlocked]

    if args == ["list"]:
        div()
        for item in getPrograms(player):
            print("{} ({} Cr.)".format(item.name, item.price))
        div()
    elif "buy" in args and len(args) == 2:
        try:
            pid = args[1]
            programs = getPrograms(player)
            valid = False
            for program in programs:
                if program.name == pid:
                    valid = True
                    if player.creditCount >= program.price:
                        player.creditCount -= program.price
                        program.unlocked = True
                        print(
                            "Successfully purchased {} for {} Cr.".format(
                                program.name, program.price
                            )
                        )
                    else:
                        print("ERROR: Cannot afford program.")
            if not valid:
                print("ERROR: Invalid program.")
        except Exception as e:
            print("ERROR: {}".format(e))
    elif args == ["balance"]:
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

    def main(self):
        div()
        print("This is the International ISP Hub.")
        print("It is important to the function of the Internet.")
        div()

    def main_hacked(self):
        print("Welcome to the IIH Console.")
        print("Run 'help' for a command list.")
        while True:
            ch = input("admin@{} $".format(self.address))
            if ch in ["quit", "exit"]:
                return
            elif ch == "help":
                div()
                print("help: Command list")
                print("cls: clear terminal")
                print("list: list all nodes you have connected to.")
                print("reassign: reassign an existing IP to a new one.")
                print("delete: Delete an IP from DNS records, making it unreachable.")
                print("mklink: Creates a node link")
                print("exit: Disconnect from host")
                div()
            elif ch in ["clear", "cls"]:
                cls()
            elif ch == "list":
                div()
                for node in [x for x in data.NODES if x.visited]:
                    print("{}: {}".format(node.name, node.address))
                div()
            elif ch == "delete":
                div()
                print("delete <IP Address>")
                div()
                print("Removes an IP from all DNS records.")
                print("This is permanent.")
            elif ch.startswith("delete "):
                ip = ch[7:]
                node = data.getNode(ip)
                if node:
                    print("WARNING! This is irreversible!")
                    print(
                        "By doing this, the server you are targeting ({}) will be inaccessible FOREVER.".format(
                            ip
                        )
                    )
                    print("If you understand this, type 'I KNOW WHAT I AM DOING'.")
                    if input(">>>") == "I KNOW WHAT I AM DOING":
                        if node.address in [
                            data.getNode(x).address for x in self.blocklist
                        ]:
                            print("ERROR: This node is not removable.")
                        else:
                            data.NODES.remove(node)
                            print("Removed node successfully.")
                    else:
                        print("Operation canceled.")
                else:
                    print("ERROR: Invalid IP address.")
            elif ch == "reassign":
                div()
                print("reassign <IP>")
                div()
                print("Reassigns an existing server to a new IP.")
                div()
            elif ch.startswith("reassign "):
                ip = ch[9:]
                node = data.getNode(ip)
                if node:
                    node.address = data.generateIP()
                    print("Reassigned {} to {}.".format(node.name, node.address))
                else:
                    print("ERROR: Invalid IP.")
            # elif ch == "mklink":
            #     div()
            #     print("mklink <original ip> <link ip>")
            #     div()
            #     print("Creates a DNS link to an IP address.")
            #     div()
            # elif ch.startswith("mklink "):
            #     args = ch[7:].split(" ")
            #     if len(args) == 2:
            #         node = data.getNode(args[0])
            #         if node:
            #             lnk = LinkNode(args[0],args[1])
            #             data.NODES.append(lnk)
            #             print("Created DNS link.")
            #             print("NOTE: DNS links are not standardised and not all programs work well with them.")
            #         else:
            #             print("ERROR: Invalid IP address.")
            #     else:
            #         print("ERROR: Invalid syntax.")
            #         print(args)
            else:
                print("ERROR: Invalid command.")


class Note(Base):
    def __init__(self, text):
        super().__init__()
        self.text = text


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
            data.getPort(22),
            data.getPort(21),
            data.getPort(23),
            data.getPort(6881),
        ]
        self.minPorts = 5
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


class WikiServer(Node):
    def __init__(self, name, uid, address, folder, homepage="Main Page"):
        super().__init__(name, uid, address)
        self.ports = [data.getPort(22), data.getPort(80), data.getPort(1433)]
        self.minPorts = 3
        self.folder = folder
        self.homepage = homepage

    def main(self):
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
        if callable(self.end_function):
            self.end_function()

class LANMission(Mission):
    def __init__(self, player, mission_id, name, target, lanserver, start_email, next_id=None, start_function=None, end_function=None, reward=0):
        super().__init__(player, mission_id, name, target, start_email, next_id=next_id, start_function=start_function, end_function=end_function, reward=reward)
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
    def __init__(self, name, uid, address, player, missions=[]):
        super().__init__(name, uid, address)
        self.player = player
        self.ports = [data.getPort(22), data.getPort(1433), data.getPort(23)]
        self.users = [User("admin"), User(self.player.name)]
        self.minPorts = 4
        self.main_hacked = self.main
        self.missions = missions

    def main(self):
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
                    data.getNode("rejected").missions.append(
                        copy.deepcopy(self.player.currentMission)
                    )
                    self.player.currentMission = None
                    print("Cancelled the mission.")
                    print(
                        "You can re-accept cancelled missions in the Rejects Hub: rejects.rehack.org"
                    )
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
        return self.target in [x for x in data.PROGRAMS if x.unlocked]


def nodecheck(args):
    d = {
        Node: "standard",
        WebServer: "website",
        MailServer: "mailserver",
        WikiServer: "wiki",
        MessageBoard: "messageboard",
        JmailServer: "jmail",
        AnonMail: "anonmail",
        MailDotCom: "maildotcom_instance",
        ISPNode: "isp",
        XOSDevice: "xosdevice",
        MissionServer: "contract_hub",
        VersionControl: "version_control",
        type(None): "invalid",
        GlobalDNS: "global_dns",
    }
    if args:
        for arg in args:
            node = type(data.getNode(arg))
            print("{}: {}".format(arg, d.get(node, "unknown")))
    else:
        div()
        print("nodecheck [list of ip addresses]")
        div()
        print("Shows a node's type.")
        div()


def getEmails(account):
    return account.inbox


def mailman(self, domain, player):
    cls()
    print("Welcome. For a command list, type HELP.")
    while True:
        ch = input("{}@{} $".format(self.name, domain))
        if ch == "help":
            div()
            print("help: command list")
            print("cls: clear the screen")
            if not f"{self.name}@{domain}" in player.saved_accounts.keys():
                print("save: save this account for future use")
            print("list: list all emails")
            print("read <id>: read an email")
            print("exit: exit mailman")
            div()
        elif ch in ["exit", "quit"]:
            return
        elif ch in ["cls", "clear"]:
            cls()
        elif ch == "":
            continue
        elif ch == "list":
            i = 0
            if getEmails(self.data):
                div()
                for item in getEmails(self.data):
                    print(
                        "{}: {} ({}-->{}) {}".format(
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
                print("Your inbox is empty.")
        elif ch == "read":
            div()
            print("read <id>")
            div()
            print("Read an email.")
            div()
        elif ch == "save":
            player.saved_accounts["{}@{}".format(self.name, domain)] = self.password
            print("Successfully saved account.")
            print("For a list of accounts, run 'mailman list'.")
        elif ch.startswith("read "):
            try:
                index = int(ch[5:])
                if 0 <= index <= len(getEmails(self.data)):
                    email = getEmails(self.data)[index]
                    email.read = True
                    div()
                    print(email.body)
                    div()
                else:
                    print("ERROR: Invalid email.")
            except:
                print(traceback.format_exc())
        else:
            print("ERROR: Invalid command.")


def mailman_base(args, player):
    if len(args) == 2:
        try:
            account = args[0]
            passwd = args[1]
            parts = account.split("@")
            node = data.getNode(parts[1])
            if isinstance(node, MailServer):
                found_acc = False
                for acc in node.accounts:
                    if acc.name == parts[0]:
                        found_acc = True
                        if acc.password:
                            if acc.password == passwd:
                                mailman(acc, parts[1], player)
                            else:
                                print("ERROR: Incorrect password.")
                        else:
                            print("ERROR: The mail account cannot be logged into.")
                if not found_acc:
                    print("ERROR: Invalid mail account.")
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
        self.offerings = {
            "base":
                {
                    "node":Node("","","",ports=[data.getPort(22),data.getPort(6881)]),
                    "price":500,
                    "description":"A basic node with no security."
                 },
            "base_plus":{
                "node":Node("","","",ports=[data.getPort(22),data.getPort(6881)], minPorts=2**16),
                "price":750,
                "description":"A basic node with full security, including a firewall.",
                },
            "xphone":{
                "node":XOSDevice("","",""),
                "price":300,
                "description":"A standard xPhone 3.",
                },
            "mail":{
                "node":MailServer("","","",player),
                "description":"A fully-fledged mail server.",
                "price":1500,
                },
            "mailplus":{
                "node":MailServer("","","",player, hideLookup=True, minPorts=2**16),
                "description":"A fully-fledged mail server with full security.",
                "price":2500,
                },
            }
        self.offerings["base_plus"]["node"].firewall = Firewall(makeRandomString(64),15)
        self.offerings["mailplus"]["node"].firewall = Firewall(makeRandomString(64),15)
        self.buckets = []
    def main(self, player):
        cls()
        print("Welcome to MasterVPS.")
        print("For a command list, type HELP.")
        while True:
            ch = input("mastervps #")
            if ch == "help":
                div()
                print("help: command list")
                print("cls: clear terminal")
                print("list: list all purchase options")
                print("bucket list: lists all running buckets")
                print("bucket spinup: spin up a bucket")
                print("balance: display balance")
                print("exit: disconnect from host")
                div()
            elif ch == "list":
                for bucket in self.offerings.keys():
                    b = self.offerings[bucket]
                    div()
                    print(bucket)
                    div()
                    print(b["description"])
                    print("Price: {}".format(b["price"]))
                div()
            elif ch == "bucket spinup":
                div()
                print("bucket spinup <id>")
                div()
                print("Spin up a bucket of type <id>.")
                print("For a list of ID's, run 'list'.")
                div()
            elif ch.startswith("bucket spinup "):
                ch = ch[14:]
                if ch in self.offerings.keys():
                    if player.creditCount >= self.offerings[ch]["price"]:
                        if ch in ["xphone"]:
                            passwd = "alpine"
                        else:
                            passwd = getpass.getpass("Admin Password $")
                        node = copy.deepcopy(self.offerings[ch]["node"])
                        node.name = "MasterVPS: {}".format(ch)
                        node.uid = "mastervps_{}".format(random.randint(2**16,2**32))
                        node.address = data.generateIP()
                        node.offeringType = ch
                        node.linked = ["mastervps_central"]
                        node.users = [User("admin",passwd if passwd else "password")]
                        self.buckets.append(node)
                        data.NODES.append(node)
                        print("Successfully spun up bucket.")
                        print("The IP address is: {}".format(node.address))
                        print("For a list, run 'bucket list'.")
                        if not passwd:
                            print("WARNING: You did not specify a password. A default password ('password') has been used instead.")
                        elif ch in ["xphone"]:
                            print("WARNING: The password for an xOS device is 'alpine'.")
                        player.creditCount -= self.offerings[ch]["price"]
                    else:
                        print("ERROR: Cannot afford bucket.")
                else:
                    print("ERROR: Invalid bucket ID.")
            elif ch == "bucket list":
                if self.buckets:
                    i = 0
                    for node in self.buckets:
                        print("{}: {} ({})".format(i,node.address,node.offeringType))
                else:
                    print("You have not spun up any buckets.")
            elif ch == "":
                continue
            elif ch in ["balance", "bal"]:
                print(player.creditCount)
            elif ch in ["clear", "cls"]:
                cls()
            elif ch in ["quit", "exit"]:
                return
            else:
                print("ERROR: Invalid command.")


def firewall(args):
    if "test" in args and len(args) == 2:
        node = data.getNode(args[1])
        if node:
            if node.firewall:
                print("Firewall active.")
            else:
                print("Firewall inactive.")
        else:
            print("ERROR: Invalid IP address.")
    elif "crack" in args and len(args) == 2:
        node = data.getNode(args[1])
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
            else:
                print("ERROR: No firewall active.")
        else:
            print("ERROR: Invalid IP address.")
    elif "solve" in args and len(args) == 3:
        node = data.getNode(args[1])
        if node:
            if node.firewall:
                if node.firewall.solution == args[2]:
                    print("Successfully solved firewall.")
                    print("Firewall disabled.")
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
        super().__init__("Global DNS Service","gdns","8.8.8.8",minPorts=2**16,ports=[data.getPort(65536)])
        self.main_hacked = self.main
    def main(self):
        print("This is the Global DNS Server.")
        print("It is important for the function of the Internet.")

class VersionControl(Node):
    def __init__(self, name, uid, address, commits = [], users = [], linked = []):
        super().__init__(name, uid, address, users=users, linked=linked, ports=[data.getPort(1433),data.getPort(80),data.getPort(22),data.getPort(21)],minPorts=4)
        self.commits = [x for x in commits if isinstance(x,Commit)]
    def main_hacked(self):
        if self.commits:
            for x in self.commits:
                print("* {}".format(x))
        else:
            print("ERROR: No commit history.")

def save(args, player):
    try:
        player.save()
    except Exception as e:
        print(e)

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
    if args:
        for arg in args:
            node = data.getTorNode(arg)
            if node:
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
            else:
                print("ERROR: Onionsite '{}' not found.".format(arg))
    else:
        div()
        print("tor [onionsite]")
        div()
        print("Connects to a Tor node.")
        div()

class SignupService(Node):
    def __init__(self, uid, url, agent_id):
        super().__init__("Signup Service", uid, url, ports=[data.getPort(80), data.getPort(21), data.getPort(22)], minPorts=65536)
        self.name = "Signup Service"
        self.agent_id = agent_id
    def main(self):
        node = data.getNode(self.agent_id)
        print("Welcome to the signup server for {}.".format(node.name))

        username = ""
        while not username:
            username = input("Enter Your Username $")
            if not username:
                print("ERROR: Must type a username.")
            if username in [x.name for x in node.users]:
                print("ERROR: That user already exists.")
                username = ""

        password = ""
        while not password:
            password = getpass.getpass("Enter a password $")
            if not password:
                print("ERROR: You must type a password.")

        node.users.append(User(username, password))
        print("Successfully added user.")
        if isinstance(Node, MailServer):
            print("Your email address is: {}@{}".format(username, node.address))

def tormail(args):
    if args:
        pass
    else:
        div()
        print("tormail <email address> [password]")
        div()
        print("Log into a Tor email service.")
        div()

class LocalAreaNetwork(Node):
    def __init__(self, name, uid, address, minPorts=1):
        super().__init__(name, uid, address, ports = [data.getPort(1)], minPorts=minPorts)
        self.devices = []
        self.locked = False
    def add_device(self, device):
        if not self.locked:
            self.devices.append(device)
    def add_router(self):
        self.devices.insert(0, Router(self.devices))
        self.locked = True
    def main(self):
        print("ERROR: Access denied.")
    def main_hacked(self):
        print("ERROR: A LAN client such as `lanconnect` is required to connect to a LAN router and access its network.")
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
        for x in self.devices:
            print("{}\t\t{}".format(x.address, x.name))
        div()
def LANTool(args):
    print("ERROR: This program is intended for use with `lanconnect`.")
def LANConnect(args, player):
    def main(node, player):
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
                print("HOST VULNERABILITY ACTIVE")
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
        for x in ["porthack", "sshkill", "ftpkill", "webworm", "nmap", "lancrack"]:
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
            elif ch in ["quit","exit"]:
                return
            else:
                print("ERROR: Invalid program.")


    def findNode(address):
        for n in data.NODES:
            if n.address == address:
                return n
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
            # return
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

class NodeTracker(Node):
    def __init__(self, name, uid, address):
        super().__init__(name, uid, address)
        self.nodes = []
    def add_node(self, uid):
        if isinstance(uid, Node):
            n = uid
        else:
            n = data.getNode(uid)
        self.nodes.append(NodeTrackerNode(n.address, n.name))
    def add_lan_node(self, lan_uid, uid):
        lan = data.getNode(lan_uid)
        node = lan.getNode(uid)
        self.nodes.append(NodeTrackerLanNode(lan.address, node.address, node.name))
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
    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance
        self.transactions = []
    def __str__(self):
        return "Account {} (Balance={:,} Cr.)".format(self.number, self.balance)
    def check(self, number, pin):
        return self.number == number and self.pin == pin

class BankBackEnd(Node):
    def __init__(self, name, uid, address):
        super().__init__(name, uid, address)
        self.accounts = [BankAccount(000000, self.gen_pin(), 0)]
    def get_next_num(self):
        nums = [x.number for x in self.accounts]
        running = True
        while running:
            num = random.choice(range(11111111,99999999))
            running = num in nums
        return num
    def gen_pin(self):
        s = ''
        for x in range(6):
            s += random.choice(list("1234567890"))
        return s
    def add_account(self, number=0, pin='', balance=0):
        acc = BankAccount(number if number else self.get_next_num(), pin if pin else self.gen_pin(), balance)
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
                div()
                print("exit/quit: disconnects from host")
                div()
            elif ch == "":
                pass
            elif ch == "list":
                for acc in self.accounts:
                    print(acc)
            elif ch in ["clear", "cls"]:
                cls()
            elif ch in ["quit", "exit"]:
                return
            else:
                print("ERROR: Invalid command.")

class BankServer(Node):
    def __init__(self, name, uid, address, backend):
        super().__init__(name, uid, address)
        self.backend = data.getNode(backend)
        if not isinstance(self.backend, BankBackEnd):
            raise Exception("Invalid backend server")
