import json

chaine = "  !coucou je sui sun etst de command"

print(chaine.split()[0])
print(chaine.split()[1:])

resp = "!openbet"


class Command:

    def __init__(self, fun, ismod, arg=0):
        self.myFunction = fun
        self.ismod = ismod
        self.arg = arg


def truc(x):
    print("truc active", x)


if __name__ == '__main__':
    c = Command(truc, 0, 1)

    cmd2 = {"!openbet": c}
    cmd2["!openbet"].myFunction("Hihihihihihihi")
