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
def sendEmail(email):
    recipient = email.receiver
    parts = recipient.split("@")
    server = None
    for item in data.NODES:
        if item.address == parts[1]:
            server = item
            break
    if isinstance(server,MailServer):
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
                item.nmap = True
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
    def __init__(self, name, address, uid, path, ports=None,minPorts=3):
        if ports is None:
            self.ports = [data.getPort(80),data.getPort(1433),data.getPort(24525)]
        else:
            self.ports = ports
        super().__init__(name, uid, address)
        self.path = path
        self.ports = ports
        self.minPorts = minPorts
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
    def __init__(self, name, uid, address, path, linked = [], hacked = False, minPorts=2, users = []):
        super().__init__(name, uid, address,files = [Folder("WebServer",[File("index.html")])], linked=linked, hacked=hacked)
        self.ports = [data.getPort(22),data.getPort(21),data.getPort(80)]
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
    def __init__(self, name, autoresponse = None):
        super().__init__()
        self.name = name
        self.data = EmailData(autoresponse)
class MailServer(Node):
    def __init__(self, name, uid, address, player, users=[], hideLookup=False, minPorts=4):
        super().__init__(name, uid,address,ports=[data.getPort(21),data.getPort(22),data.getPort(25),data.getPort(80)],minPorts=minPorts,player=player)
        self.users = users
        self.accounts = [MailAccount("accounts-daemon")]
        self.hideLookup = hideLookup
        x = []
        for user in self.users:
            self.accounts.append(MailAccount(user.name))
    def main(self, args=None, player=None):
        print("To access this mail server, log in with a mail client.")
    def lookup(self):
        return self.accounts if not self.hideLookup else []
    def main_hacked(self):
        def grabEmails(self):
            emails = []
            for acc in self.accounts:
                for item in acc.data.inbox:
                    emails.append(item)
                for item in acc.data.sent:
                    emails.append(item)
            return emails
        print("Mail Server Admin Panel")
        print("Run 'help' for a command list.")
        while True:
            ch = input("admin@{} $".format(self.address))
            if ch in ["quit","exit"]:
                return
            elif ch == "help":
                div()
                print("help: command list")
                print("list: list all emails in server")
                print("read <id>: view an email")
                print("users: print all users")
                print("exit: disconnect from host")
                div()
            elif ch in ["cls","clear"]:
                cls()
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
                    print("{}: {} ({}-->{})".format(i,item.subject,item.sender,item.receiver))
                    i += 1
            else:
                print("ERROR: Invalid command.")
class JmailServer(MailServer):
    def __init__(self, player):
        super().__init__("JMail","jmail","jmail.com",player, [User("admin","rosebud"),User(player.name,player.password),User("xwebdesign")])
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
        super().__init__("AnonMail","anonmail","anon.mail",player,[User("admin"),User("noreply"),User("welcome"),User("marketing")],hideLookup=True)
        self.ports = []
        self.minPorts= 4
    def create_user(self, address):
        u = User("").password
        acc = ForwardingAccount(u,address)
        self.accounts.append(acc)
        d = objToDict(acc)
        x = json.dumps(d,indent=4)
        print(x)
        br()
        return u
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
    # elif "send" in args and len(args) == 2:
    #     e = Email("{}@jmail.com".format(player.name),args[1],"Automated Email","GET Request made by JMail client.")
    elif args == ["del"]:
        div()
        print("jmail del <id>")
        div()
        print("Delete a message.")
        div()
    elif "del" in args and len(args) == 2:
        try:
            index = int(args[1])
            node = data.getNode("jmail.com")
            account = None
            for acc in node.accounts:
                if acc.name == player.name:
                    account = acc
            if account:
                if 0 <= index <= len(account.data.inbox):
                    account.data.inbox.pop(index)
                    print("Removed email.")
                else:
                    print("ERROR: Invalid email index.")
            else:
                pritn("ERROR: Invalid jmail account.")
        except Exception as e:
            print("ERROR: {}".format(e))
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
        print("jmail del <id>: delete an email.")
        div()
        print("Account: {}@jmail.com".format(player.name))
        div()
class LinkNode(Node):
    def __init__(self, name, uid, address, link_address):
        super().__init__(name, uid, address)
        self.link_address = link_address
    def main(self):
        connect.connectStart(self.link_address)
# class MailDotCom(MailServer):
#     def __init__(self, name, address, player, users=[]):
#         self.users = users + [User("admin")]
#         super().__init__(name, address, address, player, hideLookup=True)
#         self.ports = [data.getPort(21), data.getPort(22), data.getPort(25), data.getPort(80)]
#         self.minPorts = 4
#         for user in self.users:
#             self.accounts.append(MailAccount(user.name))
#     def main(self):
#         div()
#         print("This mail server is provided by mail.com")
#         print("Log in using an email client to use this mail server.")
#         div()
def MailDotCom(name, address, player, users=[]):
    s = MailServer(name, address, address, player, hideLookup=True)
    s.ports= [data.getPort(21), data.getPort(22), data.getPort(25), data.getPort(80)]
    s.minPorts = 4
    s.accounts = [MailAccount("admin")]
    for item in users:
        s.accounts.append(MailAccount(item.name))
    return s
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
        super().__init__(name, uid, address, ports=[data.getPort(80),data.getPort(1433),getPort(22),getPort(23)],minPorts=4)
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
        i = 0
        for item in getPrograms(player):
            print("{}: {} ({} Cr.)".format(i, item.name, item.price))
            i += 1
    elif "buy" in args and len(args) == 2:
        try:
            pid = int(args[1])
            programs = getPrograms(player)
            if 0 <= pid <= len(programs):
                program = programs[pid]
                if player.creditCount >= program.price:
                    player.creditCount -= program.price
                    program.unlocked = True
                    print("Successfully purchased {} for {} Cr.".format(program.name, program.price))
                else:
                    print("ERROR: Cannot afford program.")
            else:
                print("ERROR: Invalid ID.")
        except Exception as e:
            print("ERROR: {}".format(e))
    elif args == ["balance"]:
        print(player.creditCount)
    else:
        div()
        print("store <args>")
        div()
        print("Store for purchasing software.")
        div()
        print("store list: list all software for sale.")
        print("store buy <ID>: buy a program")
        print("store balance: prints out how many credits you have.")
        div()
def anonclient(args, player):
    print("AnonMail is temporarily unavailable.")
    return
    if "create" in args and len(args) == 2:
        try:
            address = args[1]
            parts = address.split("@")
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
                    node = data.getNode("anon.mail")
                    u = node.create_user(address)
                    print("Successfully created: {}@anon.mail".format(u))
                else:
                    print("ERROR: The email account is invalid.")
            else:
                print("ERROR: '{}' is not a valid email server.".format(parts[1]))
        except Exception as e:
            print("ERROR: {}".format(e))
    elif args == ["create"]:
        try:
            address = "{}@jmail.com".format(player.name)
            parts = address.split("@")
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
                    node = data.getNode("anon.mail")
                    u = node.create_user(address)
                    print("Successfully created: {}@anon.mail".format(u))
                else:
                    print("ERROR: The email account is invalid.")
            else:
                print("ERROR: '{}' is not a valid email server.".format(parts[1]))
        except Exception as e:
            print("ERROR: {}".format(e))                
    else:
        div()
        print("anonmail [args]")
        div()
        print("Client for anonmail, the anonymous email forwarder.")
        div()
        print("anonmail create [email address]: create a new identity.")
        div
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
    def __init__(self, name="International ISP Hub",address="1.1.1.1"):
        super().__init__(name,address,address)
        self.ports = [data.getPort(21),data.getPort(22), data.getPort(1433), data.getPort(80)]
        self.minPorts = 4
        self.linked = ["shodan"]
        self.users = [User("admin","potholes")]
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
            if ch in ["quit","exit"]:
                return
            elif ch == "help":
                div()
                print("help: Command list")
                print("list: list all nodes you have connected to.")
                print("reassign: reassign an existing IP to a new one.")
                print("delete: Delete an IP from DNS records, making it unreachable. DANGEROUS!")
                print("mklink: Creates a node link")
                print("exit: Disconnect from host")
                div()
            elif ch == "list":
                div()
                for node in [x for x  in data.NODES if x.visited]:
                    print("{}: {}".format(node.name,node.address))
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
                    print("By doing this, the server you are targeting ({}) will be inaccessible FOREVER.".format(ip))
                    print("If you understand this, type 'I KNOW WHAT I AM DOING'.")
                    if input(">>>") == "I KNOW WHAT I AM DOING":
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
            elif ch == "mklink":
                div()
                print("mklink <original ip> <link ip>")
                div()
                print("Creates a DNS link to an IP address.")
                div()
            elif ch.startswith("mklink "):
                args = ch[7:].split(" ")
                if len(args) == 2:
                    node = data.getNode(args[0])
                    if node:
                        lnk = LinkNode(node.name, args[1], args[1], args[0])
                        data.NODES.append(lnk)
                        print("Created DNS link.")
                        print("NOTE: DNS links are not standardised and not all programs work well with them.")
                    else:
                        print("ERROR: Invalid IP address.")
                else:
                    print("ERROR: Invalid syntax.")
                    print(args)
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
    def __init__(self, name, uid, address, notes = [], accounts = [], password="alpine",model="xphone"):
        super().__init__(name, uid, address)
        self.users = [User("admin",password)]
        self.ports = [data.getPort(22),data.getPort(21),data.getPort(23),data.getPort(6881)]
        self.minPorts = 5
        self.notes = notes
        self.accounts = accounts
        self.model=model
        self.battery_health = random.randint(60,99)
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
            elif ch in ["quit","exit"]:
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
            elif ch =="info":
                inf = data.XOS_DEVICES[self.model]
                div()
                print("Model: {}".format(inf.get("name","Unknown Device")))
                print("CPU Freq: {}".format(inf.get("cpu","Unreported")))
                print("Total Memory: {}".format(inf.get("ram","Unreported")))
                print("Storage: {}".format(inf.get("storage","Unreported")))
                print("Battery Capacity: {}".format(inf.get("battery","Unknown")))
                print("Battery Health: {}%".format(self.battery_health))
                div()
            elif ch in ["clear","cls"]:
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
        self.ports = [data.getPort(22),data.getPort(80),data.getPort(1433)]
        self.minPorts = 3
        self.folder = folder
        self.homepage = homepage
    def main(self):
        with open("wikis/{}/{}".format(self.folder,self.homepage)) as f:
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
                    with open("wikis/{}/{}".format(self.folder,ch[5:])) as f:
                        for line in f.read().split("\n"):
                            if line == "div()":
                                div()
                            else:
                                print(line)
                except:
                    print("ERROR: Invalid page name.")
            elif ch in ["quit","exit"]:
                return
            elif ch in ["cls","clear"]:
                cls()
            else:
                print("ERROR: Invalid command.")
class Mission(Base):
    def __init__(self, player, mission_id, name, target, start_email, end_email=None, reward=0, next_id=None):
        super().__init__()
        self.mission_id = mission_id
        self.name = name
        self.reward = reward
        self.start_email = start_email
        self.end_email = end_email
        self.target = target
        self.next_id = next_id
        self.player = player
    def start(self):
        sendEmail(self.start_email)
        self.player.currentMission = self
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
def mission_program(args, player):
    if player.currentMission:
        if player.currentMission.check_end():
            div()
            print("Congratulations! You finished the mission!")
            print("You have been awarded {} credits.".format(player.currentMission.reward))
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
                            print("* {}: {}".format(log.address,log.text))
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