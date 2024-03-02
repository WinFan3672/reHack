from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
from game.programs import (
    JmailServer,
    MailAccount,
    EmailData,
    Email,
    sendEmail,
    MailServer,
    TorMailServer,
    AnonMail,
    MailDotCom,
    MissionServer,
    pickSelection,
    Firewall,
    MasterVPS,
    BlankMission,
    Mission,
    NodeTracker,
    SignupService,
    TorSignupService,
)

import data
import sys
import missions
import time
import os
import pickle
import hashlib

import nodes
import nodes.lan
import nodes.forum
import nodes.test



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
        super().__init__(
            "Local Host", "localhost", "127.0.0.1", users=[User(name, password, True)]
        )
        self.address = "127.0.0.1"
        self.name = name
        self.password = password
        self.files = [
            Folder("home"),
            Folder("bin"),
            Folder("sys"),
            [File("system.ini")],
        ]
        self.minPorts = 2**16
        self.ports = [getPort(7777), getPort(22)]
        self.creditCount = 500
        self.firewall = Firewall(makeRandomString())
        self.saved_accounts = {
            f"{self.name}@jmail.com": self.password,
        }
        self.saved_tor_accounts = {}
        self.currentMission = None
        self.startActions()
        self.bankAccounts = []
        self.notes = []
        self.date = GameDate()
        self.timeSinceNextDay = time.time() + 300 ## Starts 50% through = midday
        self.saveName = hashlib.sha256(str(random.randint(1, 2^64)).encode()).hexdigest()
    def saveBase(self):
        return {
                "date": str(self.date),
                "time": data.extrapolateTime(self.timeSinceNextDay),
                "name": self.name,
                "password": self.password,
                "creditCount": self.creditCount,
                "notes": [x.text for x in self.notes],
                "bankAccounts": self.bankAccounts,
                "programs": [x.name for x in data.PROGRAMS if x.unlocked]
        }
    def save(self):
        ## ensure directory
        if not os.path.isdir("savegames"):
            os.mkdir("savegames")
        ## get file name
        fn = input("Save file name $")
        ## pickle data
        with open("savegames/{}.pkl".format(fn),"wb") as f:
            pickle.dump(self,f)
        print("Successfully saved game.")
    def load(self):
        if os.path.isdir("savegames"):
            fn = input("Save file name $")
            if os.path.isfile("savegames/{}.pkl".format(fn)):
                with open("savegames/{}.pkl".format(fn),"rb") as f:
                    self = pickle.load(f)
                    print("Loaded game successfully.")
            else:
                print("ERROR: Invalid save file name")
        else:
            print("ERROR: No saved files.")
    def main(self):
        while True:
            ch = input("{}@{} $".format(self.name, self.address))
            if ch in ["exit", "quit"]:
                if input("Retype command to confirm $") == ch:
                    return
                else:
                    print("Action cancelled.")
            elif ch == "":
                pass
            elif ch in ["clear", "cls"]:
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
            for node in data.NODES + data.TOR_NODES:
                node.tick()
    def check_health(self):
        return True
    def startActions(self):
        servers = [
            JmailServer(self),
            MailServer(
                "reHack Mail Server",
                "rehack-mail",
                "rehack.mail",
                [
                    User("welcome"),
                    User("careers"),
                    User("sales"),
                    User("support"),
                    User("contracts"),
                    User("domains"),
                ],
                hideLookup=True,
            ),
            AnonMail(self),
            MailDotCom("XWebDesign Mail", "xwebdesign.mail.com", self, [User("sales")]),
            MailDotCom(
                "Mail Dot Com",
                "root.mail.com",
                self,
                [User("sales"), User("beryl", "anderson")],
            ),
            MailDotCom("Jmail Corporate Mail", "jmail.mail.com", self, [User("sales")]),
            MailDotCom(
                "5chan Corporate Mail", "5chan.mail.com", self, [User("invites")]
            ),
            MailDotCom(
                "W3D Corporate Mail", "w3d.mail.com", self, [User("support", "letmein")]
            ),
            MailServer(
                "null.null", "nullmail", "null.null", self, [User("null")], minPorts=0
            ),
            MissionServer(
                "Rejected Missions Repository", "rejected", "rejects.rehack.org", self
            ),
            MissionServer(
                "reHack Contract Hub",
                "rehack_contracts",
                "contracts.rehack.org",
                self,
                missions.main_story_missions(self),
            ),
            MailServer(
                "Coca Official Mail",
                "cocamail",
                "coca.mail",
                self,
                [
                    User("admin", "platform"),
                    User("humanresources", "vinvin"),
                    User("sysadmin", "weakness"),
                ],
            ),
            MasterVPS(self),
            MailDotCom("Mountain Mail","mview.mail.com",self,[User("admin","redhat"),User("sales"),User("accounting"),User("customer-support"),User("james.rally","monica"),User("hr"),User("monica.flange")]),
            MailServer(
                "CIA Mail",
                "ciamail",
                "cia.mail.gov",
                self,
                [
                    User("admin","sympathy"),
                    User("police-relations"),
                    User("defense-response"),
                    User("public-relations"),
                    # User("webmaster","spider"),
                ],
                hideLookup = True,
            ),
            MailServer(
                "Mail Dot Gov",
                "usagovmail",
                "mail.gov",
                self,
                [
                    User("admin","sympathy"),
                    User("back.oboma"),
                    User("linkbot"),
                ],
                hideLookup=True,
            ),
            MailServer("EnWired Mail", "enwired-mail", "enwired.mail", self, [User("elliot"), User("jacob"), User("sales")]),
            nodes.lan.cialan,
            nodes.test.lan,
            nodes.test.forum,
            nodes.mht,
            nodes.rhwiki,
            nodes.openstat,
            nodes.test.git,
            MailDotCom("Deployment Test Cinnamon", "cinnamon.mail.com", self, [User("cinnamon")]),
            MailServer("Debian Mail", "debianmail", "mail.debian.org", self, [User("admin")]),
        ]
        onionsites = [
            TorMailServer(
                "Euclid",
                "euclid",
                "euclid.onion",
                self,
                [],
            ),
            TorMailServer(
                "ReHack Onionmail",
                "rhomail",
                "rehackmail.onion",
                self,
                []
            ),
            nodes.forum.chan,
            nodes.forum.vcforum,
        ]
        bodies = [
            [
                "Dear NOAH BAILEY,",
                "",
                "If you are reading this message, you have been dismissed from your position as SYSTEM ADMINISTRATOR and are required to vacate the property",
                "within 90 minutes of this message being sent.",
                "You will be given 6 months' salary ($125,000) as a severance package.",
                "",
                "We understand that this may be difficult to hear, especially given your long-term employment at Mountain View.",
                "However, given your quote, INABILITY TO COMPLY WITH INSTRUCTIONS AND A REFUSAL TO BE FLEXIBLE, unquote, we firmly believe that the dismissal has been justified.",
                "When you signed your employment contract, you waived:",
                "",
                "* The right to a class-action lawsuit over unfair dismissal",
                "* The right to a class-action lawsuit over unpaid severance or other benefits",
                "* The right to a class-action lawsuit over workplace health and safety concerns",
                "",
                "Thank you for working for Mountain View, LLC.",
            ],
            [
                "Dear MONICA FLANGE,",
                "",
                "If you are reading this message, you have been dismissed from your position as OFFICE WORKER and are required to vacate the property",
                "within 90 minutes of this message being sent.",
                "You will be given 6 months' salary ($15,000) as a severance package.",
                "",
                "We understand that this may be difficult to hear, especially given your long-term employment at Mountain View.",
                "However, given your quote, ATTEMPTED CORPORATE ESPIONAGE IN THE FORM OF SENDING AN ADMIN PASSWORD OVER AN UNENCRYPTED NETWORK (JMAIL), unquote, we firmly believe that the dismissal has been justified.",
                "When you signed your employment contract, you waived:",
                "",
                "* The right to a class-action lawsuit over unfair dismissal",
                "* The right to a class-action lawsuit over unpaid severance or other benefits",
                "* The right to a class-action lawsuit over workplace health and safety concerns",
                "",
                "Thank you for working for Mountain View, LLC.",
            ],
            [
                "NOTE TO SELF: The IP for the notes server is {}"
            ],
            [
                "Hello,",
                "This is an official email approving the launch of Project Autocrat.",
                "Please inform relevant departments immediately.",
            ],
            [
                "Dear admin,",
                "One of our employers, Monica Flange (monicaf332@jmail.com) has performed corporate espionage on your network.",
                "We would like to request that you delete ALL emails Monica has sent from your network, or we will sue for mishandling of corporate data.",
                "Signed,",
                "Administrator of Mountain View Private Mail.",
            ],
            [
                    "Dear Administrator,",
                    "We have complied with your request. All user data has been purged. In fact, because we take user data seriously, our servers run on arrays of small, 256mb hard drives which contain the user data for one user at a time. As such, we simply removed the hard-drive for the user 'monicaf332@jmail.com' and placed it into an ISO/IEC 27001 compliant de-gaussing and shredding process.",
                    "We thank you for being a JMail customer.",
            ],
            [
                "Note to self: the password is roses.are.red.violets.are.blue",
            ],
            [
                "Hello and welcome to reHack.",
                "Before you do ANYTHING, you should read these rules.",
                "",
                "1: Don't Be Stupid",
                "1.1: We know your name, IP address, etc. If you cross us, you'll regret it.",
                "1.2: We don't tolerate idiocy.",
                "1.3: Don't waste our time.",
                "",
                "2: Be Moral",
                "2.1: We NEVER hack medical organisations. While what we do is morally reprehensible to some,",
                "       hacking organisations that tend to the dying is not acceptable.",
                "2.2: We NEVER hack for political reasons. That doesn't mean we can't be political, but we should not engage in hacking",
                "       for the sake of politics.",
                "2.3: Never do the low-life criminal thing of taking money and not doing what is asked of you.",
                "       We may be criminals, but we're a better class of criminal than that.",
                "",
                "3: Criminal Code of Honour",
                "3.1: NEVER divulge information about another reHack agent to law enforcement.",
                "3.2: NEVER hold grudges yourself. Only allow others to let you act on theirs.",
                "3.3: In Rule 1.1, we suggest consequences for crossing us. These consequences will not break Rule 3.",
                "",
                "4: Only Hack Necessary Targets",
                "4.1: Don't go out of your way to hack people unrelated to your mission.",
                "",
                "By using reHack, you agree to this Code of Conduct.",
                "If you disagree with these rules, simply disconnect from your node and never connect again.",
                "Hopefully, you won't find any of our agents (or your rivals) targeting you in real life.",
                "",
                "Signed,",
                "[DATA EXPUNGED],",
                "reHack Corporation Administrator.",
            ],
            ]
        bodies = ["\n".join(x) for x in bodies]
        emails = [
            Email("admin@rehack.mail", "{}@jmail.com".format(self.name), "reHack Code of Conduct (COC)", bodies[7]),
            Email(
                "admin@coca.mail",
                "admin@coca.mail",
                "Mainframe Password",
                "The password is 'anticyclogenesis'.\nCorporate don't want us sharing this, so I'm keeping it safe here.",
            ),
            Email(
                "jennifer@coca.mail",
                "admin@coca.mail",
                "Reset Password",
                "Please reset my network password",
            ),
            Email(
                "admin@coca.mail",
                "jennifer@coca.mail",
                "RE: Reset Password",
                "I cannot do that as I am not the sysadmin. Contact your line manager if you need assistance.",
            ),
            Email(
                "admin@coca.mail",
                "sysadmin@coca.mail",
                "FW: Reset Password",
                "I am forwarding a suspected phishing attempt from a potential external body. Please investigate.",
            ),
            Email(
                "mirror-daemon@coca.mail",
                "admin@coca.mail",
                "FW: Reset Password",
                "The following email to sysadmin@coca.mail has been received:\n\nI am forwarding a suspected phishing attempt from a potential external body. Please investigate.",
            ),
            Email(
                "sysadmin@coca.mail",
                "admin@coca.mail",
                "RE: FW: Reset Password",
                "Thank you for bringing this to my attention.\nThis will be investigated soon.",
            ),
            Email(
                "james.rally@mview.mail.com",
                "admin@mview.mail.com",
                "Password Request",
                "Please reply to this email with the admin password for the mainframe or you lose your fucking job.",
                ),
            Email(
                "admin@mview.mail.com",
                "james.rally@mview.mail.com",
                "RE: Password Request",
                "For security reasons, I cannot comply with this request.",
                ),
            Email(
                "james.rally@mview.mail.com",
                "hr@mview.mail.com",
                "Request For Dismissal",
                "EMPLOYEE: Noah Bailey\nEMAIL ADDR: admin@mview.mail.com\nREASON: Inability to comply with instructions and a refusal to be flexible",
                ),
            Email(
                "hr@mview.mail.com",
                "admin@mview.mail.com",
                "Notice of Dismissal",
                bodies[0],
                ),
            Email(
                "james.rally@mview.mail.com",
                "james.rally@mview.mail.com",
                "Note To Self",
                bodies[2].format(data.getNode("mountainnotes").address),
                ),
            Email(
                "monicaf332@jmail.com",
                "amdin@mview.mail.com",
                "Mainframe Password",
                "It's backdrop2252 by the way",
                ),
            Email(
                "hr@mview.mail.com",
                "monica.flange@mview.mail.com",
                "Notice of Dismissal",
                bodies[1],
                ),
            Email(
                "back.oboma@mail.gov",
                "admin@cia.mail.gov",
                "IMPORTANT: *****************",
                bodies[3],
                ),
            Email("admin@mview.mail.com", "admin@jmail.com", "IMPORTANT: Data Destruction Request", bodies[4]),
            Email("admin@jmail.com", "admin@mview.mail.com", "RE: IMPORTANT: Data Destruction Request", bodies[5]),
            Email("admin@cia.mail.gov", "admin@cia.mail.gov", "Autocrat Mainframe Password (DO NOT LOSE!)", bodies[6]),
        ]
        for item in servers:
            data.NODES.append(item)
        for i in onionsites:
            data.TOR_NODES.append(i)
        for email in emails:
            sendEmail(email)
        self.MISSIONS = missions.main(self)
        self.currentMission = data.getMission("start1", self)
        self.currentMission.start()
        data.NODES = [x for x in data.NODES if x]
        data.NODES = [self] + data.NODES

        data.addFirewall("firewalltest", Firewall("smartheap11", 0.125))

class PlayerShodan(Node):
    def __init__(self):
        super().__init__("SHODAN #2", "shodan2", data.generateIP(), minPorts=65536)
    def tick(self):
        player = data.getNode("localhost")
