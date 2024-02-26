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
tf_offtopic = testforum.add_board("Off topic")


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
vcstore = vcforum.add_board("Store")
vcjobs = vcforum.add_board("Jobs")
vcident = vcforum.add_board("Identities")

chan = programs.Forum("5chan", "5chan", data.generateTorURL("5chan"), private=True)
chan_general = chan.boards[0]
chan_general.add_board("Welcome")
chan_ident = chan_general.add_board("Identities")

CHAN_RULES = "\n".join([
    "1. Do not target other members of the forum.",
    "2. No flame wars.",
    "3. If a topic is locked, do NOT continue the discussion elsewhere.",
    "4. No discussion of politics outside of random",
    "5. Put topics in the right channel",
    "6. NEVER hack medical companies",
    "7. Do not discuss VC-Forum in an overly positive way",
    "8. Advertising other forums is permitted, as long as it is not intrusive",
    "9. Report rule-breaking by mentioning the admin, NEVER enforce the rules yourself",
    "10. Use common sense.",
])

chan_rules = chan_general.add_topic("admin", "Forum Rules", CHAN_RULES, True)

chan_hack_advice = chan_general.add_topic("deadhead1337","Advice on hacking?", "I'm new to this kind of thing.")
chan_hack_advice.reply("admin", "The reHack Wiki (wiki.rehack.org) is a surprisingly good resource, if you're an agent.")
chan_hack_advice.reply("some_guy", "admin: reHack in general is great for new users; it pays well and you learn a lot")
chan_hack_advice.reply("admin", "some_guy: maybe 85% of the people I invite are agents")
chan_hack_advice.reply("digit", "admin: maybe that's why your forum is considered inferior to vcforum?")
chan_hack_advice.reply("deadhead1337", "aaaand the topic dies, thanks a lot digit")
chan_hack_advice.reply("system", "admin locked this topic")

CHAN_XOS = "\n".join([
    "Hey all.",
    "I've been wondering.",
    "The admin password for xOS devices, alpine, has remained unchanged for like 5 years now.",
    "Are xDevices being paid off? Or is there another reason?",
    ])
chan_xos = chan_general.add_topic("nullzsec", "Thoughts on xOS?", CHAN_XOS)
chan_xos.reply("digit", "It could just be negligence.")
chan_xos.reply("admin", "digit: would not surprise me")
chan_xos.reply("rosebud", "could be a '''''secret''''''''' NSA backdoor")
chan_xos.reply("halt", "rosebud: a default password is hardly a backdoor, that's like calling routers NSA backdoors")
chan_xos.reply("rosebud", "halt: but phones != routers")
chan_xos.reply("halt", "rosebud: fair point, but the NSA could easily have something with remote access, not local access!")
chan_xos.reply("rosebud", "halt: it could be a subversion of expectations thing?")
chan_xos.reply("code", "rosebud, halt: you're both wrong; as an ex-xDevices employee (tacky, I know) I can confirm that management considered it a non-issue")
chan_xos.reply("admin", "code: it is a bad idea to potentially divulge your identity on a HACKING FORUM")
chan_xos.reply("code", "admin: didn't you once run mango farms before it was shut down?")
chan_xos.reply("admin", "that's a rumour, and you should always assume rumours to be false not true")
chan_xos.reply("code", "suspicious")
chan_xos.reply("admin", "Don't push it, I am the admin")
chan_xos.reply("mouse", "code, admin: you always seem to have feuds like this, why?")
chan_xos.reply("admin", "don't get me started on digit, let alone this blyat")
chan_xos.reply("digit", "hey!")
chan_xos.reply("nullzsec", "digit, code, admin: why do hackers need to be so full of themselves?")
chan_xos.reply("admin", "shut up nullzsec")
chan_xos.reply("digit", "Making too many enemies is a bad idea")
chan_xos.reply("code", "digit: That's rich coming from YOU")
chan_xos.reply("code", "nullzsec: rude")
chan_xos.reply("admin", "Because this has turned into a flame war, I'll lock this topic.")
chan_xos.reply("system", "admin locked this topic")

chan_news = chan.add_board("News")
chan_jobs = chan.add_board("Jobs")
chan_b = chan.add_board("Random (/b/)")

chan_userlist = chan_b.add_topic("nullzsec", "Why no userlist?", "I wanna know how many users there are on 5chan, cmon admin!")
chan_userlist.reply("admin", "Privacy reasons")
chan_userlist.reply("digit", "nah, admin wants to hide how many users are just him with a different name to 'add' to the discussion")
chan_userlist.reply("admin", "look at this chelovek")
chan_userlist.reply("code", "stop it with your google translated russian")
chan_userlist.reply("admin", "Откуда вы узнали, что я использую Google Translate?")
chan_userlist.reply("code", "It took you suspiciously long to reply with that one, and I know you have no life")
chan_userlist.reply("halt", "shots FIRED")
chan_userlist.reply("admin", "On a serious note, suggestions are not in /b/, suggestions are in general")
chan_userlist.reply("vc", "And where would I place your leaked identity documents?")
chan_userlist.reply("halt", "ah, the vc forum ring-leader in person!")
chan_userlist.reply("vc", "I don't deal with anons, least of all the admin of the anons")
chan_userlist.reply("vc", "anons are far too inexperienced")
chan_userlist.reply("vc", "Who the hell leaves a BLANK MISSION in the jobs section?")
chan_userlist.reply("vc", "proper onboarding is a proper mission, not free money")
chan_userlist.reply("vc", "How does that teach anyone anything?")
chan_userlist.reply("admin", "leaked deets go in /b/, and 5chan is so profitable we need to give away SOME of our cash")
chan_userlist.reply("vc", "are you sure, [DATA EXPUNGED BY admin]? With your [DATA EXPUNGED BY admin] credits in debt?")
chan_userlist.reply("system", "admin expunged a message")
chan_userlist.reply("vc", "scared of me, [DATA EXPUNGED BY admin]?")
chan_userlist.reply("system", "admin expunged a message")
chan_userlist.reply("vc", "You keep expunging me, and I'll keep recrutin'.")
chan_userlist.reply("vc", "For those interested in REAL hacking, search for us")
chan_userlist.reply("vc", "Those of you with real drive will find us easily")
chan_userlist.reply("system", "admin locked this topic")
