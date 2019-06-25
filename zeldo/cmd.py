import bettingbot
com={
   "!openbet": {"fun": "nvbet.openBet()", "Needmod": True, "arg": 0},
   "!bet": {"fun": "nvbet.addBetteur(username, arguments[0], arguments[1])", "Needmod": False, "arg": 3},
   "!closebet": {"fun": "nvbet.closeBet()", "Needmod": True, "arg": 0},
   "!result": {"fun": "nvbet.result(arguments[0])", "Needmod": True, "arg": 1},
   "!cancelbet": {"fun": "nvbet.cancelBet()", "Needmod": True, "arg": 0}
}
