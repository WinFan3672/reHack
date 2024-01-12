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
cialan.add_device(programs.XOSDevice("Testing xPhone #11", "testphone11", cialan.generateIP()))
cialan.add_device(Node("CIA Local Mainframe Backup", "mainframe", cialan.generateIP()))
cialan.add_router()

## reHack Test LAN

testing = programs.LocalAreaNetwork("reHack Test: Local Area Network", "testlan", "lan.rehack.test")
for x in range(257):
    testing.add_device(Node("Test Device #{}".format(x), x, testing.generateIP()))
testing.add_router()
