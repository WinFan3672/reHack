import random
import os
import string
import platform
import copy

WARN_TEXT = "WARNING! Deleting core.sys will break your system."

def div():
    print("--------------------")

def br():
    div()
    input("Press ENTER to continue.")


def makeRandomString(length=8):
    s = ""
    for i in range(length):
        c = string.ascii_letters
        s += random.choice(list(c))
    return s


def cls():
    """
    Clears the terminal screen.
    """
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")

class Base:
    def __init__(self):
        pass


class Program(Base):
    def __init__(self, name, version, desc, function, unlocked=False, price=0, classPlease=False):
        super().__init__()
        self.name = name
        self.version = version
        self.desc = desc
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
    def __init__(self, name, data=None, origin=None):
        super().__init__()
        self.name = name
        if data:
            self.data = data
        else:
            self.data = BinaryFile().data()
        self.origin = origin
    def __str__(self):
        return "File('{}')".format(self.name)

    def clone(self):
        return File(self.name, self.data)





class Folder(Base):
    def __init__(self, name, files=[], writeAccess=False, origin=None):
        super().__init__()
        self.name = name
        self.files = files
        self.writeAccess = writeAccess
        self.origin = origin
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.files):
            result = self.files[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
    def __str__(self):
        return "Folder('{}', {})".format(self.name, len(self.files))
    def flatten(self):
        all_files = []
        for file_or_folder in self.files:
            if isinstance(file_or_folder, File):
                all_files.append(file_or_folder)
            elif isinstance(file_or_folder, Folder):
                all_files.extend(file_or_folder.flatten())
        return all_files    

    def listDir(self):
        result = []
        for item in self.files:
            if isinstance(item, Folder):
                result.append([item.name] + item.listDir())
            else:
                result.append(item)
        return result

    def get_file(self, filename, filetype="Any", flatten=False):
        files = self.flatten() if flatten else self.files
        for file in files:
            if file.name == filename:
                if filetype == "Any":
                    return file
                elif filetype == "Folder" and isinstance(file, Folder):
                    return file
                elif filetype == "File" and isinstance(file, File):
                    return file
    def add_file(self, file):
        if type(file) in [File, Folder]:
            file.origin = self.origin
            self.files.append(file)

    def setWriteAccess(self, writeAccess=False):
        self.writeAccess = writeAccess
        for file in [x for x in self.files if isinstance(x, Folder)]:
            file.setWriteAccess(writeAccess)

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
        self.files = files + [Folder("home"), Folder("bin"), Folder("sys", [File("core.sys"), File("x-server.sys"), File("warning", WARN_TEXT)])] 
        self.ports = ports
        self.minPorts = minPorts
        self.users = users
        self.hacked = hacked
        self.linked = linked
        self.visited = False
        self.nmap = False
        self.logs = []
        self.firewall = None
        self.readAccess = False ## FTP read access
        self.playerPlease = False # if true, connect will pass player
                                  # to main() or main_hacked()
        self.motd = "\n".join([
            "$ Welcome to Bash on Debian GNU/Linux 5.0.5",
            "$ To open a remote shell, run ssh <address of this node>",
            "$ To browse this terminal's files, run ssh <address of this node>",
        ])
        self.trace = None
    def tick(self):
        ## This is called after every command
        pass
    def add_trace(self, time=60):
        self.trace = Trace(self, time)
    def flatten(self):
        files = []
        for file in self.files:
            if isinstance(file, File):
                files.append(file)
            elif isinstance(file, Folder):
                files.extend(file.flatten())
        return files

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
    
    def check_health(self):
        return "core.sys" in [x.name for x in self.flatten()]

    def main_hacked(self, player=None):
        print(self.motd)

    def create_user(self, username, password):
        self.users.append(User(username, password))


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


class Commit(Base):
    def __init__(self, text, origin="127.0.0.1"):
        self.text = text
        self.origin = origin
    def __str__(self):
        return "{}: {}".format(self.origin,self.text)

class Domain(Base):
    def __init__(self, name, base, assign=None):
        self.name = name
        self.base = base
        self.assign = assign
    def assign(self, addr):
        self.assign = addr
    def getName(self):
        return ".".join([self.name, self.base])

class Note(Base):
    def __init__(self, text):
        self.text = text

class NodeError(Exception):
    pass


class GameDate(Base):
    def __init__(self, year=2010, month=6, day=1):
        self.year = year
        self.month = month
        self.day = day
        self.daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __str__(self):
        return "{}-{}-{}".format(self.year, "0{}".format(self.month) if self.month < 10 else self.month, "0{}".format(self.day) if self.day < 10 else self.day)

    def next_day(self):
        self.daysPerMonth[1] = 29 if self.is_leap() else 28
        self.day += 1
        if self.day > self.daysPerMonth[self.month - 1]:
            self.day = 1
            self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

    def is_leap(self):
        return (self.year % 400 == 0) or ((self.year % 100 != 0) and (self.year % 4 == 0))

    def clone(self):
        return GameDate(self.year, self.month, self.day)

    def from_str(self, date):
        try:
            year, month, day = date.split("-")[0], date.split("-")[1], date.split("-")[2]
            if year > GameDate().year:
                self.year = year
            if month > GameDate().month:
                self.month = month
            if day > GameDate().day:
                self.day = day
            return True
        except IndexError:
            return False

    def __add__(self, days):
        new_date = copy.deepcopy(self)
        for _ in range(days):
            new_date.next_day()
        return new_date

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        return self.day < other.day

    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day

class Trace(Base):
    def __init__(self, node, time=60):
        self.node = node
        self.time = time
        self.startedTime = None
    def start(self):
        if not self.startedTime:
            self.startedTime = time.time()
    def copy(self):
        return Trace(self.node, self.time)
