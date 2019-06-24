# bot.py
# The code for our bot

import cfg
import cmd
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


def runCommand(sock, command):
    arguments = command.split()[1:]

    try:
        eval(command)
    except:
        utils.chat(sock, "Erreur dans l'exécution de la commande")



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

    ## Demarrage du module de paris
    file = open('soldes_joueurs.json', 'r')

    try:
        soldes_des_joueurs = json.load(file)
        file.close()

    except json.JSONDecodeError:
        soldes_des_joueurs = {}
        file.close()

    nvbet = Bet(soldes_des_joueurs, s)

    cmd2 = {}
    for i in cmd.com.keys():  # on met dans un dictionnaire l ensemble des commande
        cmd2[i] = scratch.Command(cmd.com[i]["fun"], cmd.com[i]["Needmod"], cmd.com[i]["arg"])

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

                if command_name in cmd2.keys():     # Vérification si la commande est dans le dictionnaire des commandes

                    if cmd2[command_name].ismod:    # Vérification de s'il s'agit d'une commande ayant besoin de droit de modération
                        if utils.isOp(username):
                            runCommand(s, cmd2[command_name].myFunction)

                    else:
                        runCommand(s, cmd2[command_name].myFunction)

                else:
                    print("Commande non répertoriée")

            if message.strip() == "test":
                print(cfg.oplist)

        sleep(1)


if __name__ == "__main__":
    main()
