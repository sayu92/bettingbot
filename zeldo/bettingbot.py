#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 16:24:50 2019

@author: florence
"""
import math
import json
import utils


# ajouter les exceptions lorsqu'une valeur negative est ajoutee, float , ou autre structure
# devoir close bet avant de faire result -
# erreur lorsqu on pari alors qu un bet en cours
# quand mettre a jour le fichier
# rajouer une commande pour voir l etat actuel du bet (somme pariés, cote etc)
# tester la fonction cancel bet
# rajouter le mot clef "all" execption "ValueError"
# vérifier les droits requis pour certaines commandes x
# message de confimration lorsqu un bet a été réalisé

#soldes_des_joueurs = {'manie' : 100 , 'riki' : 50, 'jakiro' : 120}

# if 'soldes_joueurs.json' in request.POST:
#    soldes_des_joueurs = json.loads(request.POST['mydata'])
# else:
#    soldes_des_joueurs = {} # or data = None

class Bet:
    on_going_bet = False

    def __init__(self, soldes_des_joueurs, socket, bet_interest=0.5):

        Bet.on_going_bet = False
        self.socket = socket

        self.is_open = False
        self.bet_interest = bet_interest
        self.total_amount = {"win": 0, "lose": 0}
        self.number_betteur = 0
        self.compte = {}
        self.predictions = {'win': [],
                            'lose': []}  # 'lose' : [list des joueurs ayant predit la defaite] 'win' : [list des
        # joeurs pariant sur la victoire]

        self.soldes = soldes_des_joueurs.copy()


    def openBet(self):
        ## Ouvrir une session de paris ##
        if Bet.on_going_bet == False and False == self.is_open:
            Bet.on_going_bet = True
            self.is_open = True
            utils.chat(self.socket, "Les paris sont ouverts !!")
        elif self.is_open:
            utils.chat(self.socket, "Il est toujours possible de miser pour le pari en cours")
        else:
            utils.chat(self.socket, "Les résultats du pari en cours n'ont toujours pas été rentrés")


    def closeBet(self):
        ## Fermer l'acces aux paris ##
        if self.is_open:
            self.is_open = False
            utils.chat(self.socket, "Les jeux sont faits, rien ne va plus !!")
        elif Bet.on_going_bet:
            utils.chat(self.socket, "La phase de paris a déjà été cloturé")
        else:
            utils.chat(self.socket, "Aucune session de paris n'a été ouverte")


    def statusBet(self):

        if Bet.on_going_bet:
            return "Mises actuelles : ( win: {} | lose: {} )".format(self.total_amount["win"], self.total_amount["lose"])



    def firstTimeBet(self, name):
        if name not in self.soldes:
            return True
        else:
            return False


    def soldIsOK(self, name, amount):

        if amount > self.soldes[name]:  # Verifie si le joueur possede la somme avancee ##
            utils.chat(self.socket, "Vas travailler {} au lieu de depenser l\'argent que t\'as pas".format(name))
            return False
        else:
            return True


    def addBetteur(self, name, joueur_prediction, amount):
        ## Ajouter un joueur ##
        if self.is_open:

            ## Verification si les arguments sont correctements rentrés ##
            if joueur_prediction != "win" and joueur_prediction != "lose":
                raise ValueError
                return None
            if amount <= 0:
                raise ValueError
                return


            if self.firstTimeBet(name):  # Verifie si le joueur parie pour la premiere fois
                self.soldes[name] = 1  # on donne 1 gold le cas echeant

            if self.soldIsOK(name, amount):  # Verifie que le joueur possede l argent misee

                self.soldes[name] -= amount  # On retire du livre de compte la somme misee  

                self.total_amount[joueur_prediction] += amount   # On garde en mémoire le total des sommes misées sur les issues différentes

                if name not in self.compte:  # Si c'est la premiere mise faite durant CE pari
                    self.compte[name] = amount  # On inscrit la valeur pariee
                    self.predictions[joueur_prediction].append(name)
                    self.number_betteur += 1

                else:
                    self.compte[name] += amount  # Si le joueur rencherit, on l ajoute

                utils.chat(self.socket, "" + self.statusBet())  # Affichage de l etats des paris si la mise est bien prise en compte

        else:

            if Bet.on_going_bet:
                utils.chat(self.socket, 'Les jeux sont deja fermes')
            else:
                utils.chat(self.socket, "Aucun pari en cours")

    def soldUpdate(self):
        file = open('soldes_joueurs.json', 'r')

        try:
            soldes_des_joueurs = json.load(file)
            file.close()

        except json.JSONDecodeError:
            soldes_des_joueurs = {}
            file.close()

        for joueur, somme in self.soldes.items():

            if somme > 0:
                soldes_des_joueurs[joueur] = somme
            else:
                soldes_des_joueurs[joueur] = 1  # On fait en sorte qu un joueur puisse toujours se retrouver avec 1 gold

        with open('soldes_joueurs.json', 'w') as json_file:
            json.dump(soldes_des_joueurs, json_file)

    def result(self, resultat):  # Envoie d erreur si mauvais input
        if Bet.on_going_bet and not self.is_open:

            ## Verification si les arguments sont correctements rentrés ##
            if resultat != "win" and resultat != "lose":
                raise ValueError
                return None

            ## Exécution de la fonction ##
            if resultat == "win":
                winner = "win"
                loser = "lose"
            else:
                winner = "lose"
                loser = "win"


            list_losers = self.predictions[loser]
            list_winners = self.predictions[winner]
            best = []
            worst = []

            for joueur in list_losers:
                worst.append((joueur, self.compte[joueur]))

            for joueur in list_winners:  # On recredite le joueur de son pari
                self.soldes[joueur] += self.compte[joueur]

            for joueur in list_winners:  # Calcul des gains supplementaires
                gain = math.floor(self.total_amount[loser] * self.compte[joueur] / self.total_amount[winner]) + max(
                    math.floor(self.bet_interest * self.compte[joueur]), 1)   # total_amount[loser] represente la somme misée par les perdants et à redistribuer
                self.soldes[joueur] += gain
                best.append((joueur, gain))

            best.sort(key=lambda x: x[1], reverse=True)  # Pour afficher les meilleurs performances lors du bet
            worst.sort(key=lambda x: x[1])

            mess1 = "MVP PogChamp : "
            for i in range(len(best)):
                mess1 += "{} +{}, ".format(best[i][0], best[i][1])


            mess1 += " | Plz report SwiftRage : "
            for i in range(len(worst)):
                mess1 += "{} -{}, ".format(worst[i][0], worst[i][1])


            utils.chat(self.socket, mess1)


            self.soldUpdate()

            Bet.on_going_bet = False
            self.is_open = False               # on supprime le bet a la fin des paris
            self.total_amount = {"win": 0, "lose": 0}
            self.number_betteur = 0
            self.compte = {}
            self.predictions = {'win': [],
                                'lose': []}  # 'lose' : [list des joueurs ayant predit la defaite] 'win' : [list des
        elif self.is_open:
            utils.chat(self.socket, "Les phases de paris n'ont pas été cloturées")

        else:
            utils.chat(self.socket, "Aucune seesion de paris n'a été ouverte")


    def cancelBet(self):
        Bet.on_going_bet = False
        self.is_open = False
        self.total_amount = {"win": 0, "lose": 0}
        self.number_betteur = 0
        self.predictions = {'win': [],
                            'lose': []}  # 'lose' : [list des joueurs ayant predit la defaite] 'win' : [list des
        # joeurs pariant sur la victoire]

        for people, amount in self.compte:
            self.soldes[people] += amount

        utils.chat(self.socket, "Session de paris annulée BibleThump")




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
