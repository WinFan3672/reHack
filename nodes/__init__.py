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

## CIA Local Area Network
cialan = programs.LocalAreaNetwork("CIA Office Langley :: Local Area Network :: 1 of 1", "cialan", data.generateIP())

breakroom = programs.LocalAreaNetwork("Breakroom Wi-Fi", "breakroom", cialan.generateIP())
breakroom.add_device(programs.XOSDevice("Jack Skelly's xPhone", "jack_skelly", breakroom.generateIP(), notes=[programs.Note("Test")]))
breakroom.add_router()
cialan.add_device(breakroom)

ciaservers = programs.LocalAreaNetwork("Server Room Net Switch", "servers", cialan.generateIP())

target_watch = programs.NodeTracker("Target Companies and Orgs", "targets", ciaservers.generateIP())
target_watch.add_node("autocratmain")
target_watch.add_node("rehack")
target_watch.add_node("rehack_intranet")
target_watch.add_node("test2")
target_watch.add_node("torweb")
target_watch.add_node("shodan")

ciaservers = programs.LocalAreaNetwork("Server Room Net Switch", "servers", cialan.generateIP())
ciaservers.add_device(target_watch)
cialan.add_device(ciaservers)

ciaservers.add_router()


cialan.add_device(Node("Network Monitor v2.22", "netmonitor", cialan.generateIP()))
cialan.add_router()

## reHack Test LAN
testing = programs.LocalAreaNetwork("reHack Test: Local Area Network", "testlan", "lan.rehack.test")
for x in range(256):
    testing.add_device(Node("Test Device #{}".format(x), x, testing.generateIP()))

testing_nest = programs.LocalAreaNetwork("Nested LAN Test", "nestedlan", testing.generateIP())
testing_nest.add_device(Node("Node inside LAN inside LAN", "nesting", testing_nest.generateIP()))
testing_nest.add_router()

testing.add_device(testing_nest)
testing.add_device(Node("Hack me", "hackme", testing.generateIP()))
testing.add_router()

testforum = programs.Forum("Test Forum", "testforum", "forum.rehack.test", admin_password="root")

tf_general = testforum.boards[0]
tf_offtopic = testforum.add_board("Off topic", "")


TF_RULES ="\n".join([
    "1. Be nice.",
    "2. Be civil.",
    "3. No illegal activity.",
    "4. No witch hunting.",
])
tf_rules = tf_general.add_topic("Administrator", "Rules", TF_RULES)
tf_rules.reply("Administrator", "I like these rules.")
tf_rules.reply("SecondUser", "+1")
tf_rules.reply("ThirdUser", "+1")

vcforum = programs.Forum("VC Forum", "vcforum", data.generateTorURL("vcforum"), private=True)
vcgeneral = vcforum.boards[0] ## general discussion
vcstore = vcforum.add_board("Store", "Buy programs for use in your escapades")
vcjobs = vcforum.add_board("Jobs", "Get work here")
vcident = vcforum.add_board("Identities", "Leak the identities of random ppl")

chan = programs.Forum("5chan", "5chan", data.generateTorURL("5chan"), private=True)
chan_general = chan.boards[0]

chan_hack_advice = chan_general.add_topic("deadhead1337","Advice on hacking?", "I'm new to this kind of thing.")
chan_hack_advice.reply("admin", "The reHack Wiki (wiki.rehack.org) is a surprisingly good resource, if you're an agent.")
chan_hack_advice.reply("some_guy", "admin: reHack in general is great for new users; it pays well and you learn a lot")
chan_hack_advice.reply("admin", "some_guy: maybe 85% of the people I invite are agents")
chan_hack_advice.reply("digit", "admin: maybe that's why your forum is considered inferior to vcforum?")
chan_hack_advice.reply("deadhead1337", "aaaand the topic dies, thanks a lot digit")
chan_hack_advice.reply("admin", "digit: That's a ban.")
chan_hack_advice.reply("system", "admin banned digit")
chan_hack_advice.reply("system", "admin locked this topic")

chan_news = chan.add_board("News", "Reporting the news before the news does")
chan_jobs = chan.add_board("Jobs", "Find work here.")
chan_b = chan.add_board("Random (/b/)", "Random it is")
