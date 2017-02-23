from bet import *

class BetingSimulator(object):
    def __init__(self, capital = 0.0):
        self.initial_capital = capital
        self.current_capital = capital

    def simulate(self, bet, verbose = False):
        self.current_capital -= bet.getStake()
    
        won = bet.simulate(verbose=verbose)
        if (won == True):
            self.current_capital += bet.getEwk();
            outcome = "WON"
        else:
            outcome = "LOST"
            
        print(outcome + " current capital=" + getMoneyStr(self.current_capital))
        return outcome == "WON"
            
            
def testBetSimulator():
    event1 = Event("EV1", [Odd("1", 12), Odd("X", 6.3), Odd("2", 1.27)])
    event2 = Event("EV2", [Odd("1", 7.2), Odd("X", 4.25), Odd("2", 1.51)])
    event3 = Event("EV3", [Odd("1", 1.81), Odd("2", 1.81)])
    bet = Bet(10.0,0.12)
    bet.addItem(BetItem(event1, "1"))
    bet.addItem(BetItem(event2, "1"))
    bet.addItem(BetItem(event1, "2"))
    bet.addItem(BetItem(event3, "1"))
    bet.addItem(BetItem(event3, "1"))
    print(bet)
    
    wins=loses=0
    simulator = BetingSimulator()
    for _ in range(0, 1000):
        res = simulator.simulate(bet, verbose=True)
        if res: wins+=1 
        else: loses+=1
    print("WINS: " + str(wins) + " LOSES: " + str(loses))
    
testBetSimulator()
#testOffer()