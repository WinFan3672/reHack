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

scsi = programs.RemoteLAN("SCSI-Net", "scsi", data.generateTorURL())

scsi_irc = programs.IRCServer("SCSI Group IRC", "irc", "irc.local")
# scsi_irc.minPorts = 0
scsirc_general = scsi_irc.add_channel("#general", "The main discussion")
scsi.add_device(scsi_irc)

scsi_jobs = programs.MissionServer("Jobs", "jobs", "jobs.local")
scsi.add_device(scsi_jobs)

scsi_test = Node("Test Node", "test", "test.local", ports=[data.getPort(21), data.getPort(22)])
scsi.add_device(scsi_test)

mview = programs.RemoteLAN("Mountain View Intranet", "mountainremote", "intranet.mountain.view")
mview_ftp = programs.FTPServer("Resources", "ftp", "ftp.local")
mview.create_user("admin", "admin")
mview_ftp.create_user("admin", "admin")
with open("data/mview_recipe.txt") as f:
    mview_ftp.pub.create_encrypted_file(File("Recipe.docx", f.read(), "mountainremote"), "mountainremote", "mountainous")
mview_ftp.pub.create_encrypted_file(File("Password.txt", "mountainous", "jrallypc"), "jrallypc", data.genString(32))
mview_ftp.inc.create_file("DearJames.txt", "Hello James. Please stop leaving passwords in the INCOMING folder. Just leave them in your PC's home folder. -Noah", "nbaileypc")
mview.add_device(mview_ftp)

sfec = programs.RemoteLAN("SFEC Intranet", "sfeclan", "lan.sfec.com")

sfec_files = programs.PublicFTPServer("Files", "files", "files.local")
with open("data/sfeclan/report2010.txt") as f:
    sfec_files.pub.create_file("2010 Report.docx", f.read())
sfec_irc = programs.IRCServer("SFEC Internal IRC", "irc", "irc.local")
sfec_general = sfec_irc.add_channel("#general", "SFEC concerns")
sfec_general.add_message("admin", "welcome to the channel")

sfec.add_device(sfec_files)
sfec.add_device(sfec_irc)

def main():
    return [cialan, mview, sfec]
def tor():
    return [scsi]
