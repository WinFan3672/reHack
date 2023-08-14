import random
import os
import string
def makeRandomString(length=8):
    s = ""
    for i in range(length):
        c = string.ascii_letters
        s += random.choice(list(c))
    return s
class Base: 
    def __init__(self):
        pass
class Program(Base):
    def __init__(self, name, function, unlocked = False, price = 0):
        self.name = name
        self.function = function
        self.unlocked = unlocked
        self.price = price
    def execute(self, args):
        return self.function(args)
class User(Base):
    def __init__(self, name, password = None, isAdmin = False):
        super().__init__()    
        self.name = name
        self.password = password if password else makeRandomString()
class Port(Base):
    def __init__(self, num, name, open=False):
        super().__init__()
        self.num = num
        self.name = name
        self.open = False
    def toggleOpen(self):
        self.open = False if self.open else True
class BinaryFile(Base):
    def __init__(self, size=32, length=32):
        self.size = size
        self.length = length
    def data(self):
        data = []
        for x in range(self.length):
            d = ""
            for i in range(self.size):
                d += random.choice(["0","1"])
            data.append(d)
        return "\n".join(data)    
class File(Base):
    def __init__(self, name, data = None):
        super().__init__()
        self.name = name
        if data:
            self.data = data
        else:
            self.data = BinaryFile().data()
class Folder(Base):
    def __init__(self, name, files = []):
        self.name = name
        self.files = files
    def listDir(self):
        result = []
        for item in self.files:
            if isinstance(item, Folder):
                result.append([item.name] + item.listDir())
            else:
                result.append(item)
        return result        
class Node(Base):
    def __init__(self, name, uid, address, files = [], users = [], ports = [], minPorts = 0, linked = [], hacked = False):
        super().__init__()
        self.name = name
        self.uid = uid
        self.address = address
        self.files = files
        self.ports = ports
        self.minPorts = minPorts
        self.users = users
        self.hacked = hacked
        self.linked = linked
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
