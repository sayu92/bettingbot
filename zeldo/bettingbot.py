#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 16:24:50 2019

@author: florence
"""
import math
import json

# ajouter les exceptions lorsqu'une valeur negative est ajoutee, float , ou autre structure
# devoir close bet avant de faire result
# erreur lorsqu on pari alors qu un bet en cours
# quand mettre a jour le fichier

# soldes_des_joueurs = {'manie' : 100 , 'riki' : 50, 'jakiro' : 120}

# if 'soldes_joueurs.json' in request.POST:
#    soldes_des_joueurs = json.loads(request.POST['mydata'])
# else:
#    soldes_des_joueurs = {} # or data = None
file = open('soldes_joueurs.json', 'r')

try:
    soldes_des_joueurs = json.load(file)
    file.close()

except json.JSONDecodeError:
    soldes_des_joueurs = {}
    file.close()


class Bet:
    on_going_bet = False

    def __init__(self, bet_interest=0.5):

        Bet.on_going_bet = False
        self.is_open = False
        self.bet_interest = bet_interest
        self.total_amount = 0
        self.number_betteur = 0
        self.compte = {}
        self.predictions = {'win': [],'lose': []}  # 'lose' : [list des joueurs ayant predit la defaite] 'win' : [list des
        # joeurs pariant sur la victoire]

        self.soldes = soldes_des_joueurs.copy()

    def __del__(self):
        Bet.on_going_bet = False
        print("noooon")

    def openBet(self):
        ## Ouvrir une session de paris ##
        Bet.on_going_bet = True
        self.is_open = True

        print("Faites vos jeux !!")

    def closeBet(self):
        ## Fermer l'acces aux paris ##
        self.is_open = False

        print("Les jeux sont faits, rien ne va plus !")

    def firstTimeBet(self, name):
        if name not in self.soldes:
            return True
        else:
            return False

    def soldIsOK(self, name, amount):

        if amount > self.soldes[name]:  # Verifie si le joueur possede la somme avancee ##
            print('Vas travailler {} au lieu de depenser l\'argent que t\'as pas'.format(name))
            return False
        else:
            return True

    def addBetteur(self, name, joueur_prediction, amount):
        ## Ajouter un joueur ##
        if self.is_open:

            if self.firstTimeBet(name):  # Verifie si le joueur parie pour la premiere fois
                self.soldes[name] = 1  # on donne 1 gold le cas echeant

            if self.soldIsOK(name, amount):  # Verifie que le joueur possede l argent misee

                self.soldes[name] -= amount  # On retire du livre de compte la somme misee  

                if name not in self.compte:  # Si c'est la premiere mise faite durant CE pari
                    self.compte[name] = amount  # On inscrit la valeur pariee
                    self.predictions[joueur_prediction].append(name)
                    self.number_betteur += 1

                else:
                    self.compte[name] += amount  # Si le joueur rencherit, on l ajoute

        else:

            if Bet.on_going_bet:
                print('Les jeux sont deja fermes')
            else:
                print("Aucun pari en cours")

    def soldUpdate(self):
        for joueur, somme in self.soldes.items():

            if somme > 0:
                soldes_des_joueurs[joueur] = somme
            else:
                soldes_des_joueurs[joueur] = 1  # On fait en sorte qu un joueur puisse toujours se retrouver avec 1 gold

        with open('soldes_joueurs.json', 'w') as json_file:
            json.dump(soldes_des_joueurs, json_file)

    def result(self, resultat):  # Envoie d erreur si mauvais input

        if resultat == "win":
            winner = "win"
            loser = "lose"
        else:
            winner = "lose"
            loser = "win"

        amount_to_distribut = 0
        amount_bet_win = 0

        list_losers = self.predictions[loser]
        list_winners = self.predictions[winner]
        best = []
        worst = []

        for joueur in list_losers:
            amount_to_distribut += self.compte[joueur]
            worst.append((joueur, self.compte[joueur]))

        for joueur in list_winners:  # On recredite le joueur de son pari
            self.soldes[joueur] += self.compte[joueur]
            amount_bet_win += self.compte[joueur]

        for joueur in list_winners:  # Calcul des gains supplementaires
            gain = math.floor(amount_to_distribut * self.compte[joueur] / amount_bet_win) + max(
                math.floor(self.bet_interest * self.compte[joueur]), 1)
            self.soldes[joueur] += gain
            best.append((joueur, gain))

        best.sort(key=lambda x: x[1], reverse=True)  # Pour afficher les meilleurs performances lors du bet
        worst.sort(key=lambda x: x[1])

        mess1 = "Les gagnants sont : "
        for i in range(len(best)):
            mess1 += "{} +{}, ".format(best[i][0], best[i][1])

        print(mess1)

        mess2 = "Les noobs sont : "
        for i in range(len(worst)):
            mess2 += "{} -{}, ".format(worst[i][0], worst[i][1])
        print(mess2)

        self.soldUpdate()

        self.__init__()  # on supprime le bet a la fin des paris

    def cancelBet(self):
        self.__init__()
        print("Le pari est annule")


if __name__ == '__main__':
    nvbet = Bet()

    nvbet.openBet()

    nvbet.addBetteur("riki", 'win', 1)
    nvbet.addBetteur("manie", 'lose', 1)
    #
    #    print(nvbet.compte)
    #
    nvbet.addBetteur("riki", 'win', 1)
    nvbet.addBetteur("manie", 'lose', 1)
    nvbet.addBetteur("jakiro", 'win', 1)

    nvbet.closeBet()
    nvbet.result('win')
    print(soldes_des_joueurs)
    print(Bet.on_going_bet)

    nvbet.openBet()
    nvbet.addBetteur("riki", 'win', 2)
    nvbet.addBetteur("jakiro", 'lose', 2)
    nvbet.addBetteur("manie", 'win', 1)

    nvbet.closeBet()
    nvbet.result('win')
