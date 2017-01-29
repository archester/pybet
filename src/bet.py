from utils import * 

class Odd(object):
    def __init__(self, description, value):
        assert(isinstance(value, float) or isinstance(value, int))
        assert(value >= 1.0)
        
        self.description = description
        self.value = float(value)
        
    def getProbability(self):
        return 1 / self.value
        
    def __str__(self):
        return self.description + "\t" + str(self.value)

class Event(object):
    def __init__(self, name, odds=[]):
        self.name = name
        self.odds = odds[:]
        
    def __str__(self):
        result = self.name
        for o in self.odds:
            probability = self.__getOddProbablility(o)
            
            result += "\n" + o.__str__() + \
                      "\t" + getPercentStr(probability)
        
        return result
        
    def addOdd(self, odd):
        assert(isinstance(odd, Odd))
        #TODO: check if not already there        
        self.odds.append(odd)
        
    def getOddProbability(self, description):
        odd = self.__getOdd(description)
        
        return self.__getOddProbablility(odd)
    
    def getOddValue(self, description):
        odd = self.__getOdd(description)
        
        return odd.value
    
    def __getOdd(self, description):
        odd = [o for o in self.odds if o.description == description]
        assert(len(odd) == 1)
        
        return odd[0]
    
    def __getOddsProbabilitiesSum(self):
        return sum([o.getProbability() for o in self.odds])
    
    def __getOddProbablility(self, odd):
        return odd.getProbability() * (1/self.__getOddsProbabilitiesSum()) 

def testEventClass():
    # test event with same odds
    event = Event("A-B")
    event.addOdd(Odd("1", 1.81))
    event.addOdd(Odd("2", 1.81))
    assert(event.getOddProbability("1") == 0.5)
    assert(event.getOddProbability("2") == 0.5)
    print(event)
    #test event with 2 various odds
    event2 = Event("C-D")
    event2.addOdd(Odd("1", 1.25))
    event2.addOdd(Odd("2", 3.2))
    assert(event2.getOddProbability("1") > event2.getOddProbability("2"))
    print(event2)
    #test event with 3 various odds
    event3 = Event("E-F", [Odd("1", 12), Odd("X", 6.3), Odd("2", 1.27)])
    print(event3)    

# testEventClass()
    
class BetItem(object):
    def __init__(self, event, odd):
        assert(isinstance(event, Event))
        
        self.event = event
        self.odd = odd
        
    def getProbability(self):
        return self.event.getOddProbability(self.odd)
    
    def getName(self):
        return self.event.name
        
        
class Bet(object):
    def __init__(self, stake = 2.0, tax = 0.12):
        assert(tax >= 0.0 and tax < 1.0)

        self.items = []
        self.stake = stake
        self.tax = tax
        
    def __str__(self):
        result = "BET:\n"
        result += "num of items: " + str(len(self.items)) + "\n"

        for item in self.items:
            result += item.event.name + " " + item.odd + "\t" + str(item.event.getOddValue(item.odd)) + "\n"

        result += "AKO: " + str(self.getAko()) + "\n"
        result += "Stake: " + getMoneyStr(self.stake) + "\n"
        result += "EWK: " + getMoneyStr(self.getEwk()) + "\n"
        result += "probability: " + getPercentStr(self.getWinProbability()) + "\n"        
        
        return result
        
    def addItem(self, item):
        assert(isinstance(item, BetItem))
        #TODO: some verification
        self.items.append(item)
        
    def getAko(self):
        result = 1.0
        for item in self.items:
            result *= item.event.getOddValue(item.odd)
            
        return result
        
    def getWinProbability(self):
        result = 1
        for item in self.items:
            result = result * item.getProbability()
            
        return result
    
    def getEwk(self):
        return (self.stake * (1 - self.tax)) * self.getAko()
    
    def getStake(self):
        return self.stake
    
    def simulate(self, verbose = False):
        won = True
        for item in self.items:
            probability = item.getProbability()
            good = simulate(probability)
            if not good: 
                won = False
                if verbose:
                    print (item.getName()  + " : LOSE")
            else:
                if verbose:
                    print (item.getName()  + " : WIN")
        
        return won
         

def testBetClass():
    event1 = Event("Betis-Barcelona", [Odd("1", 12), Odd("X", 6.3), Odd("2", 1.27)])
    event2 = Event("Sasullo-Juventus", [Odd("1", 7.2), Odd("X", 4.25), Odd("2", 1.51)])
    bet = Bet()
    bet.addItem(BetItem(event1, "1"))
    bet.addItem(BetItem(event2, "2"))
    assert(bet.getAko() == 12*1.51)
    print(bet)

# testBetClass()

