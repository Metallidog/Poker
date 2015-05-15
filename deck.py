# This comment is for testing Git

from random import shuffle
class Deck:
    def __init__(self):
        self.deck_dict = {}
        self.deck_list = []
        for suite in ('H', 'S', 'C', 'D'):
            for x in range(2, 15):
                if x<10:
                    self.deck_dict['{}{}'.format(x,suite)]={'v':x,'s':suite}
                    self.deck_list.append('{}{}'.format(x,suite))
                else:
                    self.deck_dict['{}{}'.format(['T','J','Q','K','A'][x-10],suite)]={'v':x,'s':suite}
                    self.deck_list.append('{}{}'.format(['T','J','Q','K','A'][x-10],suite))
                    
    def shuffle_deck(self):
        print 'shuffling'
        shuffle(self.deck_list)
    
    def deal(self):
        return self.deck_list.pop(0)


