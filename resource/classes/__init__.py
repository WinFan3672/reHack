"""
This file contains classes accessible to ALL other files.
As such, no other code is imported, and it is free-standing.
Because of this, only core classes are included here.
"""

import random
import os
import string
import platform
import copy
import time
import getpass

WARN_TEXT = "WARNING! Deleting core.sys will break your system."

def div():
    print("--------------------")

def br():
    div()
    input("Press ENTER to continue.")


def makeRandomString(length=8):
    s = ""
    for i in range(length):
        c = string.printable
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
    def __init__(self, name, desc, function, unlocked=False, price=0, classPlease=False, inStore=True):
        super().__init__()
        self.name = name
        # self.version = version
        self.desc = desc
        self.function = function
        self.unlocked = unlocked
        self.price = price
        self.classPlease = classPlease
        self.inStore = inStore
    def __str__(self):
        return "Program({}, {})".format(self.name, self.version)

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
        self.password = password
        self.isAdmin = isAdmin

class Port(Base):
    def __init__(self, num, name, open=False):
        super().__init__()
        self.num = num
        self.name = name
        self.open = False

    def toggleOpen(self):
        self.open = False if self.open else True


class BinaryFile(Base):
    """
    This class is not for use by anything other than the File class INTERNALLY.
    It serves no function other than to generate random 'binary' data.
    """
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
            self.data = data.rstrip("\n") if type(data) == str else data
        else:
            self.data = BinaryFile().data()
        self.origin = origin
    def __str__(self):
        return "File(name='{}')".format(self.name)

    def clone(self):
        return File(self.name, self.data, self.origin)


class ZippedFolder(Base):
    def __init__(self, folder, origin=None):
        self.name = folder.name + ".zip"
        self.folder = folder if isinstance(folder, Folder) else Folder(name, origin=origin)
        self.origin = origin
        self.data = "This is a zipped folder. It requires compatible software to view and extract contents."
    def clone(self):
        return ZippedFolder(self.folder.clone(), self.origin)
    def __str__(self):
        return "ZippedFile(name='{}')".format(self.name)

class EncryptedFile(Base):
    def __init__(self, file, origin=None, password=None):
        self.file = file
        self.name = file.name + ".dec"
        self.origin = origin if origin else file.origin
        self.header = {"name": file.name, "origin": origin, "software": "DEC Solutions Encrypter v1.0a"}
        self.password = password
        self.data = "This file is encrypted.\nTo decrypt it, select DECRYPT FILE and enter the password, if one was set."
    def check(self, password):
        if self.password:
            return password == self.password
        else:
            return True
    def clone(self, deep=True):
        return EncryptedFile(self.file.clone() if deep else self.file, self.origin, self.password)


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
        return "Folder(name='{}', fileCount={}, access='{}', origin='{}')".format(self.name, len(self.files), "rw" if self.writeAccess else "r", self.origin)
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
    def add_file(self, file, preserve_origin=False):
        if type(file) in [File, EncryptedFile, ZippedFolder, Folder]:
            if not preserve_origin:
                file.origin = self.origin
            self.files.append(file.clone())
    
    def create_file(self, name, data, origin=None):
        file = File(name, data, origin if origin else self.origin)
        self.files.append(file)
        return file
    def create_encrypted_file(self, file, origin, password=None):
        file = EncryptedFile(file, origin, password)
        self.files.append(file)
        return file

    def create_folder(self, name, writeAccess=False):
        file = Folder(name, [], writeAccess, self.origin)
        self.files.append(file)
        return file

    def setWriteAccess(self, writeAccess=False):
        self.writeAccess = writeAccess
        for file in [x for x in self.files if isinstance(x, Folder)]:
            file.setWriteAccess(writeAccess)

    def set_origin(self, origin):
        self.origin = origin
        for file in self.files:
            if isinstance(file, Folder):
                file.set_origin(origin)
            else:
                file.origin = origin
    
    def clone(self, deep=False):
        if deep:
            return Folder(self.name, [x.clone() for x in self.files], self.writeAccess, self.origin)
        else:
            return Folder(self.name, self.files, self.writeAccess, self.origin)

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
        self.files = []

        self.create_folder("home")
        self.create_folder("sys")
        self.create_file("core.sys", self.genRand(), "sys")
        self.create_file("x-server.sys", self.genRand(), "sys")
        self.create_file("warning", WARN_TEXT, "sys")

        self.ports = ports if ports else []
        self.minPorts = minPorts
        self.users = users if users else []
        self.hacked = hacked
        self.linked = linked
        self.visited = False
        self.nmap = False
        self.logs = []
        self.firewall = None
        self.readAccess = False ## FTP read access
        self.playerPlease = False # if true, connect will pass player
                                  # to main() or main_hacked()
        self.installedPrograms = ["scan", "user", "info"] ## Used by ssh
        self.trace = None
    def login_screen(self):
        if not self.users:
            print("ERROR: No users registered on this machine.")
            return
        if self.hacked:
            return self.users[0]
        cls()
        div()
        print("Log In")
        div()
        username, password = input("Username $"), getpass.getpass("Password $")
        for user in self.users:
            if user.name == username and user.password == password:
                return user
        print("ERROR: Access denied.")
    def genRand(self, length=1024):
        s = ""
        for i in range(length):
            s += random.choice(string.printable)
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
    
    def create_file(self, name, data, folder="/", origin=None):
        if folder == "/":
            folder = Folder("", self.files)
        else:
            folder = self.get_file(folder)

        file = File(name, data, origin if origin else self.uid)
        folder.files.append(file)
        return file

    def create_folder(self, name, writeAccess=False):
        folder = Folder(name, [], writeAccess, self.uid)
        self.files.append(folder)
        return folder

    def check_health(self):
        return "core.sys" in [x.name for x in self.flatten()]
    
    def main(self, player=None):
        print("ERROR: Access denied.")
    # def main_hacked(self, player=None):
    #     print(self.motd)

    def create_user(self, username, password=None):
        self.users.append(User(username, password))
    
    def get_user(self, username):
        for user in self.users:
            if user.name == username:
                return user

    def get_file(self, name):
        for file in self.files:
            if name == file.name:
                return file


class Person(Base):
    def __init__(self, forename, surname, address=None, age=None):
        self.forename = forename
        self.surname = surname
        self.address = address
        self.age = age if age else random.randint(18, 60)


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
    def __init__(self, node, traceType="Corporate", time=60):
        """
        node: a uid of a node (passed into data.getAnyNode())
        traceType: one of the following values: 'Corporate', 'Government', 'Personal'
        time: how long it takes for the trace to resolve
        """
        self.node = node
        self.time = time
        self.startedTime = None
        self.traceType = traceType #if traceType in ["Personal", "Corporate", "Government"] else "Corporate"
        self.start()
    def start(self):
        if not self.startedTime:
            self.startedTime = time.time()
            self.endTime = self.startedTime + self.time
    def copy(self):
        return Trace(self.node, self.traceType, self.time)

class Action(Base):
    """
    An action that can run at a specified time.
    """
    def __init__(self, time, function):
        """
        time: a GameDate instance
        function: a callable object, such as a functio
        for log in player.logs:n
        """
        self.time = time
        self.function = function
    def run(self, time):
        if time == self.time and callable(self.function):
            self.function()
