from resource.classes import *
from game import programs
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random

global PORTS, NODES, PROGRAMS
def getNode(uid):
    for item in NODES:
        if uid == item.uid:
            return item
def generateIP():
    c = []
    for i in range(4):
        c.append(random.randint(0,255))
    return ".".join([str(x) for x in c])
def getPort(num, isOpen = False):
    for item in PORTS:
        if item.num == num:
            item.open = isOpen
            return item
DISALLOWED_USERNAMES = [
    "admin",
    ]        
PORTS = [
    Port(21,"FTP"),
    Port(22,"SSH"),
    Port(23,"Telnet"),
    Port(6881,"BitTorrent Tracker"),
    Port(7777,"reHackOS Node"),
    Port(80,"Web Server"),
    Port(1443,"SQL Database"),
    Port(123,"NTP Time Server"),
    Port(1194,"VPN Server"),
    Port(25,"Mail Server"),
    Port(24525,"Message Board"),
    Port(65536,"DNS Server"),
    ]
testSrvFiles = [
    Folder("home",[
        Folder("stash",[
            File("hello.txt","hello")
            ]),
        File("test.txt","open sesame"),
        ]),
    ]
NODES = [
    Node("International ISP Hub","isp", "1.1.1.1",ports = [getPort(21),getPort(22), getPort(1443,True)], minPorts = 2, linked=["usagov"]),
    Node("SHODAN","shodan",generateIP(), ports = [getPort(80)], minPorts=1),
    Node("reHack Test Server","rehacktest","255.255.255.3",ports = [getPort(21),getPort(22)], files = testSrvFiles, hacked = True),
    programs.MessageBoard("reHack News", "rehack.news","rehacknews","rehack.news"),
    programs.WebServer("United States Government","usagov", "usa.gov", "usa.gov"),
    programs.WebServer("reHack Official","rehack","rehack.org","rehack.org"),
    programs.WebServer("reHack Intranet","rehack_intranet","intranet.rehack.org","intranet.rehack.org"),
    programs.WebServer("World Wide Web Directory","w3d","w3d.org","w3d.org"),
    programs.WebServer("reHack Directory","rehack_dir","directory.rehack.org","directory.rehack.org"),
    programs.MessageBoard("reHack News (Private)","news.rehack.org","rehack_news","news.rehack.org"),
    programs.WebServer("PWNED YOU GOT","pwned.reha.ck","pwned.reha.ck","pwned.reha.ck"),
    programs.WebServer("UK Government","gov.uk","gov.uk","gov.uk"),
    ]
PROGRAMS = [
    Program("help",programs.Help, True),
    Program("nmap",programs.nmap, True),
    Program("porthack",programs.porthack,True),
    Program("sshkill",programs.sshkill,True),
    Program("ftpkill",programs.ftpkill,True),
    Program("connect",game.programs.connect.main,True),
    Program("webworm",programs.webworm, price = 2500),
    Program("debug",programs.debuginfo,True,classPlease=True),
    Program("mxlookup",programs.mxlookup,True),
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
    "Saffron",
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
    "Mexican chili powder"
]