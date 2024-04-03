from resource.classes import *
from game import programs
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random
import json
import copy
import string
import data

cialan = programs.LocalAreaNetwork("CIA Local Area Network: Home Base", "cialan", data.generateIP(), users=[User("admin", "admin")])

breakroom = programs.LocalAreaNetwork("Breakroom Wi-Fi", "breakroom", cialan.generateIP())
breakroom.add_device(programs.XOSDevice("Jack Skelly's xPhone", "jack_skelly", breakroom.generateIP(), notes=[programs.Note("Test")]))
cialan.add_device(breakroom)

ciaservers = programs.LocalAreaNetwork("Server Room Net Switch", "servers", cialan.generateIP())
# target_watch = programs.NodeTracker("Target Companies and Orgs", "targets", ciaservers.generateIP())
# target_watch.add_node("autocratmain")
# target_watch.add_node("rehack")
# target_watch.add_node("rehack_intranet")
# target_watch.add_node("test2")
# target_watch.add_node("torweb")
# target_watch.add_node("shodan")

# ciaservers.add_device(target_watch)
cialan.add_device(ciaservers)

netmonitor = Node("Network Monitor v2.22", "netmonitor", cialan.generateIP(), ports=[data.getPort(21)])
netmonitor.create_file("ReadMe.txt", "This is a hacker honeypot. It has logged all CIA LAN traffic since 1/1/2007. Looks like the CIA's security isn't all it's cracked up to be.", folder="home")

cialan.add_device(netmonitor)
autocratmain = Node("Project Autocrat Mainframe", "autocratmain", cialan.generateIP(), ports=[data.getPort(21)])
autocratmain.create_file("autocrat.docx", data.AUTOCRAT, "home", cialan.uid)
cialan.add_device(autocratmain)

scsi = programs.RemoteLAN("SCSI-Net :: Connect to 192.168.0.0 for an IP list", "scsi", data.generateTorURL())

scsi_irc = programs.IRCServer("SCSI Group IRC", "irc", "irc.local")
# scsi_irc.minPorts = 0
scsirc_general = scsi_irc.add_channel("#general", "The main discussion")
scsi.add_device(scsi_irc)

scsi_test = Node("Test Node", "test", "test.local", ports=[data.getPort(21), data.getPort(22)])
scsi.add_device(scsi_test)

def main():
    return [cialan]
def tor():
    return [scsi]
