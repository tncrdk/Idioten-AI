import GameEngine.deck as deck
import GameEngine.player as player
import GameEngine.turn as turn


# TODO Lage en resultatliste
# TODO Lage agents


class Game:
    def __init__(self, deal_cards=True) -> None:
        self.deck = deck.Deck()
        self.pile = deck.Deck(generate_deck=False)
        self.players = []
        self.add_players()
        if deal_cards:
            self.deal_cards()

    """ 
    SETUP 
    """

    def add_players(self):
        players_names = (
            input("Skriv inn navnene til spillerne separert med komma. ")
            .replace(" ", "")
            .split(",")
        )
        if len(players_names) > 5:
            raise ValueError("For mange spillee")
        elif len(players_names) < 2:
            raise ValueError("For få spillere")

        for name in players_names:
            self.players.append(player.Player(name))

    def deal_cards(self):
        for player in self.players:
            for _ in range(3):
                player.hand.append(self.deck.pop_top_card())
                player.table_visible.append(self.deck.pop_top_card())
                player.table_hidden.append(self.deck.pop_top_card())
        self.pile.add_card(self.deck.pop_top_card())

    """
    MAIN GAMEPLAY
    """

    def run_game(self):
        game_finished = False
        standings = []

        while not game_finished:
            for player in self.players:
                if not player.finished:
                    turn.Turn(player, self.deck, self.pile).player_turn()
                    if player.finished:
                        standings.append(player.name)

                game_finished = self.check_if_game_finished()
                if game_finished:
                    break

        print(standings)
        print("done")

    def check_if_game_finished(self):
        playing_players = 0
        for player in self.players:
            if not player.finished:
                playing_players += 1
        if playing_players < 2:
            return True
        return False


if __name__ == "__main__":
    main_game = Game()
    main_game.run_game()
