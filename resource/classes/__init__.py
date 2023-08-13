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
    def __init__(self, name, function):
        self.name = name
        self.function = function
    def execute(self, args):
        return self.function(args)
class User(Base):
    def __init__(self, name, password = None, isAdmin = False):
        super().__init__()    
        self.name = name
        self.password = password if password else makeRandomString()
class Port(Base):
    def __init__(self, num, name):
        super().__init__()
        self.num = num
        self.name = name
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
class Node(Base):
    def __init__(self, name, address, files = [], users = [], ports = [], minPorts = 0):
        super().__init__()
        self.name = name
        self.address = address
        self.files = files
