from resource.classes import *
from game import programs
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random
import json
import copy
import string
import getpass

def copyFile(from_uid, to_uid, filename, from_foldername=None, to_foldername=None, preserve_origin=False):
    """
    Copies a file from one place to another.

    from_uid: UID of the node to copy from
    to_uid: UID of the node to copy from
    filename: name of file to copy
    from_foldername: name of folder to grab from (NOT recursive)
    to_foldername: name of folder to copy to
    preserve_origin: if True, the origin will not be overwritten
    """
    fromNode, toNode = getNode(from_uid), getNode(to_uid)
    from_folder = fromNode.get_file(from_foldername) if from_foldername else createFolder(fromNode)
    to_folder = toNode.get_file(to_foldername) if to_foldername else createFolder(toNode)

    file = from_folder.get_file(filename).clone()
    file.origin = fromNode.address

    to_folder.add_file(file, preserve_origin)

def getObject(iterable, obj):
    """
    Iterates through an iterable, and returns the first instance where it is equal to obj
    """
    for i in iterable:
        if i == obj:
            return i

def getPassword():
    passwd = getpass.getpass("Password $")
    if passwd == "":
        passwd = genString(12345)
    confirm = getpass.getpass("Confirm Password $")
    if passwd == confirm:
        return passwd
    else:
        print("ERROR: Password was incorrect.")
        return getPassword()

class BankAccount(programs.BankAccount):
    pass

global PORTS, NODES, TOR_NODES, PROGRAMS, GENERATED

CRIMDB_LETTER = """NOTE TO INTERN

The computer system you are interacting with is CRITICAL GOVERNMENT INFRASTRUCTURE.
It is constantly monitored, and all changes are double- and triple- and quadruple-checked 
to be correct. If you make a mistake, you'll get thrown off the network. 

DO:
    1. Make sure all changes you make are correct.
    2. Format all those changes properly.
    3. Respect other people and their time.
DON'T:
    1. Change data without permission.
    2. Be disrespectful of others' time.
    3. Attempt to disrupt the operation of the network.

Failure to comply with these DOs and DON'Ts can lead to:
    1. Prison time;
    2. Severe fines;
    3. Deportation back to your country of origin, in the case of immigrant/foreign workers."""
INCOMING_README = """This is the incoming folder.
If you have write access, this is where uploaded files should go.
Please respect the wishes of the maintainers of this FTP server and don't:

1. Upload files they wouldn't want on the server;
2. Waste bandwidth and/or storage space;
3. Delete other people's files without reason;
4. Attempt to gain write access maliciously;

This message was brought to you by the Apache Foundation."""

def getProgram(name, force=True):
    for program in PROGRAMS if force else [x for x in PROGRAMS if x.unlocked]:
        if name == program.name:
            return program

def extrapolateTime(realTimeSinceDay):
    # Define in-game constants
    inGameDayDuration = 600  # seconds
    inGameHourDuration = inGameDayDuration / 24  # seconds

    # Calculate the in-game hour
    inGameHour = (realTimeSinceDay % inGameDayDuration) / inGameHourDuration

    # Convert in-game hour to "HH:MM" format
    inGameHour_str = "{:02d}:{:02d}".format(int(inGameHour), int((inGameHour % 1) * 60))

    return inGameHour_str

def genBinaryFileData(length=1024, prefix=""):
    s = "{}".format(prefix) ## Creates a new copy of prefix
    while len(s) < length:
        s += random.choice(string.printable)
    return s

def createFolder(node: programs.Node):
    folder = Folder("/", node.files)
    folder.origin = node.uid
    return folder

def getFile(node, name, kind="Any"):
    FILES = [File, EncryptedFile, ZippedFolder]
    FOLDERS = [Folder]
    folder = Folder("", node.files)
    file = folder.get_file(name)
    if kind == "Any" and type(file) in FILES + FOLDERS:
        return file
    elif kind == "File" and type(file) in FILES:
        return file
    elif kind == "Folder" and type(file) in FOLDERS:
        return file

def div():
    print("--------------------")


def br():
    div()
    input("Press ENTER to continue.")

GENERATED = []


def checkPort(node: Node, num: int) -> bool:
    for port in node.ports:
        if port.num == num:
            return True
    return False

def getNodeList():
    return [x.uid for x in NODES if x.check_health()]


def getMission(mission_id: str, player):
    for mission in player.MISSIONS:
        if mission_id == mission.mission_id:
            return mission


def checkEmailAddress(address: str, checkDomain=None) -> bool:
    """
    Function that returns a boolean value depending on if an email address exists.
    """
    if not "@" in address:
        ## User entered something wrong
        return False
    parts = address.split("@")
    if len(parts) != 2:
        ## User added more than one '@'
        return False
    username = parts[0]
    domain = parts[1]

    if checkDomain and (domain != checkDomain):
        ## Email domain does not match, don't bother to check if that domain is valid
        return False

    node = getAnyNode(domain)
    if not node:
        ## Invalid mailserver
        return False

    users = [x.name for x in node.users]

    if username in users:
        return True
    else:
        return False

def checkEmailDomains(address: str, domains=[]) -> bool:
    for domain in domains:
        if checkEmailAddress(address, domain):
            return True
    return False

def getNode(uid: str, strict:bool=False, force:bool=False):
    for item in NODES:
        if (uid == item.uid and not strict) or uid == item.address and (item.check_health() or force):
            return item

def getTorNode(uid: str, strict:bool=False):
    for item in TOR_NODES:
        if (uid == item.uid and not strict) or uid == item.address and item.check_health():
            return item

def getAnyNode(uid, strict=False, force=False):
    node = getNode(uid, strict, force)
    if not node:
        node = getTorNode(uid, strict)
    return node

def addFirewall(node: Node, firewall: Firewall):
    if not isinstance(node, Node):
        node = getNode(node)
    node.firewall = firewall

def genString(genLength: int) -> str:

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
    if len(prefix) > 16:
        raise TypeError("Prefix cannot be > 16 characters long.")
    genLength = 16 - len(prefix)
    return prefix + genString(genLength) + ".onion"

def generateIP():
    c = []
    for i in range(4):
        c.append(random.randint(0, 255))
    ip = ".".join([str(x) for x in c])
    if ip in [x.address for x in NODES] + ["192.168.0.0"]:
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
    Port(119, "Usenet (NNTP) Server"),
    Port(123, "NTP Time Server"),
    Port(1194, "OpenVPN Server"),
    Port(1433, "SQL Database"),
    Port(6667, "Internet Relay Chat"),
    Port(6881, "BitTorrent Tracker"),
    Port(7777, "reHackOS Node"),
    Port(8989, "Blue Medical Device Port"),
    Port(9200, "Tor Relay"),
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

JMAIL_BODIES = [
    "\n".join([
        "Welcome to JMail!",
        "JMail is a convenient and secure email service designed for YOU.",
        "We have over 100,000,000 users, and we are happy to have you amongst them.",
        "Do note that a few sponsored emails may arrive in your inbox when your account is created.",
    ]),
    "\n".join([
        "For over 130 years, Coca has been the world's most refreshing drink for only 99c a bottle.",
        "For more info, visit coca.com and find out where YOU can find refreshment.",
    ]),
    "\n".join([
        "If you need a PROFESSIONAL email address, mail.com is here to help.",
        "Get a domain at yourname.mail.com, high security, and a satisfaction guarantee, for an affordable price.",
        "Go to mail.com for more info.",
    ]),
    "\n".join([
        "If you need a bank account (and you do), Bank of reHack may be for you!",
        "We offer low interest rates on loans and guaranteed security (FDIC insurance for up to 2 million Cr.)",
        "For more info, connect to 6.5.4.4 and make an account.",
    ]),
]
JMAIL_STARTING_EMAILS = [
    programs.Email("admin@jmail.com", "", "Welcome to JMail", JMAIL_BODIES[0]),
    programs.Email("admin@coca.mail", "", "Try Coca", JMAIL_BODIES[1]),
    programs.Email("admin@root.mail.com", "", "Mail For The Pros", JMAIL_BODIES[2]),
    programs.Email("admin@rehack.mail", "", "Bank of reHack: The Best Bank", JMAIL_BODIES[3]),
]

ANONMAIL_BODIES = [
    "\n".join([
        "Hello and welcome to AnonMail.",
        "As you might be able to gague from your email address, AnonMail is entirely anonymous.",
        "We have over a million users, and making a new identity is as easy as connecting",
        "to our signup service and making a new account. Great for privacy nerds, yes, but also great",
        "for criminals. However, as a service, we are legally protected from responsibility of our users' content.",
        "That being said, we do not encourage ANY illegal activity on AnonMail, although we're not sure if any",
        "has been occuring, because we use zero-access encryption. We can't even read this email.",
    ]),
    "\n".join([
        "I hope this email finds you well.",
        "Are you interested in finding work?",
        "Are you skilled in the area of cybersecurity?",
        "If you answered YES to both, email careers@rehack.mail and we'll get back to you.",
    ]),
    "\n".join([
        "Did you know that there's a whole other Internet out there?",
        "For more information, connect to tor.org and see for yourself.",
        "(Oh, and if you're unsure of where to go on Tor, w3d.onion is a good starting point)"
    ]),
]
ANONMAIL_STARTING_EMAILS = [
    programs.Email("ceo@anon.mail", "", "Welcome", ANONMAIL_BODIES[0]),
    programs.Email("careers@rehack.mail", "", "Would You Like To Join reHack?", ANONMAIL_BODIES[1]),
    programs.Email("null", "", "Join Tor Today", ANONMAIL_BODIES[2]),
]

EUCLID_BODIES = [
    "\n".join([
        "Hello and welcome to Euclid.",
        "We hope you find our services sufficient.",
        "We would like to kindly remind you that you can only receive email from other Tor mail servers.",
        "We do not (and never will) provide proxy services to send mail to or receive mail from clearnet mail servers.",
        "This is for security purposes. Tor emails are untraceable and encrypted by default.",
    ]),
]

EUCLID_EMAILS = [
    programs.Email("admin@euclid.onion", "", "Welcome to Euclid", EUCLID_BODIES[0]),
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

NODES.append(programs.BankBackEnd("Bank of reHack :: Back-End Server", "rehackbankbe", generateIP()))


N = [
    programs.ISPNode(),
    programs.Shodan(),
    Node(
        "reHack Test Server",
        "rehacktest",
        "test.rehack.org",
        ports=[getPort(21), getPort(22)],
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
    programs.WebServer("UK Government", "gov.uk", "gov.uk", "gov.uk"),
    programs.WebServer("FFC Corporate Home", "ffc.com", "ffc.com", "ffc.com", linked=["ffcftp"]),
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
        ports=[getPort(21), getPort(22), getPort(7777)],
        minPorts=65536,
        users=[User("admin", "anticyclogenesis")],
    ),
    Node(
        "John Grey's PC",
        "johngrey",
        generateIP(),
        ports=[getPort(21), getPort(22), getPort(6881)],
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
    programs.WebServer("Mountain View", "mountainweb", "mountain.view", "mountain.view",linked=["mountainmain", "mview.mail.com", "mountainremote"]),
    programs.WebServer("DomainExpert Home", "dexpertweb", "domain.expert", "domain.expert"),
    Node("Mountain View Mainframe","mountainmain", generateIP(), ports=[],minPorts=2**16,users=[User("admin","backdrop2252")]),
    # Node("Mountain View Remote Work Hub","moutainremote",generateIP(),ports=[getPort(22),getPort(21)],minPorts=2, linked =["jrallypc","nbaileypc","mflange"]),
    programs.XOSDevice("James Rally's xPhone","jrallyphone",generateIP()),
    programs.XOSDevice("Noah Bailey's xPhone","nbaileyphone",generateIP(),notes=[programs.Note("Get back at James Rally, I know he fired me.")],accounts=[programs.XOSMailAccount("admin@mview.mail.com","redhat")]),
    programs.XOSDevice("Monica Flange's xPhone","mflangephone",generateIP(),notes=[programs.Note("I know James Rally likes me. Fucking creep.")],accounts=[programs.XOSMailAccount("monicaf332@jmail.com","monica.flange")]),
    Node("James Rally's PC","jrallypc",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["jrallyphone"]),
    Node("Noah Bailey's PC","nbaileypc",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["nbaileyphone"]),
    Node("Monica Flange's PC","mflange",generateIP(),ports=[getPort(21),getPort(22)],minPorts=2,linked=["mflangephone"]),
    programs.MessageBoard("Mountain View Message Board",generateIP(),"mountainnotes","mview"),
    programs.MessageBoard("AnonMail Blog","blog.anon.mail","anonmail_blog","blog.anon.mail"),
    programs.GlobalDNS(),
    programs.VersionControl("Version Control Test","vctest","vc.rehack.test",users=[User("admin","alpine")]),
    programs.DomainExpert(),
    programs.WebServer("Central Intelligence Agency", "ciaweb", "cia.gov", "cia.gov",linked = ["ciamail", "ciaftp"]),
    Node("CIA File Transfer Protocol Server", "ciaftp", "ftp.cia.gov", ports=[getPort(21), getPort(22)], minPorts=1, linked=["cialan"]),
    programs.WebServer("The Onion Router :: Official Site", "torweb", "tor.org", "tor.org"),
    programs.MessageBoard("EnWired: Home", "enwired.com", "enwired-web", "enwired"),
    programs.WebServer("reHack Test Suite Home", "rehacktestmain", "rehack.test", "rehack.test"),
    Node("Blank Node Test", "blanktest", "blank.rehack.test"),
    programs.BankServer("Bank of reHack", "rhbank", "6.5.4.4", getNode("rehackbankbe").address, "socialism"),
    programs.SignupService("anonmail-signup", "signup.anon.mail", "anonmail", False, ANONMAIL_STARTING_EMAILS),
    programs.WebServer("Dark.Store Landing Page", "darkstore", "dark.store", "dark.store"),
    programs.SignupService("jmailsu", "signup.jmail.com", "jmail", junkMail=JMAIL_STARTING_EMAILS),
    programs.TorForwarder("rhomail-signup", "om.rehack.org", "rhomail-signup"),
    programs.PublicFTPServer("reHack Drop Server", "rhdrop", "drop.rehack.org", minPorts=65536),
    programs.Forwarder("mvps", "mvps.me", "mastervps_central"),
    programs.WebServer("reHack Signup Meta-Service", "sign.up", "sign.up", "sign.up"),
    programs.TorForwarder("vc-su", "vc.sign.up", "vc-signup"),
    programs.TorForwarder("5chan-su", "5chan.sign.up", "5chan-signup"),
    programs.WebServer("Debian: By the world, for the world", "debianweb", "debian.org", "debian.org"),
    programs.VersionControl("Debian: Official Git Server", "debiangit", "git.debian.org", [Commit("Release 5.0.0", "admin@mail.debian.org"), Commit("Release 5.0.1", "admin@mail.debian.org"), Commit("Release 5.0.2", "admin@mail.debian.org"), Commit("Release 5.0.3", "admin@mail.debian.org"), Commit("Release 5.0.4", "admin@mail.debian.org"),Commit("Release 5.0.5", "admin@mail.debian.org")], True),
    programs.MailDotComTracker(),
    programs.WebServer("Donate to the EFF", "effdonate", "donate.eff.org", "effdonate"),
    programs.PublicFTPServer("MHT FTP", "mhtftp", "ftp.mht.com", False),
    programs.WebServer("WarpMedia Broadband", "warpmediaweb", "warp.media", "warpmedia"),
    Node("Workspaces 7 Workstation Edition", "5chan_mission1", generateIP(), ports=[getPort(21), getPort(22), getPort(6881)]),
    programs.WebServer("DCSE Homepage", "dcseweb", "dcse.com", "dcse", linked=["sfecweb"]),
    programs.WebServer("SFEC Homepage", "sfecweb", "sfec.com", "sfec", linked=["sfeclan", "sfecmail"]),
    programs.WebServer("XCombinator", "xcombinatorweb", "xcombinator.com", "xcombinator"),
    programs.WebServer("Nestaq: Home", "nestaqweb", "nestaq.com", "nestaq"),
    programs.WebServer("DEC Solutions", "decweb", "dec.com", "dec", linked=["dec.mail.com"]),
    programs.SignupService("decsignup", "private-signup.dec.com", "declan"),
    programs.WebServer("sms (homepage)", "smsweb", "sms.us", "sms"),
    programs.WebServer("UUA Home", "uuaweb", "uua.edu", "uua"),
    programs.WebServer("Harvard", "harvardweb", "harvard.edu", "harvard"),
    programs.WebServer("Yale", "yaleweb", "yale.edu", "yale"),
    programs.WebServer("MIT", "mitweb", "mit.edu", "mit"),
    programs.WebServer("Dartmouth", "dartmoutheb", "dartmouth.edu", "apache"),
    programs.WebServer("Berkley", "berkleyweb", "berkley.edu", "berkley"),
    programs.WebServer("NanoSoft Expo 2010", "expo2010web", "expo2010.nanosoft.com", "expo2010"),
    programs.WebServer("NanoSoft Workspaces 8", "wp8web", "w8.nanosoft.com", "w8"),
    programs.WebServer("Workspaces Phone 8", "wp8web", "wp8.nanosoft.com", "wp8"),
    programs.Forwarder("duck", "duck.com", "duckdonald"),
    programs.WebServer("IsDed", "isded", "isded.com", "isded"),
    programs.WebServer("RAZOR 1911", "razor1911", "razor1911.com", "razor1911"),
    programs.WebServer("Bravado :: Luxury You Can't Afford", "bravado_web", "bravado.com", "bravado", linked=["bravado_ftp"]),
    programs.TimeServer("Workspaces Time Server", "workspaces_time", "time.workspaces.com"),
    programs.WebServer("Blue Medical Official Homepage", "bluemedical", "bluemedical.com", "bluemedical"),
    programs.WebServer("Eternal September: Democratising Usenet", "esweb", "www.eternal-september.org", "eternalseptember"),
    programs.WebServer("Use.Net Home", "udnweb", "www.use.net", "usedotnet"),
]
for item in N:
    NODES.append(item)
PROGRAMS = [
    Program("help", "Lists installed programs", programs.help, True),
    Program("nmap", "Scan a node for open ports", programs.nmap, True),
    Program("porthack", "Hijack open ports to install root access", programs.porthack, True),

    programs.PortBreakingTool("lancrack", 1, price=3500).program,
    programs.PortBreakingTool("ftpkill", 21, unlocked=True).program,
    programs.PortBreakingTool("sshkill", 22, unlocked=True).program,
    programs.PortBreakingTool("mailoverflow", 25, price=1500).program,
    programs.PortBreakingTool("webworm", 80, price=500).program,
    programs.PortBreakingTool("torrentpwn", 6881, price=750).program,
    programs.PortBreakingTool("sqldump", 1433, price=2500).program,

    Program("connect", "Connect to a node", game.programs.connect.main, True, classPlease=True),
    Program("history", "View a list of all connected nodes", game.programs.history,True, classPlease = True),
    Program("note", "Create and share plaintext notes", game.programs.note, True, classPlease=True),
    Program("ssh", "Connect to a node's command line over SSH", programs.ssh, True),
    Program("ftp", "Browse a node's files over FTP", programs.ftp, True),
    Program("debug", "For developers only", programs.debuginfo, True, price=0, classPlease=True),
    Program("mxlookup", "Gets a list of email addresss associated with a mail server", programs.mxlookup, price=1500),
    Program("jmail", "Read your emails", programs.jmail, True, classPlease=True),
    Program("store", "Purchase more programs", programs.store, True, classPlease=True),
    # Program("anonmail", programs.anonclient, price=250, classPlease=True),
    Program("login", "Gain root access to a node using an admin password", programs.login, True),
    Program("mission", "Run this command once you've finished your mission", programs.mission_program, True, classPlease=True),
    Program("logview", "View logs for a (hacked) node", programs.logview, True),
    Program("nodecheck", "Tool for checking what type of node a node is", programs.nodecheck, True),
    Program("mailman", "Email client", programs.mailman_base, True, classPlease=True),
    Program("bruter", "Attempts to brute-force a node's admin password using a small dictionary", programs.bruter, True, classPlease=True),
    Program("emailbruter", "Attempts to brute-force an email address password using a small dictionary", programs.emailbruter, True, classPlease=True),
    Program("firewall", "The firewall multi-tool, free for a limited time only", programs.firewall, price=0),
    Program("tor", "Connect to the Tor network", programs.tor, True, classPlease=True, inStore=False),
    # Program("sweep", programs.sweep, price=0),
    Program("save", "Save the game", programs.save,True,classPlease=True),
    Program("lanconnect", "Connect to a hacked LAN as if you were inside of the network", programs.LANConnect, True, classPlease=True),
    Program("account", "List all saved bank accounts", programs.accountList, True, classPlease=True),
    Program("bankhack", "Tool for brute-forcing a bank PIN", programs.bankhack, price=1000, classPlease=True),
    Program("tormail", "Email client for the Tor network", programs.tormail, True, classPlease=True),
    Program("date", "Check the date and time", programs.date, True, classPlease=True),
    Program("openftp", "Install an FTP server to a remote node", programs.openftp, price=10000, inStore=False),
    Program("chmod", "Set permissions for a folder and its contents on a remote node", programs.chmod, True),
    Program("irc", "IRC client", programs.irc, True),
    Program("logclear", "Clears logs on a remote node", programs.logclear, price=500),
    Program("darkstore", "The one-stop shop for ALL your Tor needs", programs.darkstore, inStore=False),
    Program("scsi", "Official SCSI-NET client", programs.scsi, inStore=False),
    Program("unhack", "Removes root access from a node", programs.unhack, True),
    Program("autohack", "Semi-automatically hacks a node", programs.autohack, price=1500, inStore=False),
    Program("autohack2", "Automatically hacks a node", programs.autohack2, price=3500, inStore=False),
    Program("tor_addon", "Adds tor support to ALL port breakers", programs.tor_addon, price=500, inStore=False),
]

DARKSTORE = [
    "openftp",
    "autohack",
    "tor_addon",
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
    programs.MessageBoard("The Tor Times", "tortimes", "tortimes.onion", "tortimes"),
    programs.MessageBoard("EnWired: Home", "enwired.onion", "enwired-onion", "enwired"),
    programs.TorWebServer("Apache HTTP Server 1.0", "rehack.onion", "rehack-onion", "httpserver"),
    programs.TorWebServer("Euclid :: Homepage", "euclid-web", "www.euclid.onion", "euclid"),
    programs.TorSignupService("euclid-signup", "signup.euclid.onion", "euclid", False, EUCLID_EMAILS),
    programs.TorSignupService("5chan-signup", generateTorURL("5chansu"), "5chan", usePlayerName=True),
    programs.TorSignupService("rhomail-signup", generateTorURL(), "rhomail", usePlayerName=True),
    programs.TorSignupService("vc-signup", generateTorURL("vcsu"), "vcforum", usePlayerName=True, private=["anonmail", "euclid"]),
    programs.TorSignupService("ds-signup", generateTorURL("darkstoresu"), "darkstore", usePlayerName=True, private=["rhmail"]),
    programs.ProgramInstaller("DarkStore", "darkstore", "darkstore.onion", getProgram("darkstore")),
    programs.ProgramInstaller("SCSI Client", "scsiclient", generateTorURL("scsiclient"), getProgram("scsi")),
    programs.ProgramInstaller("Autohack2", "autohack2", generateTorURL("autohack2"), getProgram("autohack2")),
    programs.Forwarder("nerdnet", "nerd-net.onion", "nerdnet"),
    programs.Forwarder("mht", "mht.onion", "mht"),
]
for node in TN:
    TOR_NODES.append(node)

CRIMES = [
    "Petty theft",
    "Theft",
    "Murder",
    "Arson",
    "Tax evasion",
    "Unauthorised computer access",
    "Drug Trafficking",
    "Other",
]    

with open("data/autocrat.docx.txt") as f:
    AUTOCRAT = f.read()

jrallypc = getNode("jrallypc")
jrallypc_home = jrallypc.get_file("home")
jrally_file = jrallypc_home.create_file("Password.txt", "mountainous", "jrallypc")
jrallypc_home.create_encrypted_file(jrally_file, "jrally_file", genString(32))



PRISON_STATUS = [
    "Incarcerated",
    "Free",
    "Awaiting Parole",
    "Awaiting Release",
    "Deceased",
    "Supervised Leave",
    "Transferring",
    "Missing",
]
