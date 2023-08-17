from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
from game.programs import JmailServer, MailAccount, EmailData, Email, sendEmail, MailServer, AnonMail, MailDotCom, Mission, ConnectMission, NMapMission
import data
import sys

def getProgram(name):
    for item in data.PROGRAMS:
        if item.name == name:
            return item
def getPort(num):
    for item in data.PORTS:
        if item.num == num:
            return item
class PlayerNode(Node):
    def __init__(self, name, password):
        super().__init__("Local Host","localhost","127.0.0.1", users = [User(name, password, True)])
        self.address = "127.0.0.1"
        self.name = name
        self.password = password
        self.files = [Folder("home"),Folder("bin"),Folder("sys"),[File("system.ini")]]
        self.minPorts = 100
        self.ports = [getPort(7777),getPort(22)]
        self.creditCount = 500
        self.lvl = 0
        self.currentMission = None
        self.startActions()
    def main(self):
        while True:
            ch = input("{}@{} $".format(self.name, self.address))
            if ch in ["exit","quit"]:
                return
            elif ch == "":
                pass
            elif ch in ["clear","cls"]:
                cls()
            else:
                parts = ch.split(" ")
                if len(parts) == 1:
                    args = []
                else:
                    args = parts[1:]
                name = parts[0]
                program = getProgram(name)
                if program and program.unlocked:
                    if program.classPlease:
                        program.execute(args, self)
                    else:
                        program.execute(args)
                else:
                    print("FATAL ERROR: The program was not found.")
    def startActions(self):
        servers = [
            self,
            JmailServer(self),
            MailServer("reHack Mail Server","rehack-mail","rehack.mail",self,[User("welcome"),User("careers"),User("sales"),User("support"),User("contracts")],hideLookup=True),
            AnonMail(self),
            MailDotCom("XWebDesign Mail","xwebdesign.mail.com", self,[User("sales")]),
            MailDotCom("Mail Dot Com","root.mail.com", self, [User("sales")]),
            MailDotCom("Jmail Corporate Mail","jmail.mail.com",self,[User("sales")]),
            MailServer("WinFan3672 Personal Mail","mail3672","winfan3672.mail.com",self,[User("admin","somesecretpassword")]),
            MailServer("null.null","nullmail","null.null",self,[User("null")],minPorts=0),
            ]
        bodies = [
                [
                "Welcome to reHack!",
                "",
                "To get started, you'll want to connect to our intranet (intranet.rehack.org).",
                "You can do this using the 'connect' command.",
                "It will contain some useful resources as well as some info for beginners such as yourself.",
                "You will receive some marketing emails as well as this one, so be aware of that."
                ],
                [
                    "Hello.",
                    "",
                    "I work for AnonMail, a reHack sponsor.",
                    "AnonMail provides unlimited untraceable email addresses.",
                    "A rehack.org email address is a huge red flag, and a jmail.com email is easy to trace.",
                    "AnonMail is neither. We have over a million accounts, 99% of which are privacy-savvy users.",
                    "As such, your email blends right in.",
                    "You get a randomly generated username and get to receive up to 100,000 emails before your mailbox shuts down.",
                    "We also use port masking and hide our MX records, meaning script kiddies can't break in easily.",
                    "",
                    "To register, purchase the AnonMail client using the 'store' command for just 100 credits.",
                ],
                [
                    "Hello, fellow hacker.",
                    "",
                    "I would like to personally invite you to join our forum, 5chan.",
                    "In case you don't know, reHack and 5chan have a, let's just say, toxic relationship.",
                    "That is to say, reHack'ers target anons on 5chan all the time.",
                    "However, I feel that you might be different.",
                    "Because our website URL changes all the time, you'll need to check it out in the",
                    "WorldWide Web Directory: w3d.org.",
                    "",
                    "I hope to see you on 5chan, fellow anon.",
                ],
                [
                    "What is the price for having a mail server for the xwebdesign subdomain?",
                    "We aim to have 25 accounts and want full security.",
                ],
                [
                    "Dear {},",
                    "Thank you for purchasing mail.com.",
                    "See the invoice below:",
                    "",
                    "INVOICE",
                    "MAIL.COM SERVER <MONTHLY>: $79.99",
                    "INSTALLATION FEE <ONE-TIME>: $49.99",
                    "",
                    "Thank you for shopping with mail.com",
                ],
                [
                    "Dear Joe",
                    "See below the mail.com admin password:",
                    "",
                    "superuser",
                    "",
                    "I trust that jmail is secure enough that you won't somehow leak it.",
                    "It's only the web portal, but you are the webmaster, so it's only fair.",
                ],
                [
                    "Hello,",
                    "",
                    "This is a message intended for easter egg hunters.",
                    "Thank you for enjoying my game.",
                    "I put a lot of effort into creating a lot of complex systems (such as mail servers)",
                    "and I'm really proud of my work.",
                    "All I can leave you with is a hint for some gameplay:",
                    "",
                    "There's a hidden ISP database that offers some pretty powerful functionality.",
                    "It allows you to reassign any IP address, including your own, so that any traces you leave behind are gone.",
                    "",
                    "Connect to it: 1.1.1.1",
                    "Before you do that, the admin password is potholes. Use the login command to take advantage of that.",
                    "",
                    "Signed,",
                    "WinFan3672",
                    "Creator of reHack",
                ],
                [
                    "This email server is reserved by W3D for the use of spoofing the FROM field of an email.",
                    "Set the FROM field to null@null.null and SMTP will do the rest.",
                    "The email server actively ignores any emails sent to it.",
                    "If you send an email, it will be sent back to you and not stored.",
                ],
                [
                    "The email you provided was sent to null@null.null.",
                    "This is usually because you are replying to an email which had its FROM address spoofed.",
                    "For security purposes, your email has been sent back to you:",
                    "FROM: {}",
                    "TO: null@null.null",
                    "SUBJECT: {}",
                    "",
                    "{}",
                ],
            ]
        bodies = ["\n".join(x) for x in bodies]
        emails = [
            Email("welcome@rehack.mail","{}@jmail.com".format(self.name),"Welcome to reHack",bodies[0]),
            # Email("marketing@anon.mail",f"{self.name}@jmail.com","AD: Try AnonMail",bodies[1]),
            # Email("null@null",f"{self.name}@jmail.com","A Personal Invitation",bodies[2])
            Email("xwebdesign@jmail.com","sales@root.mail.com","Client: XWebDesign",bodies[3]),
            Email("sales@root.mail.com","sales@xwebdesign.mail.com","Invoice",bodies[4].format("XWebDesign")),
            Email("sales@root.mail.com","sales@jmail.mail.com","Invoice",bodies[4].format("JMail")),
            Email("null@null.null","admin@winfan3672.mail.com","A Message",bodies[6]),
            Email("null@null.null","null@null.null","Notice",bodies[7]),
            
            ]
        mission_bodies = [
            [
                "Hello and welcome to reHack.",
                "I hope that you've been getting used to your Node.",
                "This is your first mission, out of many.",
                "This one's simple. You need to connect to the reHack Test Server.",
                "The IP address is: test.rehack.org.",
                "If this works, you'll be denied access.",
                "",
                "Once you've connected once, you can run the 'mission' command.",
                "This command simply completes your mission. Simple, right?",
                "We'll find out.",
            ],
            [
                "OK. You did it. Now for the next bit.",
                "You need to run the nmap command on it.",
                "Run the following command:",
                "",
                "nmap test.rehack.org",
                "",
                "This will reveal the exposed ports on the node as well as how many you need to open.",
                "I'll be waiting.",
            ],
            [
                "You ran the nmap command, great. The output should have looked something like this:"
                "",
                "--------------------",
                "Found Target",
                "Hostname: reHack Test Server",
                "Min. Ports To Crack: 0",
                "--------------------",
                "[CLOSED] PORT 21: FTP",
                "[CLOSED] PORT 22: SSH",
                "--------------------",
                "",
                "As you can see, there are 2 closed ports: 21 and 22.",
                "The important part is the 'Min. Ports To Crack' section.",
                "It shows how many you need to open to hack the device.",
                "This node has weak security, so it can be hacked instantly.",
                "Let's do it!",
                "",
                "Use the porthack command on test.rehack.org.",
                "Once you're done, run 'mission' and read my next email."
            ],
            [
                "Good job.",
                "Now for a bit of an explanation.",
                "",
                "There are different types of nodes (devices connected to the Internet).",
                "As such, some of them do different things, and have different levels of security.",
                "When you connect to a node as a normal user, it can do one thing, such as display a webpage, or just deny access.",
                "When you hack in, it performs a different function, such as opening an admin panel or allowing you to run commands on it.",
                "",
                "With multiple types of security comes multiple ways to break it. For instance, you may one day stumble on a node's admin password.",
                "If this happens, you can run the following command:",
                "",
                "login <IP address> <password>",
                "",
                "This will break into the system in the same way porthack does, but without you forcing your way in.",
                "",
                "Try it. The admin password for one of our throwaway test servers is 'trollface'.",
                "The IP address is {}.",
            ],
            [
                "You're doing well. Now for a REAL test.",
                "A forum called ColonSlash has been spreading lies about us.",
                "We as a collective are not pleased.",
                "I would like you to break in.",
                "If you run nmap, you'll notice that ports 21 and 22 are exposed.",
                "There are 2 built-in programs that expose those ports.",
                "To expose port 21, you use ftpkill.",
                "To expose port 22, you use sshkill.",
                "",
                "Break into colonsla.sh and run 'mission' once you are done.",
            ],
            ]
        mission_bodies = ["\n".join(x) for x in mission_bodies]
        missionEmails = [
            Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 1",mission_bodies[0]),
            Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 2",mission_bodies[1]),
            Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 3",mission_bodies[2]),
            Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 4",mission_bodies[3].format(data.getNode("test2").address)),
            Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 5",mission_bodies[4]),
            ]
        self.MISSIONS = [
            ConnectMission(self, "start1","Start (Pt. 1)","test.rehack.org",missionEmails[0],reward=500,next_id = "start2"),
            NMapMission(self, "start2","Start (Pt. 2)","test.rehack.org",missionEmails[1],reward=500,next_id="start3"),
            Mission(self, "start3","Start (Pt. 3)","test.rehack.org",missionEmails[2],reward=500,next_id="start4"),
            Mission(self, "start4","Start (Pt. 4)","test2",missionEmails[3],reward=500,next_id="start5"),
            Mission(self, "start5","Start (Pt. 5)","colonsla.sh",missionEmails[4],reward=500,next_id="start6"),
            ]
        for item in servers:
            data.NODES.append(item)
        for item in emails:
            sendEmail(item)
        data.getNode("null.null").accounts[0].autoresponse = Email("null@null.null","","Your email could not be sent",bodies[8])
        self.currentMission = data.getMission("start1",self)
        self.currentMission.start()