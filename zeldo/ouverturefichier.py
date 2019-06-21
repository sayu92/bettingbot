#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 07:50:23 2019

@author: florence
"""

import json

if __name__ == '__main__' :

    file = open('soldes_joueurs.json','r')
    
    try:   
        soldes_des_joueurs = json.load(file)
        file.close()
    
    except json.JSONDecodeError :
        soldes_des_joueurs = {}
        file.close()
        print("erreur catch")
    
    
    print("la fin")