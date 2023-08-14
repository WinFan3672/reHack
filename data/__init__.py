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
        
PORTS = [
    Port(21,"FTP"),
    Port(22,"SSH"),
    Port(6881,"BitTorrent Tracker"),
    Port(7777,"reHackOS Node"),
    Port(80,"Web Server"),
    Port(1443,"SQL Database"),
    Port(123,"NTP Time Server"),
    Port(1194,"VPN Server"),
    Port(25,"Mail Server"),
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
    Node("USA.GOV","usagov", generateIP(), ports=[getPort(80),getPort(6881,True)],minPorts=2),
    Node("SHODAN","shodan",generateIP(), ports = [getPort(80)], minPorts=1),
    Node("reHack Test Server","rehacktest","255.255.255.3",ports = [getPort(21),getPort(22)], files = testSrvFiles, hacked = True)
    ]
PROGRAMS = [
    Program("help",programs.Help, True),
    Program("nmap",programs.nmap, True),
    Program("directory",programs.Directory,True),
    Program("porthack",programs.porthack,True),
    Program("sshkill",programs.sshkill,True),
    Program("connect",game.programs.connect.main,True),
    Program("webworm",programs.webworm, price = 2500),
    ]