import deck, player

deck = deck.Deck()
p1 = player.Player("a")

p1.hand = deck.cards[-5:]
p1.hand.sort()
for i in p1.hand:
    print(i.value)
