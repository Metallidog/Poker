from deck import Deck

class Player:
    def __init__(self, name, bankroll):
        self.hand = []
        self.playing = False
        self.bankroll = bankroll
        self.name = name
        self.in_pot = 0
        self.hand_rank = None

    def ante(self, amount):
        self.playing = True
        self.bankroll -= amount
        
    def fold(self):
        self.playing = False

    def display_hand(self):
        for pos, card in enumerate(self.hand, 1):
            print pos, card,
        print
        
    def discard(self, card):
        self.hand.remove(card)

    def draw(self, card):
        self.hand.append(card)

    def rais(self):
        while True:
            r = int(raw_input("Raise how much? "))
            if r<= self.bankroll:
                self.bankroll -= r
                self.in_pot += r
                print 'your bankroll is {}'.format(self.bankroll)
                return r
        
    def call(self, amount):
        match = amount-self.in_pot
        self.bankroll -= match
        print 'your bankroll is {}'.format(self.bankroll)
        self.in_pot += match
        return match

    def bet(self):
        while True:
            b = int(raw_input("Bet how much? "))
            if b<= self.bankroll:
                self.bankroll -= b
                self.in_pot += b
                print 'your bankroll is {}'.format(self.bankroll)
                return b
        print '{} bets {}'.format(self.name, amount)

    def hand_value(self, values):
        print values
        hist={}
        for x in values:
            hist[x] = hist.get(x, 0) + 1
        print hist
        if len(hist)==2:
            self.hand_rank = '4ofakind' if 4 in hist.values() else 'Fullhouse'
        elif len(hist)==3:
            self.hand_rank = '3ofakind' if 3 in hist.values() else '2Pair'
        elif len(hist)==4:
            self.hand_rank = 'Pair'
        elif len(hist)==5:
            self.hand_rank = 'Straight Flush, Flush, Straight, High Card'
        print '{} has a {}'.format(self.name, self.hand_rank)

class FiveCardDraw:
    def __init__(self, *args):
        self.d = Deck()
        self.d.shuffle_deck()
        self.pot_amount = 0
        self.player_list=[names for names in args]
        self.num_players = len(self.player_list)

    def ante(self, amount):
        for player in self.player_list:
            player.ante(amount)
            self.pot(amount)
    
    def deal_to_players(self, player, num_cards):
        for x in range(num_cards):
            player.draw(self.d.deal())
        print player.name
        player.display_hand()
        
    def pot(self, amount):
        self.pot_amount += amount
        print 'pot is {}'.format(self.pot_amount)

    def betting_round(self):
        player_turn, amount, bettor, bet = 0, 0, -1, False
        while True:
            player_turn = player_turn%len(self.player_list)
            options = ['call', 'raise', 'fold'] if bet else ['check', 'bet']
            if bettor != player_turn:
                player = self.player_list[player_turn]
                if player.playing == False:
                    player_turn += 1
                    continue
                print "\n{}. The bet is {} to you. amount is {} in_pot is {} pot_amount is {}\n".format(player.name, amount - player.in_pot, amount, player.in_pot, self.pot_amount)
                dec = raw_input(' '.join(options)+' ')
                if dec not in options:
                    print 'try again'
                    continue
                if dec == 'check':
                    if bettor == -1:
                        bettor = player_turn
                elif dec == 'bet':
                    bettor = player_turn
                    bet = True
                    amount = player.bet()
                    self.pot(amount)
                elif dec == 'raise':                    
                    bettor = player_turn
                    print 'I see your {} and raise.'.format(amount - player.in_pot)
                    self.pot(amount - player.in_pot)
                    player.call(amount)                    
                    r = player.rais()
                    self.pot(r)
                    amount += r
                elif dec == 'call':
                    match = player.call(amount)
                    self.pot(match)
                elif dec == 'fold':
                    player.fold()
                else:
                    continue
                player_turn += 1
            else:
                for player in self.player_list: player.in_pot = 0
                return None
            
    def discard_round(self):
        for player in [p for p in self.player_list if p.playing]:
            print player.name
            player.display_hand()
            num_dis = int(raw_input('how many cards to discard? '))
            for d in range(num_dis):
                card = int(raw_input('what card to discard? '))
                player.discard(player.hand[card-1])
                player.display_hand()
            self.deal_to_players(player, num_dis)

    def hand_values(self):
        for p in self.player_list:
            p.hand_value(sorted([self.d.deck_dict[c]['v'] for c in p.hand], reverse = True))
            
        
    def start_game(self):
        self.ante(5)
        for player in self.player_list:
            self.deal_to_players(player, 5)
        self.hand_values()
        self.betting_round()
        self.discard_round()
        self.betting_round()
        for p in self.player_list:
            if p.playing: print p.name
        self.hand_values()
    
joe = Player('Joe', 100)
sam = Player('Sam', 100)
frank = Player('Frank', 100)
tony = Player('Tony', 100)
game = FiveCardDraw(joe, sam, frank, tony)
game.start_game()

