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


lan = programs.LocalAreaNetwork("reHack Test: Local Area Network", "testlan", "lan.rehack.test")
for x in range(256):
    lan.add_device(Node("Test Device #{}".format(x), x, lan.generateIP()))

lan_nest = programs.LocalAreaNetwork("Nested LAN Test", "nestedlan", lan.generateIP())
lan_nest.add_device(Node("Node inside LAN inside LAN", "nesting", lan_nest.generateIP()))

lan.add_device(lan_nest)
lan.add_device(Node("Hack me", "hackme", lan.generateIP()))

forum = programs.Forum("Test Forum", "forum", "forum.rehack.test", admin_password="root")
# forum.hacked = True

forum_general = forum.boards[0]
forum_offtopic = forum.add_board("Off topic")


FORUM_RULES ="\n".join([
    "1. Be nice.",
    "2. Be civil.",
    "3. No illegal activity.",
    "4. No witch hunting.",
])
forum_rules = forum_general.add_topic("Administrator", "Rules", FORUM_RULES)
forum_rules.reply("Administrator", "I like these rules.")
forum_rules.reply("SecondUser", "+1")
forum_rules.reply("ThirdUser", "+1")

git = programs.GitServer("Test Server VC", "testgit", "git.rehack.test")

blank = Node("Blank Node", "blanktest", "blank.rehack.test")

ftp = programs.PublicFTPServer("FTP Server Test", "ftptest", "ftp.rehack.test", users=[User("admin", "admin")])
ftp.pub.add_file(ZippedFolder(Folder("test", [File("foo"), File("bar")])))
ftp.pub.add_file(EncryptedFile(ZippedFolder(Folder("encryption_test", [File("foo"), File("bar")]))))

def main():
    return [git, forum, lan, blank, ftp]
