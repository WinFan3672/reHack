from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data
import sys
def getProgram(name):
    for item in data.PROGRAMS:
        if item.name == name:
            return item
def getPort(num):
    for item in data.PORTS:
        if item.num == num:
            return item
class PlayerNode(Node):
    def __init__(self, name, password):
        super().__init__("Local Host","127.0.0.1", users = [User(name, password, True)])
        self.address = "127.0.0.1"
        self.name = name
        self.password = password
        self.files = [Folder("home"),Folder("bin"),Folder("sys"),[File("system.ini")]]
        self.minPorts = 100
        self.ports = [getPort("reHackOS Local Server")]
    def main(self):
        ch = input("{}@{} $".format(self.name, self.address))
        if ch in ["exit","quit"]:
            sys.exit()
        elif ch == "":
            pass
        elif ch in ["clear","cls"]:
            cls()
        else:
            parts = ch.split(" ")
            if len(parts) == 1:
                args = []
            else:
                args = parts[1:]
            name = parts[0]
            program = getProgram(name)
            if program:
                program.execute(args)
            else:
                print("FATAL ERROR: The program was not found.")
        self.main()