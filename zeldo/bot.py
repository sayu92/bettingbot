# bot.py
# The code for our bot

import cfg
import utils
##import sql
import socket
import re
import time, threading
from time import sleep


def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")

    #threading.start_new_thread(utils.threadFillOpList, ())
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

            if message.strip() == "!message":
                utils.chat(s,"Bonjour à la communauté des fruits")
        sleep(1)

if __name__ == "__main__":
    main()