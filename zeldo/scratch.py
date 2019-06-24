
import bettingbot






class Command:

    def __init__(self, fun, ismod, arg=0):
        self.myFunction = fun
        self.ismod = ismod
        self.arg = arg





def truc(x):
    print("truc active", x)


if __name__ == '__main__':

    nvbet = bettingbot.Bet()
    #nvbet.openBet() POURQUOI CA MARCHE ET PAS BESOIN DE FAIRE UN .BETTINGBOT-> A RESSAYER SANS LE EVAL
    print(cmd2["!openbet"].myFunction)

    chain = "coucou"
    print(eval(chain))