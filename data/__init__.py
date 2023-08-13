from resource.classes import *
from game import programs
import resource.information as resourceInfo
from resource.libs import *
import data

NODES = [Node("Cheater's Stash","1337.1337.1337.1337")]
PORTS = [
    Port(21,"FTP"),
    Port(22,"SSH"),
    Port(6881,"BitTorrent Tracker"),
    Port(7777,"reHackOS Local Server")
    ]
PROGRAMS = [
    Program("help",programs.Help),
    Program("argtest",programs.Argtest)
    ]