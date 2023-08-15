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

def sendEmail(email):
    recipient = email.receiver
    parts = recipient.split("@")
    server = None
    for item in data.NODES:
        if item.address == parts[1]:
            server = item
            break
    if server:
        account = None
        for item in server.accounts:
            if item.name == parts[0]:
                account = item
        if account:
            account.data.receive(email)
        else:
            m = [
                "Your message to {} could not be delivered.".format(recipient),
                "The email address is invalid.",
                "Please check that the email address is valid and try again.",
                "You can use the `mxlookup` utility for a list of email accounts on our server."
                ]
            m = "\n".join(m)
            e = Email("accounts-daemon@{}".format(parts[1]),email.sender,"Your message could not be delivered",m)
            sendEmail(e)
    else:
        raise TypeError("Invalid mail server: {}".format(parts[1]))
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
                if isinstance(item,LinkNode):
                    item = data.getNode(item.link_address)
                    linkMode = True
                else:
                    linkMode = False
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
                    if isinstance(node, LinkNode):
                        node = data.getNode(node.link_address)
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
                    if isinstance(node, LinkNode):
                        node = data.getNode(node.link_address)
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
                if isinstance(item, LinkNode):
                    item = data.getNode(item.link_address)
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
        print("You must unlock at least the minimum amount as defined")
        print("by running 'nmap <hostname>'.")
        div()
class MessageBoardMessage(Base):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.text = text
class MessageBoard(Node):
    def __init__(self, name, address, uid, path):
        super().__init__(name, uid, address)
        self.path = path
        self.ports = [data.getPort(80),data.getPort(1443),data.getPort(24525)]
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
                    if isinstance(node, LinkNode):
                        node = data.getNode(node.link_address)
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
class MailServer(Node):
    def __init__(self, name, uid, address, player, users=[], hideLookup=False):
        super().__init__(name, uid,address,ports=[data.getPort(21),data.getPort(22),data.getPort(25),data.getPort(80)],minPorts=4,player=player)
        self.users = users
        self.accounts = [MailAccount("accounts-daemon")]
        self.hideLookup = hideLookup
        x = []
        for user in self.users:
            g = Folder(user.name,[
                File("account","password={}".format(user.password))
                ])
            x.append(g)
        f = [
            Folder("Mail",[
                Folder("accounts",[x])
                ])
            ]
        for user in self.users:
            a = MailAccount(user.name)
            self.accounts.append(a)
        self.files += f
    def main(self, args=None, player=None):
        print("To access this mail server, log in with a mail client.")
    def lookup(self):
        return self.accounts if not self.hideLookup else []
class JmailServer(MailServer):
    def __init__(self, player):
        super().__init__("JMail","jmail","jmail.com",player, [User("admin","rosebud"),User(player.name,player.password)])
        self.ports = [data.getPort(25),data.getPort(80),data.getPort(22)]
        self.minPorts = 2
    def main(self, args=None, player=None):
        with open("websites/jmail.com") as f:
            for line in f.read().split("\n"):
                if line == "div()":
                    div()
                else:
                    print(line)
def mxlookup(args,player=None):
    if args:
        for arg in args:
            node = data.getNode(arg)
            if isinstance(node, MailServer):
                div()
                print(node.name)
                div()
                if node.lookup():
                    for account in node.lookup():
                        print("{}@{}".format(account.name,node.address))
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
class AnonMail(MailServer):
    def __init__(self, player):
        super().__init__("AnonMail","anonmail","anon.mail",player,[User("admin"),User("noreply"),User("welcome"),User("marketing")])
        self.ports = []
        self.minPorts= 1
    def lookup(self):
        return []
class SoftwareStore(Node):
    def __init__(self, player):
        super().__init__("reHack Store","rehack_store","store.rehack.org",player=player, ports=[data.getPort(23),data.getPort(22),data.getPort(1443)],minPorts=3)
    def main(self):
        print("Welcome to the Store.")
        print("For a list of commands, type HELP.")
        while True:
            ch = input("{}@{} $".format(self.player.name, self.address))
            if ch == "help":
                div()
                print("help: list of commands")
                print("about: display version information")
                print("exit: disconnect from host")
                div()
            elif ch in ["quit","exit"]:
                return
            elif ch == "about":
                div()
                print("StoreSoft 2012.11.4")
                print("StoreSoft is a state-of-the-art online storefront making use of Telnet-over-SSH.")
                div()
def jmail(args, player):
    if args == ["list"]:
        node = data.getNode("jmail")
        acc = None
        for item in node.accounts:
            if item.name == player.name:
                acc = item
                break
        if acc:
            i = 0
            if acc.data.inbox:
                div()
                for mail in acc.data.inbox:
                    print("{}: {} ({})".format(i,mail.subject,mail.sender))
                    i += 1
                div()
                print("To view an email, run 'jmail read <id>'")
                div()
            else:
                print("Your inbox is empty.")
        else:
            print("ERROR: Invalid jmail account.")
    elif args == ["cleanup"]:
        node = data.getNode("jmail")
        for item in node.accounts:
            if item.name == player.name:
                acc = item
                break
        if acc:
            old = len(acc.data.inbox)
            acc.data.inbox = [x for x in acc.data.inbox if x.subject not in ["",None,"Your message could not be delivered"]]
            print("Deleted {} emails.".format(abs(len(acc.data.inbox)-old)))
        else:
            print("ERROR: Your jmail account could not be found.")
    elif "read" in args and len(args) == 2:
        try:
            index = int(args[1])
            node = data.getNode("jmail")
            for item in node.accounts:
                if item.name == player.name:
                    acc = item
                    break
            if acc:
                i = 0
                if 0 <= index < len(acc.data.inbox):
                    email = acc.data.inbox[index]
                    div()
                    print("FROM: {}".format(email.sender))
                    print("TO: {}".format(email.receiver))
                    print("SUBJECT: {}".format(email.subject))
                    div()
                    print(email.body)
                    div()
                else:
                    print("ERROR: Invalid email index.")
            else:
                print("ERROR: Invalid jmail account.")
        except:
            print(traceback.format_exc())
    else:
        div()
        print("jmail [args]")
        div()
        print("Client for JMail accounts.")
        div()
        print("jmail list: list all emails in inbox")
        print("jmail read <id>: read an email")
        print("jmail cleanup: removes all blank and useless emails.")
        # print("jmail send <address>: send an email (automated systems only).")
        # print("jmail del <id>: delete an email.")
        div()
        print("Account: {}@jmail.com".format(player.name))
        div()
class LinkNode(Node):
    def __init__(self, name, uid, address, link_address):
        super().__init__(name, uid, address)
        self.link_address = link_address
    def main(self):
        connect.connectStart(self.link_address)
class MailDotCom(MailServer):
    def __init__(self, name, address, player, users=[]):
        self.users = users + [User("admin")]
        super().__init__(name,address,address,player, hideLookup = True)
        self.ports = [data.getPort(21),data.getPort(22),data.getPort(25),data.getPort(80)]
        self.minPorts = 3
    def main(self):
        div()
        print("This mail server is provided by mail.com")
        print("Log in using an email client to use this mail server.")
        div()
def mailoverflow(args, player):
    if args:
        for arg in args:
            successes, failures = 0,0
            for i in range(5000):
                try:
                    em = Email("{}@jmail.com".format(player.name),arg,str(i),data.generateIP())
                    sendEmail(em)
                    successes += 1
                except:
                    failures += 1
            print("{}: {}/{} Sent".format(arg,successes-failures,successes))
    else:
        div()
        print("mailoverflow <list of email addresses>")
        div()
        print("Sends 5000 junk emails to each specified email address.")
        print("WARNING: Double-check the email address. If the email server is valid but the username is not, the emails will bounce to your inbox.")
        print("WARNING: Your email account is used to send the emails.")
        div()
class MediaWikiServer(Node):
    def __init__(self, name, uid, address, directory, homepage):
        super().__init__(name, uid, address, ports=[data.getPort(80),data.getPort(1443),getPort(22),getPort(23)],minPorts=4)
        self.files += [
            Folder("MediaWiki",[
                File("index.php"),
                File("wiki.tar.gz"),
                File("index.js"),
                File("favicon.ico"),
                ])
            ]
    def main(self):
        print("ERROR: Client incorrectly configured.")
def sweep(args):
    print("Begin sweep...")
    nodes = []
    try:
        for a in range(256):
            for b in range(256):
                print("Begin {}.{}.x.x".format(a,b))
                for c in range(256):
                    for d in range(256):
                        node = data.getNode(f"{a}.{b}.{c}.{d}")
                        if node:
                            print("{}: {}".format(node.address,node.name))
                            nodes.append(node)
    except KeyboardInterrupt:
        pass
    print("Finished sweep.")
    if nodes:
        for node in nodes:
            print("{}: {}".format(node.address,node.name))
    else:
        print("No nodes found.")