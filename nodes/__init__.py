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

import nodes.lan
import nodes.forum
import nodes.forum.nerdnet
import nodes.test
import nodes.university


rhwiki = programs.WikiServer("rehack Wiki", "rehack_wiki", "wiki.rehack.org", "wiki.rehack.org", "reHack Wiki")

wiki_hacking = rhwiki.homepage.add_category("Hacking")
wiki_hacking.add_page("How to hack")
wiki_hacking.add_page("Opening Ports")
wiki_hacking.add_page("Hacking Tor")
wiki_hacking.add_page("Firewalls")
wiki_hacking.add_page("LAN")
wiki_hacking.add_page("Encrypted Files")
wiki_hacking.add_page("Traces")

wiki_nodes = rhwiki.homepage.add_category("Nodes")
wiki_nodes.add_page("Tor")
# wiki_nodes.add_page("ISP Hub")
wiki_nodes.add_page("MasterVPS")

wiki_rh = rhwiki.homepage.add_category("reHack")
wiki_rh.add_page("Who we are")
wiki_rh.add_page("Services")
wiki_rh.add_page("Test Services")
wiki_rh.add_page("Store")

openstat = programs.WikiServer("OpenStat", "openstat", "openstat.org", "openstat", "OpenStat")
openstat_os = openstat.homepage.add_category("Operating System Marketshare")
openstat_os.add_page("Desktop OS Marketshare")

mht = programs.NewsServer("MHT", "mht", "mht.com", "admin@mht.mail.com")
with open("msgboard/mht.com/Confirming The Rumours") as f:
    mht_rumours = mht.add_story("Confirming The Rumours", "Admin", GameDate(), f.read())
    mht_rumours.reply("rehack", "Hopefully this encourages xDevices to update their admin password")
    mht_rumours.reply("admin", "rehack: Probably not, they've ignored it since the OG xPhone")
    mht_rumours.reply("duplexity", "what a madman; publishing an article months ahead of time under nda while saying literally nothing")

with open("msgboard/mht.com/dcseweb") as f:
    mht_dcse = mht.add_story("DCSE Launches New Web-Based Stock Exchange", "Admin", GameDate(), f.read())
    mht_dcse.reply("rehack", "when a company cites state-of-the-art encryption etc. they're just spurring on egotistical hackers")

debian_ftp = programs.PublicFTPServer("Debian FTP", "debianftp", "ftp.debian.org", False)
debian_ftp.pub.create_file("debian-5.0.5.iso", debian_ftp.genRand())
debian_ftp.pub.create_file("debian-5.0.5.iso.gz", debian_ftp.genRand())
debian_ftp.pub.create_file("debian-5.0.5.iso.zip", debian_ftp.genRand())
debian_ftp.pub.create_encrypted_file(File("debian-5.0.6.iso", debian_ftp.genRand(), "debianftp"), "debianftp", "debian")

search = programs.SearchEngine("Search: Find It All", "search", "search.com")
search.add("search")
search.add("jmail")
search.add("usagov")
search.add("w3d")
search.add("mail.com")
search.add("www.anon.mail")
search.add("cocaweb")
search.add("mountainweb")
search.add("xwebdesign.com")
search.add("nanosoftweb")
search.add("mastervps_web")
search.add("mastervps_central")
search.add("dexpertweb")
search.add("dexpertmain")
search.add("ffc.com")
search.add("rehack")
search.add("gov.uk")
search.add("rhbank")
search.add("mht")
search.add("enwired-web")
search.add("debianweb")
search.add("debiangit")
search.add("openstat")
search.add("ciaweb")

rhsearch = programs.SearchEngine("reHack Internal Search", "rhsearch", "search.rehack.org")
for area in search.searchArea:
    rhsearch.add(area)
rhsearch.add("maildotcomtracker")
rhsearch.add("uscrimdb")
rhsearch.add("crimdb_signup")

eff = programs.LinkTree("Electronic Frontier Foundation", "effmain", "eff.org")
eff.motd = """EFF: Because privacy is a basic human right"""
eff.add_link("effdonate")

meddb = programs.MedicalDatabase()
meddb.create_user("root", "root")

irc = programs.IRCServer("reHack IRC", "rhirc", "irc.rehack.org", True)
# irc.create_user("admin", "constant")
irc_general = irc.add_channel("#general", "General reHack discussion")
irc_news = irc.add_channel("#news", "Server Announcements", readOnly=True)
irc_news.allow("admin")
irc_news.allow("newsbot")
irc_news.add_message("newsbot", "Welcome to the News channel!")
irc_rules = irc.add_channel("#rules", "Read these!", readOnly=True)
irc_rules.allow("admin")
irc_rules.add_message("admin", "1. Only reHack agents")
irc_rules.add_message("admin", "2. No account sharing")
irc_rules.add_message("admin", "3. We are not 5chan")
irc_rules.add_message("admin", "4. Be nice to others")
irc_rules.add_message("admin", "5. Don't share your/other people's personal info")
irc_rules.add_message("admin", "6. Report suspected undercover agents to me ASAP")


that_irc = programs.IRCServer("ThatCD IRC", "thatirc", "irc.that.cd", private=True)
# that_rec = that_irc.add_channel("#recruitment", "Joining ThatCD? Get interviewed here!")

dcse = programs.StockMarket("DCSE", "dcse", "trade.dcse.com")

dcse_coca = programs.Stock("Coca Corporation", "COCA", 25)
dcse_idco = programs.Stock("IsDedCo", "IDCO", 62)
dcse_acme = programs.Stock("Acme Corporation", "ACME", 50)
dcse_anon = programs.Stock("AnonMail GmbH", "ANON", 11)
dcse_duck = programs.Stock("DuckDonald Corporation", "DUCK", 66)
dcse_mail = programs.Stock("JMail Incorporated", "MAIL", 45)

dcse.add_free_stock("COCA", 2)
dcse.add_free_stock("DUCK", 1)

dcse.add_stock(dcse_coca)
dcse.add_stock(dcse_idco)
dcse.add_stock(dcse_acme)
dcse.add_stock(dcse_anon)
dcse.add_stock(dcse_duck)
dcse.add_stock(dcse_mail)

nestaq = programs.StockMarket("Nestaq Stock Exchange", "nestaq", "trade.nestaq.com")

ffcftp = programs.FTPServer("FFC FTP Server", "ffcftp", "ftp.ffc.com")
with open("data/ffc.txt") as f:
    ffcftp.pub.create_file("HerbsAndSpices.docx", f.read())

mailcomftp = programs.FTPServer("Mail.Com FTP Server", "mailcomftp", "ftp.mail.com")
mailcomftp.pub.create_file("CME_2009_12_07.zip", None)
mailcomftp.pub.create_file("ReadMe.txt", """This folder contains tools deployed on all servers. For more info, see the docs server.""")

def main():
    return [
        mht,
        eff,
        search,
        debian_ftp,
        openstat,
        rhwiki,
        meddb,
        irc,
        that_irc,
        dcse,
        nestaq,
        ffcftp,
        mailcomftp,
    ] + nodes.forum.main() + nodes.forum.nerdnet.main() + nodes.test.main() + nodes.lan.main()

def tor():
    return [] + nodes.forum.tor() + nodes.forum.nerdnet.tor() + nodes.lan.tor()
