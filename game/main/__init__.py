from resource.classes import *
import resource.information as resinf
from resource.libs import *
def start():
    div()
    print("Welcome To ReHack")
    div()
    print("[1] New Game")
    print("[x] Load Game")
    div()
    print("Version: {}\nReleased: {}".format(resinf.friendlyVersion,resinf.friendlyRelDate))
    div()