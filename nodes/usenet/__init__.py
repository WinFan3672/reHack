from resource.classes import *
from game import programs
from game.programs import Newsgroup, Email
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random
import json
import copy
import string
import data


alt = programs.Newsgroup("alt", "Anything goes")

rec = programs.Newsgroup("rec", "Recreational")

sci = programs.Newsgroup("sci", "Science")

news = programs.Newsgroup("news", "Usenet news from the Big-8 Management Board")

soc = programs.Newsgroup("soc", "Social discussion")

humanities = programs.Newsgroup("humanities", "Human society and culture")

talk = programs.Newsgroup("talk", "Talk about (controversial) stuff")

comp = programs.Newsgroup("comp", "Computer science")
comp.linux = comp.add_newsgroup(Newsgroup("comp.linux", "The Linux operating system"))
comp.linux.debian = comp.linux.add_newsgroup(Newsgroup("comp.linux.debian", "Debian Linux"))

es = programs.Newsgroup("eternalseptember", "Discussions about eternal-september.org")
es.es = es.add_newsgroup(Newsgroup("eternalseptember.eternalseptember", "General discussion"))
es.news = es.add_newsgroup(Newsgroup("eternalseptember.news", "News announcements"))

bin = programs.Newsgroup("bin", "Binary files")
bin.linux = bin.add_newsgroup(programs.Newsgroup("bin.linux", "Linux distro ISOs"))
bin.linux.debian = bin.linux.add_newsgroup(programs.Newsgroup("bin.linux.debian", "Debian Linux"))
bin.linux.debian.add_file(File("debian-5.0.5.iso", origin="debianftp"))

udn = programs.Newsgroup("udn", "Use.Net")
udn.news = udn.add_newsgroup(programs.Newsgroup("udn.news", "News/Announcements"))

with open("data/usenet/eternalseptember.news/welcome") as f:
    es.news.add_message(Email("Admin", "eternalseptember.news", "Welcome to Eternal September", f.read()))

with open("data/usenet/udn.news/welcome") as f:
    udn.news.add_message(Email("Admin", "udn.news", "Welcome to UDN", f.read()))

eternal_september = programs.Usenet("Eternal September", "eternal_september", "eternal-september.org")
eternal_september.add_newsgroup(alt)
eternal_september.add_newsgroup(comp)
eternal_september.add_newsgroup(rec)
eternal_september.add_newsgroup(sci)
eternal_september.add_newsgroup(talk)
eternal_september.add_newsgroup(soc)
eternal_september.add_newsgroup(humanities)
eternal_september.add_newsgroup(news)
eternal_september.add_newsgroup(es)

essu = programs.SignupService("essu", "sign-up.eternal-september.org", "eternal_september")

usedotnet = programs.Usenet("Use.Net", "use.net", "use.net", minPorts=1)
usedotnet.add_newsgroup(bin)
usedotnet.add_newsgroup(news)
usedotnet.add_newsgroup(udn)

def main():
    return [
        eternal_september,
        essu,
        usedotnet,
    ]

def tor():
    return []
