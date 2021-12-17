import deck
import player
import turn
import card_switch as cs
import static_agents as sa


# TODO Lage en resultatliste
# TODO Lage agents


class AbstactGame:
    def __init__(self, deal_cards=True, run_game=True) -> None:
        self.deck = deck.Deck()
        self.pile = deck.Deck(generate_deck=False)
        self.players = []
        self.add_players()
        if deal_cards:
            self.deal_cards()
            if run_game:
                self.run_game()

    """ 
    SETUP 
    """

    def add_players(self):
        pass

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
        pass

    def check_if_game_finished(self):
        playing_players = 0
        for player in self.players:
            if not player.finished:
                playing_players += 1
        if playing_players < 2:
            return True
        return False


class PlayerGame(AbstactGame):
    def __init__(self, deal_cards=True, run_game=True) -> None:
        super().__init__(deal_cards=deal_cards, run_game=run_game)

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

    """
    MAIN GAMEPLAY
    """

    def run_game(self):
        game_finished = False
        standings = []

        for player in self.players:
            input(f"Card switches for {player.name}. ")
            cs.PlayerCardSwitch(player).switch()

        input("Spillet begynner. ")
        while not game_finished:
            for player in self.players:
                if not player.finished:
                    turn.PlayerTurn(player, self.deck, self.pile).play_turn()
                    if player.finished:
                        standings.append(player.name)

                game_finished = self.check_if_game_finished()
                if game_finished:
                    break

        print(standings)
        print("done")


class AgentGame(AbstactGame):
    def __init__(self, deal_cards=True, run_game=True, agents=[]) -> None:
        self.agents = agents
        super().__init__(deal_cards=deal_cards, run_game=run_game)

    def add_players(self):
        if len(self.agents) > 5:
            raise ValueError("For mange spillee")
        elif len(self.agents) < 2:
            raise ValueError("For få spillere")

        for agent in self.agents:
            self.players.append(player.AgentPlayer(agent))
        # bruke super().add_players så spillere kan spille mot agents

    def run_game(self):
        game_finished = False
        standings = []
        burnt_cards = []
        turn_number = 0

        while not game_finished:
            turn_number += 1
            for player in self.players:
                if not player.finished:
                    turn.AgentTurn(
                        player, self.deck, self.pile, burnt_cards
                    ).play_turn()
                    if player.finished:
                        standings.append(player)
                game_finished = self.check_if_game_finished() or turn_number >= 10000
                if game_finished:
                    break
        # if bool(standings):
        #     print(standings[0].policy.name)
        # print(turn_number)
        return standings[0].policy.name
        # gjør noe med belønninger


if __name__ == "__main__":
    agents = [sa.PlayLowAgent1(), sa.PlayHighAgent1()]
    main_game = AgentGame(agents=agents)
    main_game.run_game()
