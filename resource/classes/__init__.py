class Base: 
    def __init__(self):
        pass
class Port(Base):
    def __init__(self, num, name):
        self.num = num
        self.name = name
class Node(Base):
    def __init__(self, name, address, files = [], users = [], ports = []):
        super().__init__()
        self.name = name
        self.address = address
        self.files = []