import random
class Base: 
    def __init__(self):
        pass
class Port(Base):
    def __init__(self, num, name):
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
                d += random.choice("0","1")
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
class Node(Base):
    def __init__(self, name, address, files = [], users = [], ports = []):
        super().__init__()
        self.name = name
        self.address = address
        self.files = []