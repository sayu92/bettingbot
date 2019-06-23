import json
import bettingbot
import cmd


cmd2 = {}


class Command:

    def __init__(self, fun, ismod, arg=0):
        self.myFunction = fun
        self.ismod = ismod
        self.arg = arg


for i in cmd.com.keys():
    cmd2[i] = Command(cmd.com[i]["fun"], cmd.com[i]["Needmod"], cmd.com[i]["arg"])


def truc(x):
    print("truc active", x)


if __name__ == '__main__':

    cmd2["!openbet"].myFunction()
