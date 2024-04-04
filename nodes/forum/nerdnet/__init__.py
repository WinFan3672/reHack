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

nerdnet = programs.Forum("NerdNet: Being Right > Money (Est. 2010)", "nerdnet", "nerd.net")
nerdnet.boards = [] ## Delete "General Discussion"

meta = nerdnet.add_board("n/nerdnet")
finance = nerdnet.add_board("n/finance")
funny = nerdnet.add_board("n/funny")
relationships = nerdnet.add_board("n/relationshipadvice")
programming = nerdnet.add_board("n/programming")
hacking = nerdnet.add_board("n/hacking")

subnerds = meta.add_board("n/nerdnet/subnerd_requests")
reports = meta.add_board("n/nerdnet/reports")

dcsebets = nerdnet.add_board("n/dcsebets")

rehack = hacking.add_topic("u/rehack", "[AD] Want To Learn Pentesting At a Professional Level? Join reHack!", """If you're reading this, you PROBABLY want to do hacking.
Well, unfortunately, most people seem to think that all hacking is illegal. They are wrong. While hacking can be very, very illegal, there are branches of it that are not.
reHack speciailises in one branch: penetration testing. You get hired by a company and you let loose whatever you can onto their systems, and tell them what vulnerabilities you found,
what data you could access, how much control you had over their network, etc. reHack is a company specialising in recruiting agents. Companies needing agents pay us money, 
and we find them agents (that's you!) to do the work. Once the company is happy, the agent is paid and the company goes about its merry way.

When you join, we offer:
* Free work;
* Resources and tools to learn the necessary skills;
* Extensive tutorial contracts to learn new skills;
* A thriving community of enthusiastic hackers;
* Generous pay (we tax companies 20% extra, which they take into account when making listings).

If this interests you, go to rehack.org and sign up today. It's free*!
*Agents will need to pass an examination, which we do offer (paid) training for if you fail.
""")

req_memes = subnerds.add_topic("u/drytron", "REQUEST: n/memes", """I think n/memes would be a very popular subnerd, and would provide a one-of-a-kind centralised place to store memes.""")
req_memes.reply("u/admin", "Don't think so. Storage/bandwidth costs would be sky-high, and we don't make any money yet.")

def main():
    return [nerdnet]

def tor():
    return []
