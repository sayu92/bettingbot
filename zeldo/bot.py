# bot.py
# The code for our bot

import cfg
import utils
##import sql
import socket
import re
import scratch
import time, threading
from time import sleep
from bettingbot import *


def isCommand(message):
    if message.strip()[0] == '!':
        return True
    else:
        return False


def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")

    # threading.start_new_thread(utils.threadFillOpList, ())
    x = threading.Thread(target=utils.threadFillOpList)
    x.start()
    ##    commands = sql.getCommands()

    ##    cmd = []
    ##    for c in commands:
    ##        cmd.append(Command(c["Command"], c["Response"], c["Description"], c["Op"]))
    ##
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)

            if isCommand(message):
                command_name = message.split()[0]
                arguments = message.split()[1:]

                if command_name in scratch.cmd2.keys():
                    number_arguments = scratch.cmd2[command_name].arg

                    if number_arguments > 0:
                        scratch.cmd2[command_name].myFunction()
                    else:
                        scratch.cmd2[command_name].myFunction()

                else:
                    print("Commande non répertoriée")


            if message.strip() == "test":
                print(cfg.oplist)

        sleep(1)


if __name__ == "__main__":
    main()
