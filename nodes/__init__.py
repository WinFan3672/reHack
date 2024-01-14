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
target_watch.add_node("rehack")
target_watch.add_node("rehack_intranet")
target_watch.add_node("torweb")

internal = programs.NodeTracker("Internal LAN Tracker", "lantrack", ciaservers.generateIP())

ciaservers = programs.LocalAreaNetwork("Server Room Net Switch", "servers", cialan.generateIP())
ciaservers.add_device(target_watch)
ciaservers.add_device(internal)
ciaservers.add_router()
cialan.add_device(ciaservers)


target_watch = programs.NodeTracker("Target Companies and Orgs", "targets", ciaservers.generateIP())
target_watch.add_node("rehack")
target_watch.add_node("rehack_intranet")
target_watch.add_node("torweb")

internal = programs.NodeTracker("Internal LAN Tracker", "lantrack", ciaservers.generateIP())
internal.add_node(cialan)

ciaservers.add_router()


cialan.add_device(ciaservers)
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
