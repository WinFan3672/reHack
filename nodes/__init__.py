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

rhwiki = programs.WikiServer("rehack Wiki", "rehack_wiki", "wiki.rehack.org", "wiki.rehack.org", "reHack Wiki")

wiki_hacking = rhwiki.homepage.add_category("Hacking")
wiki_hacking.add_page("How to hack")
wiki_hacking.add_page("Opening Ports")
wiki_hacking.add_page("Hacking Tor")
wiki_hacking.add_page("Firewalls")
wiki_hacking.add_page("LAN")

wiki_nodes = rhwiki.homepage.add_category("Nodes")
wiki_nodes.add_page("Tor")
wiki_nodes.add_page("ISP Hub")

wiki_rh = rhwiki.homepage.add_category("reHack")
wiki_rh.add_page("Who we are")
wiki_rh.add_page("Services")
wiki_rh.add_page("Test Services")

openstat = programs.WikiServer("OpenStat", "openstat", "openstat.org", "openstat", "OpenStat")
openstat_os = openstat.homepage.add_category("Operating System Marketshare")
openstat_os.add_page("Desktop OS Marketshare")

mht = programs.NewsServer("MHT", "mht", "mht.com", "admin@mht.mail.com")
with open("msgboard/mht.com/Confirming The Rumours") as f:
    mht_rumours = mht.add_story("Confirming The Rumours", "Admin", GameDate(), f.read())
    mht_rumours.reply("rehack", "Hopefully this encourages xDevices to update their admin password")
    mht_rumours.reply("admin", "rehack: Probably not, they've ignored it since the OG xPhone")
    mht_rumours.reply("duplexity", "what a madman; publishing an article months ahead of time under nda while saying literally nothing")

debian_ftp = programs.PublicFTPServer("Debian FTP", "debianftp", "ftp.debian.org")
debian_pub = data.getFile(debian_ftp, "pub", "Folder")
debian_pub.add_file(File("debian.5.0.5.iso.tar.gz", data.genBinaryFileData()))
