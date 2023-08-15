from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
from game.programs import JmailServer, MailAccount, EmailData, Email, sendEmail, MailServer
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
        super().__init__("Local Host","localhost","127.0.0.1", users = [User(name, password, True)])
        self.address = "127.0.0.1"
        self.name = name
        self.password = password
        self.files = [Folder("home"),Folder("bin"),Folder("sys"),[File("system.ini")]]
        self.minPorts = 100
        self.ports = [getPort(7777),getPort(22)]
        self.creditCount = 0
        self.lvl = 0
        servers = [
            self,
            JmailServer(self),
            MailServer("reHack Mail Server","rehack-mail","rehack.mail",self,[User("welcome")])
            ]
        bodies = [
                [
                "Welcome to reHack!",
                "To get you started, we recommend running the `tutorial` command.",
                ]
            ]
        bodies = ["\n".join(x) for x in bodies]
        emails = [
            Email("welcome@rehack.mail","{}@jmail.com".format(self.name),bodies[0])
            ]
        for item in servers:
            data.NODES.append(item)
        for item in emails:
            sendEmail(item)
    def main(self):
        while True:
            ch = input("{}@{} $".format(self.name, self.address))
            if ch in ["exit","quit"]:
                return
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
                if program and program.unlocked:
                    if program.classPlease:
                        program.execute(args, self)
                    else:
                        program.execute(args)
                else:
                    print("FATAL ERROR: The program was not found.")