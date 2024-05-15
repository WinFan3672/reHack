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
    mht_dcse.reply("rehack", "when a company cites state-of-the-art encryption etc. they're asking to get pwnd")

debian_ftp = programs.PublicFTPServer("Debian FTP", "debianftp", "ftp.debian.org", False)
debian_ftp.pub.create_file("debian-5.0.5.iso", debian_ftp.genRand())
debian_ftp.pub.create_file("debian-5.0.5.iso.gz", debian_ftp.genRand())
debian_ftp.pub.create_file("debian-5.0.5.iso.zip", debian_ftp.genRand())
debian_src = ZippedFolder(Folder("debian-5.0.5-src", [
    Folder("src", [
        Folder("drivers", [
            Folder("network", [
                File("network-aio.deb.cpp"),
                File("networklegacy-aio.deb.cpp"),
            ]),
            Folder("audio", [
                File("audio-aio.deb.cpp"),
                File("audiolegacy-aio.deb.cpp"),
            ]),
            File("cpu-gpu-readme.txt", "As you know, SMC ships FOSS drivers for their product. Debian doesn't ship the src to the drivers, but does ship the drivers themselves."),
        ]),
    ]),
    Folder("config", [
        Folder("etc", [
            Folder("apt", [
                File("sources.txt"),
            ]),
        ]),
    ]),
    Folder("bin", [
        Folder("debs", [
            File("coreutils.deb"),
            File("base.deb")
        ]),
        Folder("libs", [
            Folder("libdec", [
                File("libdec.so"),
                File("libdec.h"),
            ]),
            Folder("libaudio", [
                File("libaudio.so"),
                File("libaudio.h"),
            ]),
        ]),
        Folder("drivers", [
            Folder("gpu", [
                Folder("smc", [
                    File("smc-gpu-v222.45.22.deb"),
                ]),
                Folder("evasia", [
                    File("evasia-gpu-v2010.06.01.deb"),
                ]),
            ]),
            Folder("cpu", [
                Folder("simtel", [
                    File("simtel-cpu.deb"),
                    File("simtel-microcode.deb"),
                    File("simtel-management-engine.deb"),
                    File("ReadMe.txt", "This is the SimTel CPU drivers for up to SimTel Core (1st Generation)."),
                ]),
                Folder("smc", [
                    File("smc-cpu.deb"),
                    File("smc-microcode.deb"),
                    File("smc-psp.deb"),
                    File("ReadMe.txt", "This is the SMC CPU drivers for up to Apteron."),
                ]),
            ]),
        ]),
    ]),
    File("Makefile"),
    File("ReadMe.txt", """This is the Debian 5.0.5 source code. It includes proprietary blobs (incl. CPU/GPU drivers) that can be deleted.""")
]))

debian_ftp.pub.add_file(debian_src)

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

eff = programs.LinkTree("Electronic Frontier Foundation", "effmain", "eff.org", motd="""EFF: Because privacy is a basic human right""")
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

dcse = programs.StockMarket("DCSE", "dcse", "trade.dcse.com", adminPassword="shipment")

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
maildotcom_cme = ZippedFolder(Folder("CME_2009-12-01", [
    Folder("plugins", [
        File("NoReplyEmail.plugin.json"),
        File("MailDotComWebViewer.plugin.json"),
        File("SecurityPlus.plugin.json"),
        File("AdminUser.plugin.json"),
        File("MailDotCom.plugin.json"),
        File("")
    ]),
    Folder("config", [
        File("maild.cfg"),
    ]),
    Folder("installer", [
        File("dotnetfx35.exe"),
        File("mail.net-2003.exe"),
    ]),
    Folder("w2k3", [
        File("w2k3_RZR_1911.iso"),
        File("w2k3_RZR_1911.nfo", "Cracked By Razor 1911 on 2004-04-01: razor1911.com"),
        File("ProductKey.txt", "RZR19-11RZR-1911R-ZR191-1RZR1"),
    ]),
]))

mailcomftp.pub.add_file(maildotcom_cme)
mailcomftp.pub.create_file("ReadMe.txt", """This folder contains tools deployed on all servers. For more info, see the docs server.""")


debnews = programs.NewsServer("Debian News", "debnews", "news.debian.org")
with open("msgboard/debian/deb505") as f:
    debnews.add_story("Debian 5.0.5 Release Notes", "Debian Team", GameDate(2010, 1, 30), f.read())

duckdonald = programs.WikiServer("DuckDonald", "duckdonald", "duckdonald.com", "duckdonald", "Home")

duckdonald.homepage.add_page("About")

duck_meals = duckdonald.homepage.add_category("Menu Items")
duck_meals.add_page("DuckBurger")
duck_meals.add_page("DuckSalad")
duck_meals.add_page("Egg DuckMuffin")
duck_meals.add_page("Refreshments")

duckdonald.homepage.add_page("Careers")
duckdonald.homepage.add_page("Locations")

apache = programs.WikiServer("Apache Foundation", "apacheweb", "apache.org", "apache", "Apache")
apache.homepage.add_page("HTTP Server")
apache.homepage.add_page("Wiki Server")
apache.homepage.add_page("Apache Forwarder")

enwired_ftp = programs.FTPServer("EnWired FTP Server", "enwired-ftp", "ftp.enwired.com")
with open("data/enwired/EnwiredArticleList.docx.txt") as f:
    enwired_ftp.pub.create_file("EnwiredArticleList.docx", f.read())

enwired_articles = Folder("Articles")

ARTICLES = [
    "1978-0000.doc",
    "1990-0000.doc",
    "2000-0000.doc",
    "2003-0000.doc",
]

for article in ARTICLES:
    with open("data/enwired/articles/{}.txt".format(article)) as f:
        enwired_articles.create_file(article, f.read())

enwired_zip = ZippedFolder(enwired_articles)

enwired_ftp.pub.add_file(enwired_zip)

bravado_ftp = programs.FTPServer("Bravado Internal FTP", "bravado_ftp", "ftp.bravado.com")
bravado_ftp.firewall = Firewall("bravado", 0.75)

bravado_2010 = ZippedFolder(Folder("Bravado2010", [
    Folder("engineering", [
        File("Chasis.blend"),
        File("WndShldWipers.blend"),
    ]),
    Folder("design", [
        Folder("concepts", [
            File("2010-v1.png"),
            File("2010-v2.png"), 
            File("2010-v3.png"),
            File("2010-v4.png"),
            File("2010-v5.png"),
            File("2010-v6.png"),
            File("2010-v7.png"),
            File("2010-v8.png"),
            File("2010-v9.png"),
            File("2010-v10.png"),
            File("2010-v11.png"),
            File("2010-v12.png"),
        ]),
        File("FinalConceptArt.png"),
    ]),
    Folder("advertising", [
        Folder("posters", [
            File("The New Bravado 2010.bmp"),
            File("Bravado 2010 Refresh.bmp"),
        ]),
        Folder("tv", [
            File("RightNews.mp4"),
            File("LeftNews.mp4"),
            File("CenterNews.mp4"),
        ]),
        Folder("magazine", [
            File("The Car You Want.pdf"),
        ]),
        Folder("radio", [
            File("jingle.wav"),
            File("ad1.wav"),
            File("ad2.wav"),
        ]),
    ]),
    Folder("technical", [
        File("Technical Specifications.pdf"),
        File("Letter To Shareholders.pdf"),
    ]),
    File("Launch Date.txt", "2010-07-11"),
]))

bravado_ftp.pub.add_file(bravado_2010)

bluemedic_ftp = programs.FTPServer("Blue Medical FTP", "bluemedical_ftp", "ftp.bluemedical.com", minPorts=65536)

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
        debnews,
        duckdonald,
        apache,
        enwired_ftp,
        bravado_ftp,
        bluemedic_ftp,
    ] + nodes.forum.main() + nodes.forum.nerdnet.main() + nodes.test.main() + nodes.lan.main()

def tor():
    return [] + nodes.forum.tor() + nodes.forum.nerdnet.tor() + nodes.lan.tor()
