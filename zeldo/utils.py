# utils.py
# A bunch of utility functions

import cfg
import urllib.request, json
import time, threading
from time import sleep
import re


# Function: chat
# Send a chat message to the server.
#    Parameters:
#      sock -- the socket over which to send the message
#      msg  -- the message to send
def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode('utf-8'))


# Function: ban
# Ban a user from the channel
#   Parameters:
#       sock -- the socket over which to send the ban command
#       user -- the user to be banned
def ban(sock, user):
    chat(sock, ".ban {}".format(user))


# Function: timeout
# Timeout a user for a set period of time
#   Parameters:
#       sock -- the socket over which to send the timeout command
#       user -- the user to be timed out
#       seconds -- the length of the timeout in seconds (default 600)
def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds))


# Function: threadFillOpList
# In a separate thread, fill up the op list
def threadFillOpList():
    print("thread 1")
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/sayu92/chatters"
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req).read()

            # if response.find("502 Bad Gateway") == -1:
            cfg.oplist.clear()
            data = json.loads(response)

            for p in data["chatters"]["moderators"]:
                cfg.oplist[p] = "mod"
            for p in data["chatters"]["global_mods"]:
                cfg.oplist[p] = "global_mod"
            for p in data["chatters"]["admins"]:
                cfg.oplist[p] = "admin"
            for p in data["chatters"]["staff"]:
                cfg.oplist[p] = "staff"
            for p in data["chatters"]["broadcaster"]:
                cfg.oplist[p] = "broadcaster"
        except:
            pass
        sleep(5)


def isOp(user):
    return user in cfg.oplist
