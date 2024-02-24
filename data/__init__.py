from resource.classes import *
from game import programs
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random
import json
import copy
import string

global PORTS, NODES, TOR_NODES, PROGRAMS, GENERATED


def div():
    print("--------------------")


def br():
    div()
    input("Press ENTER to continue.")

GENERATED = []

def getMission(mission_id, player):
    for mission in player.MISSIONS:
        if mission_id == mission.mission_id:
            return mission


def checkEmailAddress(address):
    ## Function that returns a boolean value depending on if an email address exists.
    if not "@" in address:
        ## User entered something wrong
        return False
    parts = address.split("*")
    if len(parts) != 2:
        ## User added more than one '@'
        return False
    username = parts[0]
    domain = parts[1]

    node = getNode(domain)
    if not node:
        ## Invalid mailserver
        return False

    users = [x.username for x in node.users]

    if username in users:
        return True
    else:
        return False

def getNode(uid):
    for item in NODES:
        if uid == item.uid or uid == item.address:
            return item

def getTorNode(uid):
    for item in TOR_NODES:
        if uid == item.uid or uid == item.address:
            return item

def addFirewall(node, firewall):
    if not isinstance(node, Node):
        node = getNode(node)
    node.firewall = firewall

def genString(genLength):

    s = ""
    for x in range(genLength):
        s += random.choice(list(string.hexdigits))
    return s

def generateTorURL(prefix=""):
    '''
    Generates a Tor URL from an optional prefix in the format:
    $ <prefix><random hex digits>.onion
    The URL is guaranteed to be 64 characters long.
    '''
    if type(prefix) != str:
        raise TypeError("Prefix must be a string.")
    if len(prefix) > 64:
        raise TypeError("Prefix cannot be > 64 characters long.")
    genLength = 64 - len(prefix)
    return prefix + genString(genLength) + ".onion"

def generateIP():
    c = []
    for i in range(4):
        c.append(random.randint(0, 255))
    ip = ".".join([str(x) for x in c])
    if ip in [x.address for x in NODES]:
        return generateIP() ## prevents duplicate IP addresses.
    GENERATED.append(ip)
    return ip


def getPort(num, isOpen=False):
    for item in PORTS:
        if item.num == num:
            item.open = isOpen
            return copy.deepcopy(item)


def createNodeLink(uid, link_uid):
    if getNode(link_uid):
        raise Exception("Cannot link when a node exists in its place")
    else:
        ## Grab using getNode(uid), remove the link to the uid and address
        ## then generate a new IP and put link_uid in its place
        raise Exception("Not yet implemented")

BLOCKLIST = [
    "admin",
]
PORTS = [
    Port(1, "Local Area Network Router"),
    Port(21, "FTP"),
    Port(22, "SSH"),
    Port(23, "Telnet"),
    Port(25, "Mail Server"),
    Port(80, "Web Server"),
    Port(123, "NTP Time Server"),
    Port(1194, "VPN Server"),
    Port(1433, "SQL Database"),
    Port(6881, "BitTorrent Tracker"),
    Port(7777, "reHackOS Node"),
    Port(9200, "Tor Node"),
    Port(24525, "Message Board"),
    Port(65536, "DNS Server"),
]
testSrvFiles = [
    Folder(
        "home",
        [
            Folder("stash", [File("hello.txt", "hello")]),
            File("test.txt", "open sesame"),
        ],
    ),
]
XOS_DEVICES = {
    "xphone": {
        "name": "xPhone",
        "cpu": "1 GHz",
        "ram": "500 MB",
        "storage": "8 GB",
        "battery": "500 mAh",
    },
    "xphone2": {
        "name": "xPhone 2",
        "cpu": "1.33 GHz",
        "ram": "1000 MB",
        "storage": "16 GB",
        "battery": "1000 mAh",
    },
    "xphone3": {
        "name": "xPhone 3",
        "cpu": "2.7 GHz",
        "ram": "2000 MB",
        "storage": "64 GB",
        "battery": "3000 mAh",
    },
    "xpad": {
        "name": "xPad",
        "cpu": "1.5 GHz",
        "ram": "750 MB",
        "storage": "16 GB",
        "battery": "2500 mAh",
    },
    "xpad2": {
        "name": "xPad 2",
        "cpu": "2.5 GHz",
        "ram": "1450 MB",
        "storage": "64 GB",
        "battery": "4000 mAh",
    },
    "xpad3": {
        "name": "xPad 3",
        "cpu": "3.5 GHz",
        "ram": "2500 MB",
        "storage": "256 GB",
        "battery": "5000 mAh",
    },
}
NODES = []
jgreyfiles = [
    Folder(
        "Notes",
        [
            File("mail login is admin:platform"),
        ],
    )
]

NODES.append(programs.BankBackEnd("Bank of reHack :: Back-End Server", "rehackbankbe", generateIP()))


N = [
    programs.ISPNode(),
    Node("SHODAN", "shodan", generateIP(), ports=[getPort(80)], minPorts=1),
    Node(
        "reHack Test Server",
        "rehacktest",
        "test.rehack.org",
        ports=[getPort(21), getPort(22)],
        files=testSrvFiles,
    ),
    programs.MessageBoard(
        "reHack News", "rehack.news", "rehacknews", "rehack.news", minPorts=4
    ),
    programs.MessageBoard(
        "reHack News",
        "news.rehack.org",
        "newsrehack_pri",
        "news.rehack.org",
        minPorts=4,
    ),
    programs.WebServer("United States Government", "usagov", "usa.gov", "usa.gov"),
    programs.WebServer(
        "reHack Official", "rehack", "rehack.org", "rehack.org", minPorts=4
    ),
    programs.WebServer(
        "reHack Intranet",
        "rehack_intranet",
        "intranet.rehack.org",
        "intranet.rehack.org",
        minPorts=4,
    ),
    programs.WebServer(
        "World Wide Web Directory", "w3d", "w3d.org", "w3d.org", minPorts=4
    ),
    programs.WebServer(
        "reHack Directory",
        "rehack_dir",
        "directory.rehack.org",
        "directory.rehack.org",
        minPorts=4,
    ),
    programs.WebServer(
        "reHack pwnlist", "pwned.reha.ck", "pwned.reha.ck", "pwned.reha.ck", minPorts=4
    ),
    programs.WebServer("UK Government", "gov.uk", "gov.uk", "gov.uk"),
    programs.WebServer("FFC Corporate Home", "ffc.com", "ffc.com", "ffc.com"),
    programs.WebServer(
        "XWebDesign Home", "xwebdesign.com", "xwebdesign.com", "xwebdesign.com"
    ),
    programs.WebServer(
        "Mail.com",
        "mail.com",
        "mail.com",
        "mail.com",
        users=[User("admin", "superuser")],
        linked=[
            "root.mail.com",
            "xwebdesign.mail.com",
            "jmail.mail.com",
            "winfan3672.mail.com",
            "mailcomdocs",
        ],
    ),
    programs.WebServer(
        "AnonMail Home", "www.anon.mail", "www.anon.mail", "www.anon.mail"
    ),
    programs.XOSDevice(
        "WinFan3672's xPhone",
        "3672_xphone",
        generateIP(),
        notes=[programs.Note("This is a test")],
        accounts=[
            programs.XOSMailAccount("admin@winfan3672.mail.com", "supersecretpassword")
        ],
        model="xphone3",
    ),
    programs.WikiServer(
        "rehack Wiki", "rehack_wiki", "wiki.rehack.org", "wiki.rehack.org"
    ),
    Node(
        "reHack Test Server #2",
        "test2",
        generateIP(),
        ports=[],
        minPorts=2,
        users=[User("admin", "trollface")],
    ),
    programs.MessageBoard(
        "ColonSlash",
        "colonsla.sh",
        "colonslash",
        "colonsla.sh",
        minPorts=2,
        ports=[getPort(22), getPort(21)],
    ),
    programs.WebServer("Test Hub", "testhub", "test.hub", "test.hub", minPorts=3),
    programs.WebServer(
        "Coca Homepage",
        "cocaweb",
        "coca.com",
        "coca.com",
        linked=["cocamain", "cocamail", "johngrey"],
    ),
    Node(
        "Coca Mainframe",
        "cocamain",
        generateIP(),
        [getPort(21), getPort(22), getPort(7777)],
        minPorts=65536,
        users=[User("admin", "anticyclogenesis")],
    ),
    Node(
        "John Grey's PC",
        "johngrey",
        generateIP(),
        ports=[getPort(21), getPort(22), getPort(6881)],
        files=jgreyfiles,
        linked=["cocamail"],
    ),
    programs.WebServer(
        "Nanosoft Home",
        "nanosoftweb",
        "nanosoft.com",
        "nanosoft.com",
        users=[User("admin", "lavender")],
    ),
    Node(
        "Beryl Anderson's PC",
        "berylandserson",
        generateIP(),
        ports=[getPort(21), getPort(22), getPort(6881)],
        linked=["berylanderson_phone"],
    ),
    programs.XOSDevice(
        "Beryl Anderson's xPhone",
        "berylanderson_phone",
        generateIP(),
        accounts=[
            programs.XOSMailAccount("beryl@root.mail.com", "anderson"),
        ],
    ),
    programs.MessageBoard(
        "Mail.com Documentation",
        generateIP(),
        "mailcomdocs",
        "mail.com",
        linked=["mail.com", "mailcommain", "berylandserson"],
        ports=[getPort(80), getPort(1433), getPort(24525)],
        minPorts=2,
        users=[User("admin", "composer")],
    ),
    Node(
        "Mail.com Mainframe",
        "mailcommain",
        generateIP(),
        users=[User("admin", "fuckinganonmailfuckingjmail")],
    ),
    Node(
        "reHack Tests: Bruter",
        "brutertest",
        "bruter.rehack.test",
        users=[User("admin", "overcoat")],
        minPorts=2**16,
    ),
    Node(
        "reHack Tests: Firewall",
        "firewalltest",
        "firewall.rehack.test",
        users=[User("admin")],
        minPorts=0,
    ),
    programs.WebServer(
        "MasterVPS Homepage", "mastervps_web", "mastervps.me", "mastervps.me"
    ),
    programs.WebServer("Mountain View", "mountainweb", "mountain.view", "mountain.view",linked=["mountainmain","mountainmail","moutainremote"]),
    programs.WebServer("DomainExpert Home", "dexpertweb", "domain.expert", "domain.expert"),
    Node("Mountain View Mainframe","mountainmain", generateIP(), ports=[],minPorts=2**16,users=[User("admin","backdrop2252")]),
    Node("Mountain View Remote Work Hub","moutainremote",generateIP(),ports=[getPort(22),getPort(21)],minPorts=2, linked =["jrallypc","nbaileypc","mflange"]),
    programs.XOSDevice("James Rally's xPhone","jrallyphone",generateIP(),accounts=[programs.XOSMailAccount("james.rally@mview.mail.com","monica")]),
    programs.XOSDevice("Noah Bailey's xPhone","nbaileyphone",generateIP(),notes=[programs.Note("Get back at James Rally, I know he fired me.")],accounts=[programs.XOSMailAccount("admin@mview.mail.com","redhat")]),
    programs.XOSDevice("Monica Flange's xPhone","mflangephone",generateIP(),notes=[programs.Note("I know James Rally likes me. Fucking creep.")],accounts=[programs.XOSMailAccount("monicaf332@jmail.com","monica.flange")]),
    Node("James Rally's PC","jrallypc",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["jrallyphone"]),
    Node("Noah Bailey's PC","nbaileypc",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["nbaileyphone"]),
    Node("Monica Flange's PC","mflange",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["mflangephone"]),
    programs.MessageBoard("Mountain View Message Board",generateIP(),"mountainnotes","mview"),
    programs.MessageBoard("MHT Web","mht.com","mhtweb","mht.com"),
    programs.MessageBoard("AnonMail Blog","blog.anon.mail","anonmail_blog","blog.anon.mail"),
    programs.GlobalDNS(),
    programs.VersionControl("Version Control Test","vctest","vc.rehack.test",[Commit("Test commit")],[User("admin","alpine")]),
    programs.DomainExpert(),
    programs.WebServer("Central Intelligence Agency", "ciaweb", "cia.gov", "cia.gov",linked = ["ciamail", "ciaftp"]),
    Node("CIA File Transfer Protocol Server", "ciaftp", "ftp.cia.gov", ports=[getPort(21)], minPorts=1, linked=["cialan"]),
    programs.WebServer("The Onion Router :: Official Site", "torweb", "tor.org", "tor.org"),
    programs.MessageBoard("EnWired: Home", "enwired.com", "enwired-web", "enwired"),
    Node("Project Autocrat :: Mainframe", "autocratmain", generateIP(), ports=[], minPorts=65536, users=[User("admin", "roses.are.red.violets.are.blue")]),
    programs.WebServer("reHack Test Suite Home", "rehacktestmain", "rehack.test", "rehack.test"),
    Node("Blank Node Test", "blanktest", "blank.rehack.test"),
    programs.BankServer("Bank of reHack", "rhbank", "6.5.4.4", getNode("rehackbankbe").address, "socialism"),
    programs.SignupService("anonmail-signup", "signup.anon.mail", "anonmail", False),
]
for item in N:
    NODES.append(item)
PROGRAMS = [
    Program("help", programs.Help, True),
    Program("nmap", programs.nmap, True),
    Program("porthack", programs.porthack, True),
    programs.PortBreakingTool("ftpkill", 21, True).program,
    programs.PortBreakingTool("sshkill", 22, True).program,
    programs.PortBreakingTool("mailoverflow", 25, price=1500).program,
    programs.PortBreakingTool("webworm", 80, price=500).program,
    programs.PortBreakingTool("torrentpwn", 6881, price=750).program,
    programs.PortBreakingTool("sqldump", 1433, price=2500).program,
    programs.PortBreakingTool("lancrack", 1, price=3500).program,
    Program("connect", game.programs.connect.main, True, classPlease=True),
    Program("debug", programs.debuginfo, True, price=0, classPlease=True),
    Program("mxlookup", programs.mxlookup, price=0),
    Program("jmail", programs.jmail, True, classPlease=True),
    Program("store", programs.store, True, classPlease=True),
    # Program("anonmail", programs.anonclient, price=250, classPlease=True),
    Program("login", programs.login, True),
    Program("mission", programs.mission_program, True, classPlease=True),
    Program("logview", programs.logview, price=0),
    Program("nodecheck", programs.nodecheck, price=0),
    Program("mailman", programs.mailman_base, True, classPlease=True),
    Program("bruter", programs.bruter, True, classPlease=True),
    Program("emailbruter", programs.emailbruter, True, classPlease=True),
    Program("firewall", programs.firewall, price=0),
    Program("tor", programs.tor, True, classPlease=True),
    # Program("sweep", programs.sweep, price=0),
    # Program("save",programs.save,True,classPlease=True),
    Program("lanconnect", programs.LANConnect, True, classPlease=True),
    Program("account", programs.accountList, True, classPlease=True),
]
SPICES = [
    "Basil",
    "Thyme",
    "Rosemary",
    "Sage",
    "Oregano",
    "Parsley",
    "Cilantro",
    "Dill",
    "Mint",
    "Chives",
    "Tarragon",
    "Bay leaf",
    "Marjoram",
    "Lemon balm",
    "Lavender",
    "Savory",
    "Coriander",
    "Lemongrass",
    "Fennel",
    "Wintergreen",
    "Lemon verbena",
    "Stevia",
    "Lovage",
    "Lemon thyme",
    "Saffron",
    "Cinnamon",
    "Cumin",
    "Paprika",
    "Nutmeg",
    "Cloves",
    "Cardamom",
    "Ginger",
    "Turmeric",
    "Chili powder",
    "Black pepper",
    "White pepper",
    "Cayenne pepper",
    "Mustard seed",
    "Allspice",
    "Fenugreek",
    "Anise seed",
    "Caraway",
    "Celery seed",
    "Poppy seed",
    "Sichuan peppercorn",
    "Juniper berries",
    "Vanilla bean",
    "Asafoetida",
    "Bay leaves",
    "Sumac",
    "Curry leaves",
    "Star anise",
    "Smoked paprika",
    "Himalayan Salt",
    "Herbes de Provence",
    "Italian seasoning",
    "Garam masala",
    "Chinese five spice",
    "Ras el hanout",
    "Cajun seasoning",
    "Old Bay seasoning",
    "Poultry seasoning",
    "Adobo seasoning",
    "Pumpkin spice",
    "Curry powder",
    "Za'atar",
    "Jerk seasoning",
    "Baharat",
    "Mexican chili powder",
]
WHOIS = {}
with open("data/passwords.txt") as f:
    PASSLIST = sorted(f.read().split("\n"))
    for item in PASSLIST:
        if "-" in item:
            PASSLIST.remove(item)
with open("data/password-wordlist.txt") as f:
    PASSLIST += sorted(f.read().split("\n"))

PASSLIST = sorted(PASSLIST)

random.shuffle(PASSLIST)

with open("data/names.json") as f:
    d = json.load(f)
temp_people = []
for i in range(500):
    temp_people.append(
        {"fore": random.choice(d["forenames"]), "sur": random.choice(d["surnames"])}
    )
with open("data/streetnames.json") as f:
    d = json.load(f)
nouns, adjectives = d["nouns"], d["adjectives"]
addresses = []
for i in range(500):
    n = str(random.randint(1, 2000))
    a1 = random.choice(nouns)
    a2 = random.choice(adjectives)
    addresses.append("{} {} {}".format(n, a1, a2))

PEOPLE = []
for i in temp_people:
    x = random.choice(addresses)
    addresses.remove(x)
    p = Person(i["fore"], i["sur"], x)
    PEOPLE.append(p)


TOR_NODES = []

TN = [
        programs.TorWebServer("The Onion Router :: Official Site", "tor", "tor.onion", "tor"),
        programs.TorWebServer("World Wide Web Directory :: Onionsite", "w3d", "w3d.onion", "w3d"),
        programs.MessageBoard("EnWired: Home", "enwired.onion", "enwired-onion", "enwired"),
        programs.TorWebServer("Apache HTTP Server 1.0", "rehack.onion", "rehack-onion", "httpserver"),
        programs.TorWebServer("Euclid :: Homepage", "euclid.onion", "euclid-web", "euclid"),
        programs.SignupService("euclid-signup", "signup.euclid.onion", "jmail"),
        programs.SignupService("5chan-signup", generateTorURL("5chansu"), "5chan"),
        programs.TorWebServer("Apache HTTP Server 1.0", generateTorURL("5chan"), "5chan", "httpserver"),
]

for node in TN:
    TOR_NODES.append(node)
