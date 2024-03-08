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

def main():
    return [cialan]

