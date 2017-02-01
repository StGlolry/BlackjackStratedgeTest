# -*- coding: utf-8 -*-

from random import shuffle


class Card:
    '''
    This simple class manages single card objects.
    It has not any methods.
    '''
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

 
class Hand:
    '''
    This class manages hands that are lists of card object.
    It has some methods.
    '''
    
    def __init__(self):
        self.cards = [] #The hand is empty
        
    def __str__(self):
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['Ace', 'Two', 'Three', 'Four', 'Five',
                 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
                 'Jack', 'Queen', 'King']
        s = ''
        for card in self.cards:
            s += (' ' + ranks[card.rank - 1] + ' of '
                 + suits[card.suit - 1] + '\n')
        return s
    
    def IsAce(self):
        '''Check if is there at least one ace in the hand'''
        
        for card in self.cards:
            if card.rank == 1:
                return True
        else:
            return False
        
    def Add(self, card):
        '''Add a card at the END of the hand'''

        self.cards.append(card)

    def Reset(self):
        '''The hand return to be empty'''
        
        self.cards = []
            
    def Remove(self):
        '''Remove the FIRST card in the hand'''

        if self.cards == []: #If the hand is empty
            return False
        else:
            return self.cards.pop(0)
        
    def Value(self, ace):
        '''Return the value of the deck according to the ace'''
        self.value = 0 #The value of the hand is zero at beginning
        for card in self.cards: #For every card in the hand
            if card.rank > 10: #If it is a figure...
                self.value += 10 #...is value is 10
            elif card.rank == 1: #If it is an ace...
                if ace: #...according to the parameter...
                    self.value += 1 #...his value is 1...
                else:
                    self.value += 11 #...or 11
            else:
                self.value += card.rank #Else his value is the mark
        return self.value


class Deck(Hand):
    '''
    This class is inherited from Hand class.
    It manages decks that are like hands.
    It has only a method more.
    '''
    
    def __init__(self):
        self.cards = []
        for iDeck in range(1,9):
            for mark in range(1, 14): #for every marks
                for suit in range(1, 5): #for every suits
                    self.Add(Card(mark, suit)) #Add a card to the deck
                
    def Shuffle(self, times):
        '''Shuffle the deck though it is empty'''
        
        for i in range(times):
            shuffle(self.cards)
        
        
class Player:
    '''
    This simple class manages player objects.
    It allow to have some simple thing with them,
    like bet or win money.
    '''
    
    def __init__(self, money):
        self.money = money
        self.hand = Hand() #Every player has a hand
        self.candouble=True;
        self.cansurrender=True;
        
    def Bet(self):

        #Always bet 100
        self.bet = 100;
        return True
        '''Return true if you can bet'''
        
        if bet > self.money: #If your money is not enough...
            return False #...you can't bet
        else:
            self.bet = bet
            return True
    
    def Win(self):
        '''Win your bet'''
        
        self.money += self.bet * 1.0
    
    def Lose(self):
        '''Lose your bet'''
        
        self.money -= self.bet

    def LoseHalf(self):
        self.money -= self.bet * 0.5;

    def Take(self, deck, ncards):
        '''Add n cards to the hand taking them form the deck'''
        for i in range(ncards):
            self.hand.Add(deck.Remove())


class Dealer(Player):
    '''
    This class manages the dealer
    '''

    def __init__(self):
        self.hand = Hand() #Also the dealer has a hand
            
    def Play(self, deck):
        '''The dealer plays according to his rule'''
        
        while self.hand.Value(True) < 17:
            self.Take(deck, 1)
 
 
class View:
    '''
    This class manages the interface from
    the player to the game and vice versa
    '''

    def __init__(self, deck, player, dealer,hardtable):
        self.deck = deck
        self.player = player
        self.dealer = dealer
        self.hardtable = hardtable

    def AskBet(self):
        '''Return how much the player wants to bet'''
        
        bet = input('How much is your bet? ')
        while bet > self.player.money:
            print('You don\'t have enough money!')
            bet = input('How much is your bey? ')
        return bet
        
    def DealerHand(self):
        
        '''Print the dealer\'s hand'''
        print(str(self.dealer.hand.Value(True))+':')
        # print('The dealer\'s hand is ' + 
              # str(self.dealer.hand.Value(True)))
        # print(self.dealer.hand)
        
    def PlayerHand(self):
        '''Print the player\'s hand'''
        
        if (self.player.hand.IsAce() and 
            self.player.hand.Value(False) <= 21):
            # print('Your hand is ' + 
                  # str(self.player.hand.Value(True)) + ' o '
                  # + str(self.player.hand.Value(False)))
            print (str(self.player.hand.Value(True)) + '/' + str(self.player.hand.Value(False))+' vs'),
        else:
            # print('Your hand is ' +  
                  # str(self.player.hand.Value(True)))
        # print(self.player.hand)
            print (str(self.player.hand.Value(True))+' vs'),

    def AskHitStand(self):
        # here we can implement our stratedge
        '''Return true if the pl ayer wants hit'''
        soft=0;
        if(self.player.hand.IsAce() and (self.player.hand.Value(False)>=17 and self.player.hand.Value(False)<=21)):
           soft=0;
        else:
           soft=1;
        str='%d:%d'%(self.player.hand.Value(soft),self.dealer.hand.Value(False))
        return self.hardtable[str]

    '''
    while True:
            hitstand = raw_input( 'Do you want Hit or ' + 
                                 'Stand("h" or "s")? ')
            if hitstand == 'h' or hitstand == 's':
                break
        if hitstand == 'h':
            return True
        else:
            return False
    '''
    def PlayerMoney(self):
        '''Print how much money you have'''
        
        print('You have ' + str(self.player.money) + '$')
        
    def Win(self, string):
        '''Print your bet and your new money'''
        
        print(string)
        print('You win ' + str(self.player.bet) +
              '$, so now you have ' + str(self.player.money) + '$\n')
        
    def Lose(self, string):
        '''Print your bet and your new money'''
        
        print(string)
        print('You lose ' + str(self.player.bet) +
              '$, so now you have '  + str(self.player.money) + '$\n')
    def LoseHalf(self, string):
        '''Print your bet and your new money'''
        
        print(string)
        print('You lose ' + str(self.player.bet*0.5) +
              '$, so now you have '  + str(self.player.money) + '$\n')
        
    def PlayAgain(self):
        ''' '''
        return False;#loop for test
        while True:
            playagain = raw_input('Do you want play again("y" or "n")? ')
            if playagain == 'y':
                return False
            elif playagain == 'n':
                return True
            else:
                print('I don\'t understand')

    def Credits(self):
        '''Thank the player'''
        print('Thank you for playing')
        print('If you have found bugs, ' + 
               'please write to andreaciceri96@gmail.com')
class Game:
    '''
    This class manages the rules of the game
    '''
    def __init__(self):
        self.deck = Deck() #Create the deck
        self.deck.Shuffle(10) #Shuffle the deck 10 times
        self.player = Player(0) #The player has 100$
        self.dealer = Dealer()
        # 11 means double and hit
        self.hardtable = {
        '2:2':1,'2:3':1,'2:4':1,'2:5':1,'2:6':1,'2:7':1,'2:8':1,'2:9':1,'2:10':1,'2:11':1,
        '3:2':1,'3:3':1,'3:4':1,'3:5':1,'3:6':1,'3:7':1,'3:8':1,'3:9':1,'3:10':1,'3:11':1,
        '4:2':1,'4:3':1,'4:4':1,'4:5':1,'4:6':1,'4:7':1,'4:8':1,'4:9':1,'4:10':1,'4:11':1,
        '5:2':1,'5:3':1,'5:4':1,'5:5':1,'5:6':1,'5:7':1,'5:8':1,'5:9':1,'5:10':1,'5:11':1,
        '6:2':1,'6:3':1,'6:4':1,'6:5':1,'6:6':1,'6:7':1,'6:8':1,'6:9':1,'6:10':1,'6:11':1,
        '7:2':1,'7:3':1,'7:4':1,'7:5':1,'7:6':1,'7:7':1,'7:8':1,'7:9':1,'7:10':1,'7:11':1,
        '8:2':1,'8:3':1,'8:4':1,'8:5':1,'8:6':1,'8:7':1,'8:8':1,'8:9':1,'8:10':1,'8:11':1,
        '9:2':1,'9:3':11,'9:4':11,'9:5':11,'9:6':11,'9:7':1,'9:8':1,'9:9':1,'9:10':1,'9:11':1,
        '10:2':11,'10:3':11,'10:4':11,'10:5':11,'10:6':11,'10:7':11,'10:8':11,'10:9':11,'10:10':1,'10:11':1,
        '11:2':11,'11:3':11,'11:4':11,'11:5':11,'11:6':11,'11:7':11,'11:8':11,'11:9':11,'11:10':11,'11:11':1,
        '12:2':1,'12:3':1,'12:4':2,'12:5':2,'12:6':2,'12:7':1,'12:8':1,'12:9':1,'12:10':1,'12:11':1,
        '13:2':2,'13:3':2,'13:4':2,'13:5':2,'13:6':2,'13:7':1,'13:8':1,'13:9':1,'13:10':1,'13:11':21,
        '14:2':2,'14:3':2,'14:4':2,'14:5':2,'14:6':2,'14:7':1,'14:8':1,'14:9':1,'14:10':21,'14:11':21,
        '15:2':2,'15:3':2,'15:4':2,'15:5':2,'15:6':2,'15:7':1,'15:8':1,'15:9':1,'15:10':21,'15:11':21,
        '16:2':2,'16:3':2,'16:4':2,'16:5':2,'16:6':2,'16:7':1,'16:8':1,'16:9':21,'16:10':21,'16:11':22,
        '17:2':2,'17:3':2,'17:4':2,'17:5':2,'17:6':2,'17:7':2,'17:8':2,'17:9':2,'17:10':2,'17:11':2,
        '18:2':2,'18:3':2,'18:4':2,'18:5':2,'18:6':2,'18:7':2,'18:8':2,'18:9':2,'18:10':2,'18:11':2,
        '19:2':2,'19:3':2,'19:4':2,'19:5':2,'19:6':2,'19:7':2,'19:8':2,'19:9':2,'19:10':2,'19:11':2,
        '20:2':2,'20:3':2,'20:4':2,'20:5':2,'20:6':2,'20:7':2,'20:8':2,'20:9':2,'20:10':2,'20:11':2,
        '21:2':2,'21:3':2,'21:4':2,'21:5':2,'21:6':2,'21:7':2,'21:8':2,'21:9':2,'21:10':2,'21:11':2,
}

        self.view = View(self.deck, self.player, self.dealer,self.hardtable)
    def Play(self):
        self.view.PlayerMoney()
        stillplay = True
        round=100000;
        while stillplay: #For every game
            # bet = self.view.AskBet()
            if(len(self.deck.cards)<20):
                self.deck = Deck()
                self.deck.Shuffle(10)
            self.deck.Shuffle(1)
            self.player.Bet() #The player bets
            self.player.hand.Reset() #The player's hand is empty
            self.dealer.hand.Reset() #the dealer's hand is empty
            self.player.Take(self.deck, 1) #The player takes 1 cards
            self.dealer.Take(self.deck, 1) #The dealer takes 1 cards
            self.player.Take(self.deck, 1) #The player takes 1 cards

            self.view.PlayerHand() #Print the player's hand
            self.view.DealerHand() #Print the dealer's hand

            stillhit = True
            double_base = 0;

            if self.player.hand.Value(False) == 21:
                self.player.bet*=1.5;

            while stillhit: #Until the player hits
                hit = self.view.AskHitStand() #Hit or stand?
                if hit==11:
                    if self.player.candouble == True:
                        self.player.bet*=2
                        double_base = 1;
                    hit=1

                if (hit==21 or hit==22):
                    if not self.player.cansurrender:
                        hit-=20;
                    else:
                        hit=0;
                

                
                if hit==1 and double_base!=2:#hit
                    self.player.candouble = False;
                    self.player.cansurrender = False;
                    self.player.Take(self.deck, 1)

                    if(double_base==1):
                        double_base==2;
                    # if self.player.hand.Value(True) == 21 or \
                    #     self.player.hand.Value(False) == 21:
                    #      #If the value's hand is 21(both ace's value)
                         
                    #     self.view.PlayerHand() #Print the player's hand
                    #     self.view.DealerHand() #Print the player's hand

                    #     self.player.Win()
                    #     self.view.Win('You did Black Jack')
                        
                    #     stillhit = False
                    
                    if self.player.hand.Value(True) > 21 and \
                        self.player.hand.Value(False) > 21:
                        #If the value's hand busts(both ace's value)

                        self.view.PlayerHand() #Print the player's hand
                        self.view.DealerHand() #Print the player's hand

                        self.player.Lose()
                        self.view.Lose('You busted')
                        
                        stillhit = False
                    
                elif hit==2:#stand
                    self.dealer.Play(self.deck)
                    #According to the dealer's rule
                    
                    # if self.dealer.hand.Value(True) == 21:
                    #     #If the value of dealer's hand is 21
                        
                    #     self.player.Lose()
                    #     self.view.Lose('The dealer did Blak Jack')

                    self.view.PlayerHand() #Print the player's hand
                    self.view.DealerHand() #Print the player's hand
                    dealerEnd = self.dealer.hand.Value(True) if self.dealer.hand.Value(False)>21 else self.dealer.hand.Value(False);
                    playerEnd = self.player.hand.Value(True) if self.player.hand.Value(False)>21 else self.player.hand.Value(False);

                    if  dealerEnd> 21:
                        #If the value of dealer's hand is more than 21

                        self.player.Win()
                        self.view.Win('The dealer busted')

                    elif  playerEnd> 21:
                        #If the value of dealer's hand is more than 21

                        self.player.Lose()
                        self.view.Win('You are busted')

                        
                    elif dealerEnd>playerEnd:
                        #If the value of dealer's hand is more
                        #than the value of player's hand
                        
                        self.player.Lose()
                        self.view.Lose('The dealer is higher than you')
                        
                    elif dealerEnd==playerEnd:
                        #If the value of dealer's hand and
                        #the value of player's hand are equal
                        
                        # self.player.Lose()
                        # self.view.Lose('The dealer is equeal to you')
                        print 'Dealer Equal Player\n'
                        
                    elif dealerEnd<playerEnd:
                        #If the value of dealer's hand is less
                        #than the value of player's hand
                        
                        self.player.Win()
                        self.view.Win('The dealer is lower than you')

                    stillhit = False
                else:#surrender
                    self.player.LoseHalf()
                    self.view.LoseHalf('You Surrender.')
                    stillhit = False

            self.player.candouble = True;
            self.player.cansurrender = True;
            round-=1;
            if(round==0):
                stillplay=False;
            playagain = self.view.PlayAgain()
            
            if playagain: #If the player don't want play again
                self.view.Credits()
                stillplay = False



if __name__ == "__main__":  
    game = Game()
    game.Play()
