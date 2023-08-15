import sys
from resource.classes import *
from resource.libs import *
import data
import time
import json
import types
import inspect

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
def objToDict(obj,addItemType=True):
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
            obj2 = {"@itemType":type({}).__name__}
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
# def Directory(args):
#     div()
#     print("This is a list of reHack-related IP addresses.")
#     div()
#     print("ISP Database: 1.1.1.1")
#     print("Mission Server: 255.255.255.0")
#     print("Program Shop: 255.255.255.1")
#     print("Credits Machine: 255.255.255.255")
#     div()
#     print("It has come to the attention of reHack.Org that agents are sharing their missions server")
#     print("login credentials to friends and family. DO NOT DO THIS.")
#     print("If you are found doing this, you will 'disappear' and never return.")
#     div()
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
                print("* Confirm port 22 is valid.")
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
class MessageBoardMessage(Base):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.text = text
class MessageBoard(Node):
    def __init__(self, name, address, uid, path):
        super().__init__(name, uid, address)
        self.path = path
        self.ports = [data.getPort(80),data.getPort(1433),data.getPort(24525)]
        self.minPorts = 3
    def main(self):
        div()
        print(self.name)
        for item in os.listdir("msgboard/{}".format(self.path)):
            div()
            print("* "+item)
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
    def __init__(self, name, uid, address, path, linked = [], hacked = False):
        super().__init__(name, uid, address,files = [Folder("WebServer",[File("index.html")])], linked=linked, hacked=hacked)
        self.ports = [data.getPort(22),data.getPort(21),data.getPort(80)]
        self.path = path
        self.minPorts = 2
    def main(self):
        with open("websites/{}".format(self.path)) as f:
            for line in f.read().split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)
def ftpkill(args):
    if args:
        for item in args:
            success = False
            print("TRYING {}...".format(item))
            for node in data.NODES:
                if node.address == item:
                    print("ATTACKING PORT 21...")
                    for port in node.ports:
                        if port.num == 21:
                            time.sleep(2.5)
                            port.open = True
                            print("SUCCESSFULLY OPENED PORT 21 @ {}".format(item))
                            success = True
            if not success:
                print("Failed to attack port 21:")
                print("* Confirm port 21 is valid.")
                print("* Confirm that `{}` is a valid IP.".format(item))
    else:
        div()
        print("ftpkill <IP address(es)>")
        div()
        print("Attacks port 21 and opens it.")
        div()               
def debuginfo(args, player):
    d = objToDict(player)
    x = json.dumps(d,indent=4)
    print(x)
class Email(Base):
    def __init__(self, sender, receiver,subject=None, body=None):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
class EmailData(Base):
    def __init__(self):
        super().__init__()    
        self.inbox = []
        self.sent = []
    def receive(self, email):
        self.inbox.append(email)
    def send(self, email):
        self.sent.append(email)
class MailAccount(Base):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.data = EmailData()
class JmailServer(Node):
    def __init__(self, player):
        super().__init__("JMail","jmail","jmail.com",ports=[data.getPort(21),data.getPort(22),data.getPort(25),data.getPort(80)],minPorts=4,player=player)
        self. files += [
            Folder("Mail",[
                Folder("accounts",[
                    Folder("admin",[
                        File("account","password=rosebud")
                        ]),
                    Folder(player.name,[
                        File("account","password={}".format(player.password))
                        ])
                    ]),
                Folder("config",[
                    File("mailserver"),
                    File("mailserver.lib.so"),
                    ])
                ])
            ]
        self.users = [User("admin","rosebud",True),User(player.name,player.password)]
        self.accounts = [MailAccount("admin"),MailAccount(player.name)]
    def main(self, args=None, player=None):
        div()
        print("Welcome to JMail.")
        print("Use the official jmail client to read your email.")
        div()
        print("We currently do not have a web interface.")
        div()