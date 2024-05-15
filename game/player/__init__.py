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
    ProgramInstaller,
)

import data

import sys
import missions
import time
import os
import pickle
import configparser
import hashlib
import traceback
import getpass
import json

import nodes



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
            "Local Host", "localhost", "127.0.0.1", users=[User(name, password, True), User("admin")]
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
        self.currentMission = None
        self.startActions()
        self.bankAccounts = []
        self.notes = []
        self.date = GameDate()
        self.timeSinceNextDay = time.time() + 300 ## Starts 50% through = midday
        self.saveName = hashlib.sha256(str(random.randint(1, 2^64) * time.time()).encode()).hexdigest()
        self.trace = None
        self.actions = []
        self.secrets = {}
    def saveBase(self):
        default = {
            "name": self.name,
            "password": self.password,
            "date": str(self.date),
            "time": data.extrapolateTime(self.timeSinceNextDay),
            "credits": self.creditCount,
            "firewall": self.firewall.solution,
            "savefile": self.saveName,
            "saved": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mission": self.currentMission.mission_id if self.currentMission else "None",
        }
        save = configparser.ConfigParser()
        save["Player"] = default
        save["Programs"] = {x.name: x.unlocked for x in sorted(data.PROGRAMS)}
        save["Notes"] = {index: item.text for index, item in enumerate(self.notes)}
        save["Accounts"] = self.saved_accounts
        save["Node Addresses"] = {x.uid:x.address for x in data.NODES}
        save["Tor Node Addresses"] = {x.uid:x.address for x in data.TOR_NODES}
        save["Bank Accounts"] = {index: json.dumps({"ip": item.ip, "number": item.number, "pin": item.pin, "balance": item.balance}) for index, item in enumerate(self.bankAccounts)}
        save["Missions"] = {item.mission_id: item.complete for item in self.MISSIONS}

        return save
    def save(self):
        if not os.path.isdir("savegames"):
            os.mkdir("savegames")

        save = self.saveBase()

        with open("savegames/{}.rh_save".format(self.saveName),"w") as f:
            save.write(f)
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
                    exit()
                else:
                    print("Action cancelled.")
            elif ch == "":
                pass
            elif ch in ["clear", "cls"]:
                cls()
            else:
                self.run_command(ch)
            for node in data.NODES + data.TOR_NODES:
                node.tick()
    def run_command(self, command):
        parts = command.split(" ")
        if len(parts) == 1:
            args = []
        else:
            args = parts[1:]
        name = parts[0]
        program = getProgram(name)
        if program and program.unlocked:
            try:
                if program.classPlease:
                    program.execute(args, self)
                else:
                    program.execute(args)
            except:
                print(traceback.format_exc())
        else:
            print("FATAL ERROR: The program was not found.")
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
            MailDotCom("MHT Mail", "mht.mail.com", self),
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
                "Rejected Missions Repository", "rejected", "rejects.rehack.org",
            ),
            MissionServer(
                "reHack Contract Hub",
                "rehack_contracts",
                "contracts.rehack.org",
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
            MailServer("Debian Mail", "debianmail", "mail.debian.org", self, [User("admin")]),
            CriminalDatabase(),
            PlayerShodan(),
            ProgramInstaller("Tor Download Service", "tordl", "dl.tor.org", data.getProgram("tor", 1.0)),
            MailServer("SFEC Mail", "sfecmail", "sfec.mail", self, [User("admin"), User("xcombinator", "epilepsy"), User("dcse", "hydrogen")]),
            MailDotCom("DEC Solutions Mail", "dec.mail.com", self, [User("admin", "password123"), User("sales", "password123"), User("press", "password123"), User("roy", "fruition"), User("recruitment")]),
            MailDotCom("sms", "sms.mail.com", self, [User("sales", "morality")]),
            MailDotCom("Cinnamon", "cinnamon.mail.com", self, [User("john"), User("jane")], web_address="mail.com"),
        ] + nodes.main()
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
        ] + nodes.tor()
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
            [
                "Dear Mr Roy Andresson,",
                "Congratulations, your application to work for DEC Solutions as a Senior Programmer has been accepted.",
                "Because the work is remote, you will need to:",
                "",
                "1: Create an account using our Signup Service (private-signup.dec.com), creating an account and logging in.",
                "2: Connect to the LAN (the signup service will provide the IP address)",
                "3: Connect to ftp.local and find the file called 'ROY_TODO.TXT'. Read it and follow the instructions.",
                "",
                "We hope you find this work exciting.",
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
            Email("recruitment@dec.mail.com", "roy@dec.mail.com", "Congratulations", bodies[8]),
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
        irc = data.getNode("rhirc")
        irc.create_user(self.name, self.password)
    def checkCorporateTrace(self):
        uid, address = self.corporateTrace
        node = data.getAnyNode(uid)
        for log in node.logs:
            if log.address == address:
                self.gameOver()
        email = Email("admin@rehack.mail", "{}@jmail.com".format(self.name), "Good job!", "Looks like you made it. Be more careful next time.")
        print("WARNING: An email from reHack's admin reaches your inbox.")
        br()
    def gameOver(self):
        cls()
        time.sleep(5)
        div()
        print("Notice of Termination")
        div()
        print("We have been informed by your local government that they have caught you hacking into their systems.")
        print("As such, we have been forced to strike you off the active agents list and destroy your node.")
        print("You can create a new account, but you'll need to start from scratch.")
        print("Let this be a lesson to be more careful next time.")
        br()
        exit()
    def catchTrace(self):
        """
        Function called when an active trace reaches 0 seconds.
        """
        if self.trace.traceType == "Government":
            self.gameOver()
        elif self.trace.traceType == "Corporate":
            cls()
            div()
            print("You've been caught hacking into {}. Just tomorrow, the police will ask us to shut down your account.".format(data.getNode(self.trace.node).address))
            print("To prevent that from happening, you need to do one of the following:")
            div()
            print("* Delete the logs of the computer in question.")
            print("* Change your IP address. Check the reHack wiki for instructions on how to do that.")
            div()
            print("Once this is done, the passive trace will die anod you can live another day. If this happens, I'll email you.")
            div()
            print("NOTE FROM THE DEVS: One day in reHack is 10 minutes real world time.")
            br()
            cls()
            action = Action(self.date + 1, self.checkCorporateTrace)
            self.corporateTrace = (self.trace.node, str(self.address))
            self.actions.append(action)
            self.trace = None
class PlayerShodan(Node):
    def __init__(self):
        super().__init__("SHODAN #2", "shodan2", data.generateIP(), minPorts=65536)
        self.mhtForum = False
    def check_trace(self, player):
        node = data.getNode(player.trace.node)
        for log in node.logs:
            if node.address == player.address:
                return True
    def tick(self):
        player = data.getNode("localhost")
        mht = data.getNode("mht")
        ## Check if the trace is valid
        if player.trace:
            if not self.check_trace(player):
                player.trace = None
                print("SUCCESS: Active trace cleared.")
        if player.date == GameDate(2010, 7, 15) and not self.mhtForum:
            # print("MHT FORUM EVENT")
            self.mhtForum = True
            data.NODES.append(nodes.forum.mht)
            with open("msgboard/mht.com/forum") as f:
                forum = mht.add_story("MHT Is Opening A New Forum", "Admin", player.date.clone(), f.read())
                forum.reply("admin", "The forum is here: forum.mht.com, almost forgot!")

class Criminal(Base):
    def __init__(self, forename, surname, age, prison=None, crimes=None, status=None):
        self.forename = forename
        self.surname = surname
        self.age = age
        self.prison = prison
        self.crimes = crimes if crimes else []
        self.status = status
class CriminalDatabase(Node):
    def __init__(self, **kwargs):
        super().__init__("United States Federal Government Criminal Database", "uscrimdb", "db.crim.gov", ports=[data.getPort(21), data.getPort(22), data.getPort(80), data.getPort(1433)], minPorts=4, users=[User("admin", "admin")])
        self.criminals = [Criminal("John", "Smith", 44, "Alcatraz", ["Murder", "Arson", "Theft"])]
        # i = 0
        # while i < 40:
        #     person = random.choice(data.PEOPLE)
        #     name = "{} {}".format(person.forename, person.surname)
        #     if forename not in [x.forename for x in self.people]:
        #         self.add(name, random.randint(18, 45))
        #         i += 1
        self.create_file("New Intern Letter.txt", data.CRIMDB_LETTER, "home")
        self.create_user("root", "root")
        self.trace = Trace(self.uid, "Government", 35)
    def main(self, attemptCount=1):
        username = input("Username $")
        passwd = getpass.getpass("Password $")
        for user in self.users:
            if user.name == username and user.password == passwd:
                self.main_hacked()
                return
        print("ERROR: Invalid credentials.")
        if attemptCount < 3:
            self.main(attemptCount + 1)
        else:
            print("Too many bad password attempts. You have been disconnected from the server.")
    def main_hacked(self):
        while True:
            cls()
            div()
            print(self.name)
            div()
            print("[1] New Criminal")
            print("[2] Manage Criminal")
            print("[3] Delete Criminal")
            # if self.hacked:
            #     print("[4] Administration")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "0":
                return
            elif ch == "1":
                self.add_criminal()
            elif ch == "2":
                self.manage_criminal()
            elif ch == "3":
                self.remove_criminal()
    def choose_criminal(self):
        while True:
            cls()
            div()
            i = 1
            for person in self.criminals:
                print("[{}] {}, {} ({} Y.O)".format(i, person.surname, person.forename, person.age))
                i += 1
            div()
            try:
                ch = int(input("$"))
                if ch == 0:
                    return
            except:
                return
            return self.criminals[ch-1]
    def add_criminal(self):
        try:
            forename, surname = input("Forename $"), input("Surname $")
            age = int(input("Age (Years) $"))
        except:
            print("ERROR: Invalid input.")
            return
        prison = input("Prison Name (Optional) $")
        status = self.select_status()
        self.criminals.append(Criminal(forename, surname, age, prison if prison else None, status=status))
        self.message("Successfully added criminal.")
    def manage_criminal(self):
        crim = self.choose_criminal()
        if crim:
            self.manage(crim)
    def select_status(self):
        while True:
            cls()
            div()
            print("Select Prisoner Status")
            div()
            i = 1
            for status in data.PRISON_STATUS:
                print("[{}] {}".format(i, status))
                i += 1
            div()
            try:
                ch = int(input("$"))
            except:
                ch = 0
            if 0 <= ch -1 < len(data.PRISON_STATUS):
                return data.PRISON_STATUS[ch-1]
    def message(self, message):
        cls()
        div()
        print(message)
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
    def manage(self, crim):
        while True:
            cls()
            div()
            print("Name: {}, {}".format(crim.surname, crim.forename))
            print("Age: {}".format(crim.age))
            print("Status: {}".format(crim.status))
            print("Prison: {}".format(crim.prison))
            print("Crimes: {}".format("; ".join(crim.crimes) if crim.crimes else "None"))
            div()
            print("[1] Add Crime")
            print("[2] Remove Crime")
            print("[3] Transfer/Remove Prison")
            print("[0] Exit")
            div()
            ch = input("$")
            if ch == "0":
                return
            elif ch == "1":
                cls()
                crime = input("Crime $")
                if crime:
                    crim.crimes.append(crime)
                    self.message("Successfully added crime '{}'.".format(crime))
                else:
                    self.message("Canceled action.")
            elif ch == "2":
                self.message("This functionality is disabled for maintenance.")
            elif ch == "3":
                cls()
                prison = input("Prison name (leave blank for no prison) $")
                crim.prison = prison if prison else None
    def remove_criminal(self):
        crim = self.choose_criminal()
        if crim:
            if self.confirm():
                self.criminals.remove(crim)
                self.message("Successfully removed criminal.")
            else:
                self.message("Canceled action.")

