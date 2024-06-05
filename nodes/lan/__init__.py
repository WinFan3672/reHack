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

mview = programs.RemoteLAN("Mountain View Intranet", "mountainremote", "intranet.mountain.view", users=[User("admin")])
mview_ftp = programs.FTPServer("Resources", "ftp", "ftp.local")
with open("data/mview_recipe.txt") as f:
    mview_ftp.pub.create_encrypted_file(File("Recipe.docx", f.read(), "mountainremote"), "mountainremote", "mountainous")
mview_ftp.pub.create_encrypted_file(File("Password.txt", "mountainous", "jrallypc"), "jrallypc", data.genString(32))
mview_ftp.inc.create_file("DearJames.txt", "Hello James. Please stop leaving passwords in the INCOMING folder. Just leave them in your PC's home folder. -Noah", "nbaileypc")
mview.add_device(mview_ftp)

sfec = programs.RemoteLAN("SFEC Intranet", "sfeclan", "lan.sfec.com", users=[User("admin")])

sfec_files = programs.PublicFTPServer("Files", "files", "files.local")
with open("data/sfeclan/report2010.txt") as f:
    sfec_files.pub.create_file("2010 Report.docx", f.read(), "sfecweb")
sfec_irc = programs.IRCServer("SFEC Internal IRC", "irc", "irc.local")
sfec_general = sfec_irc.add_channel("#general", "SFEC concerns")
sfec_general.add_message("admin", "welcome to the channel")

sfec.add_device(sfec_files)
sfec.add_device(sfec_irc)

dec = programs.RemoteLAN("DEC Remote LAN", "declan", data.generateIP(), minPorts=65536, users=[User("roy", "31718")])
dec.firewall = Firewall("dec", 3)

dec_ftp = programs.PublicFTPServer("FTP", "ftp", "ftp.local")

dec_src = ZippedFolder(Folder("dec-src-v1.0", [
    Folder("client", [
        Folder("cli", [
            File("main.c"),
            File("Makefile"),
        ]),
        Folder("gui", [
            File("main.c"),
            File("Makefile"),
        ]),
        Folder("libdec", [
            File("libdec.c"),
            File("libdec.h"),
            File("Makefile"),
        ]),
        Folder("private", [
            Folder("cli", [
                File("main.c"),
                File("Makefile")
            ]),
            Folder("lib", [
                File("libdecbruter.c"),
                File("libdecbruter.h"),
                File("Makefile")
            ]),
            File("ReadMe.txt", "Src for decbruter (can brute-force the passwords for DEC archives). If the public gets a copy of this, all hell breaks loose.")
        ]),
    ]),
    Folder("bin", [
        Folder("unix", [
            File("dec"),
            File("dec-gui"),
            File("libdec.so"),
            File("libdec.h")
        ]),
        Folder("workspaces", [
            File("dec.exe"),
            File("dec-gui.exe"),
            File("libdec.dll"),
            File("libdec.h"),
        ]),
    ]),
    Folder("crypto", [
        Folder("sigs", [
            Folder("public", [
                File("current.pem"),
                File("revoked.pem"),
            ]),
            Folder("private", [
                File("current.pem"),
                File("revoked.pem"),
            ]),
            File("ReadMe.txt", "This folder contains signatures used to sign compiled executables. They were acquired from a CA trusted by Nanosoft.")
        ]),
    ]),
    File("Makefile"),
    File("ReadMe.txt", "This is the src for DEC Suite v1.0. Do not distribute. Compile with SCC (Standard Compiler Collection) v2010.5.1+. Sign with crypto/sigs/private/current.pem"),
]), "roynet")

dec_enc = EncryptedFile(dec_src, "roynet", "infiltrate")
dec_ftp.pub.add_file(dec_enc, True)

dec.add_device(dec_ftp)

roynet = programs.LocalAreaNetwork("Roy Andresson's Network", "roynet", data.generateIP())
roynet_pc = Node("Roy's PC", "roy", "roy.local", ports=[data.getPort(22)])
roynet_nas = programs.FTPServer("Roy's Simology NAS", "nas", "nas.local")


with open("data/roy.txt") as f:
    roynet_nas.pub.create_file("Diary.docx", f.read())

roynet.add_device(roynet_pc)
roynet.add_device(roynet_nas)

blue_medical = programs.RemoteLAN("Blue Medical LAN", "bluelan", "work-vpn.bluemedical.com", minPorts=65536)
blue_forum = programs.Forum("Forum", "forum", "forum.local", "webmaster@bluemedical.mail.com")
blue_medical.add_device(blue_forum)

bfg = blue_forum.boards[0]

def main():
    return [
        cialan, 
        mview,
        sfec, 
        dec,
        roynet,
        blue_medical,
    ]
def tor():
    return [
        scsi,
    ]
