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
    def __init__(self, name, function, unlocked=False, price=0, classPlease=False):
        super().__init__()
        self.name = name
        self.function = function
        self.unlocked = unlocked
        self.price = price
        self.classPlease = classPlease

    def execute(self, args, player=None):
        if player:
            return self.function(args, player)
        else:
            return self.function(args)

    def __lt__(self, other):
        return self.name < other.name


class User(Base):
    def __init__(self, name, password=None, isAdmin=False):
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
        super().__init__()
        self.size = size
        self.length = length

    def data(self):
        data = []
        for x in range(self.length):
            d = ""
            for i in range(self.size):
                d += random.choice(["0", "1"])
            data.append(d)
        return "\n".join(data)


class File(Base):
    def __init__(self, name, data=None):
        super().__init__()
        self.name = name
        if data:
            self.data = data
        else:
            self.data = BinaryFile().data()


class Folder(Base):
    def __init__(self, name, files=[]):
        super().__init__()
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


class Log(Base):
    def __init__(self, text, address=None):
        super().__init__()
        if address:
            self.address = address
        else:
            self.address = data.getNode("localhost").address
        self.text = text


class Node(Base):
    def __init__(
        self,
        name,
        uid,
        address,
        files=[],
        users=[],
        ports=[],
        minPorts=0,
        linked=[],
        hacked=False,
        player=None,
    ):
        super().__init__()
        self.name = name
        self.uid = uid
        self.player = player
        self.address = address
        self.files = files + [Folder("sys", [File("core.sys"), File("x-server.sys")])]
        self.ports = ports
        self.minPorts = minPorts
        self.users = users
        self.hacked = hacked
        self.linked = linked
        self.visited = False
        self.nmap = False
        self.logs = []
        self.firewall = None

    def create_log(self, ip_address, text):
        self.logs.append(Log(ip_address, text))

    def clone(self, new_address):
        cloned_node = type(self)(
            name=self.name,
            uid=self.uid,
            address=new_address,
            files=self.files,  # Here, files will be shared between the original and the clone
            users=self.users.copy(),  # Other attributes that should be copied
            ports=self.ports.copy(),
            minPorts=self.minPorts,
            linked=self.linked.copy(),
            hacked=self.hacked,
            player=self.player,
        )

        return cloned_node

class Person(Base):
    def __init__(self, forename, surname, address):
        self.forename = forename
        self.surname = surname
        self.address = address
        self.age = random.randint(18, 60)
        
class Firewall(Base):
    def __init__(self, solution, time=1):
        super().__init__()
        self.solution = solution
        self.time = time

    def check(self, solution):
        return solution == self.solution        