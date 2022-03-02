import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.deck.append(created_card)

    def __str__(self):
        return str([str(card) for card in self.deck])

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        if card.rank == 'Ace':
            self.aces += 1
        self.value += card.value

    def adjust_for_ace(self):
        for card in self.cards:
            if card.rank == 'Ace':
                card.value = 1
                self.value -= 10


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        print(f'You have won {self.bet} chips.')
        self.total += self.bet

    def lose_bet(self):
        print(f'You have lost {self.bet} chips.')
        self.total -= self.bet


def take_bet():
    while True:
        try:
            chips.bet = int(input("Take a bet: "))
            if chips.bet > chips.total:
                print("You don't have enough chips.")
            else:
                return chips.bet
                break
        except:
            print("You have to choose how many chips you want to bet!")


def hit(deck, hand):
    if hand.value > 21 or hand.aces > 2:
        hand.adjust_for_ace()

    return hand.add_card(deck.deal())


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        try:
            choice = input('Hit or stand? Press H or S: ').lower()
            if choice == 'h':
                hit(deck, hand)
                break
            elif choice == 's':
                playing = False
                break
        except:
            print('Choose to Hit or Stand! H or S.')


def show_some(player, dealer):
    print('')
    print('Player\'s cards:')
    for card in player.cards:
        print(card)
    print(f"Player score: {player.value}")
    print('')
    print('Dealer\'s cards: ')
    print(str(dealer.cards[0]) + ', <card hidden> ')
    print(f'Dealer score: {dealer.cards[0].value}')
    print('')


def show_all(player, dealer):
    print('')
    print('Player\'s cards:')
    for card in player.cards:
        print(card)
    print(f'Player score: {player.value}')
    print('')
    print('Dealer\'s cards: ')
    for card in dealer.cards:
        print(card)
    print(f'Dealer score: {dealer.value}')
    print('')


def player_busts():
    chips.lose_bet()
    print('')
    print('Player busted!')
    print('')


def player_wins():
    chips.win_bet()
    print('')
    print('Player won!')
    print('')


def dealer_busts():
    chips.win_bet()
    print('')
    print('Dealer busted!')
    print('')


def dealer_wins():
    chips.lose_bet()
    print('')
    print('Dealer won!')
    print('')


def push():
    print('We\'ve got a tie!'):
    pass


chips = Chips()
while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!')

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()

    for x in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    # Set up the Player's chips
    players_chips = chips

    # Prompt the Player for their bet
    take_bet()

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts()
            playing = True
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value < 21:
        while dealer.value < 17:
            dealer.add_card(deck.deal())

        # Show all cards
        show_all(player, dealer)

    # Run different winning scenarios
    if 21 > player.value > dealer.value:
        player_wins()
    elif player.value == 21:
        player_wins()
    elif dealer.value == 21:
        dealer_wins()
    elif dealer.value > 21:
        dealer_busts()
    elif 21 > dealer.value > player.value:
        dealer_wins()
    elif player.value == dealer.value:
        push()

    # Inform Player of their chips total 
    print(f'You have {players_chips.total} chips.')
    if players_chips.total == 0:
        print('GAME OVER!')
        break
    # Ask to play again
    replay = input('Do you want to play again Y or N? ').lower().startswith('y')
    if not replay:
        playing = True
        print('Thank you for playing!')
        break
