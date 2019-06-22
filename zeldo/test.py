import json
import urllib.request


url = "http://tmi.twitch.tv/group/user/froggedtv/chatters"
req =  urllib.request.Request(url)

r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))
oplist ={}

for people in cont['chatters']['moderators']:
    oplist[people] = "modo"

print("parsing des modos faits")

print("les modos sont : ")


for people, i in  oplist.items():
    print(people)
 
print(cont)

