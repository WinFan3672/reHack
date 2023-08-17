from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
from game.programs import JmailServer, MailAccount, EmailData, Email, sendEmail, MailServer, AnonMail, MailDotCom, MissionServer
import data
import sys
import missions

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
        self.creditCount = 500
        self.lvl = 0
        self.currentMission = None
        self.startActions()
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
    def startActions(self):
        servers = [
            self,
            JmailServer(self),
            MailServer("reHack Mail Server","rehack-mail","rehack.mail",self,[User("welcome"),User("careers"),User("sales"),User("support"),User("contracts")],hideLookup=True),
            AnonMail(self),
            MailDotCom("XWebDesign Mail","xwebdesign.mail.com", self,[User("sales")]),
            MailDotCom("Mail Dot Com","root.mail.com", self, [User("sales")]),
            MailDotCom("Jmail Corporate Mail","jmail.mail.com",self,[User("sales")]),
            MailServer("WinFan3672 Personal Mail","mail3672","winfan3672.mail.com",self,[User("admin","somesecretpassword")]),
            MailServer("null.null","nullmail","null.null",self,[User("null")],minPorts=0),
            MissionServer("Rejected Missions Repository","rejected","rejects.rehack.org",self),
            MissionServer("reHack Contract Hub","rehack_contracts","contracts.rehack.org",self,missions.main_story_missions(self)),
            ]
        for item in servers:
            data.NODES.append(item)
        self.MISSIONS = missions.start_missions(self)
        self.currentMission = data.getMission("start1",self)
        self.currentMission.start()