import player
import deck


class CardSwitch:
    def __init__(self, player: player.Player) -> None:
        self.player = player

    def switch(self) -> None:
        done = False

        while not done:
            self.player.show_hand()
            self.player.show_visible_table_cards()
