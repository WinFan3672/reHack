import sys
from resource.classes import *
from resource.libs import *
import data
def div():
    print("--------------------")
def br():
    div()
    input("Press ENTER to continue.")
def cls():
    """
    Clears the terminal screen.
    """
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")
    
def Help(args):
    div()
    print("help: list of programs")
    print("exit: returns to the main menu")
    div()
def Exit(args):
    sys.exit()
def Argtest(args):
    print(args)