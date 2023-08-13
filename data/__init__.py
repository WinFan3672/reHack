from resource.classes import *
from game import programs
import resource.information as resourceInfo
from resource.libs import *

global PORTS, NODES, PROGRAMS

def getPort(num, isOpen = False):
    for item in PORTS:
        if item.num == num:
            item.open = isOpen
            return item
        
PORTS = [
    Port(21,"FTP"),
    Port(22,"SSH"),
    Port(6881,"BitTorrent Tracker"),
    Port(7777,"reHackOS Local Server"),
    Port(80,"Web Server"),
    Port(1443,"SQL Database Server"),
    ]
NODES = [
    Node("International ISP Hub","1.1.1.1",ports = [getPort(21),getPort(22), getPort(1443,True)], minPorts = 2),
    Node("USA.GOV","112.35.89.12",ports=[getPort(80),getPort(6881,True)],minPorts=2),
    ]
PROGRAMS = [
    Program("help",programs.Help),
    Program("argtest",programs.Argtest),
    Program("ping",programs.Ping),
    Program("nmap",programs.nmap)
    ]