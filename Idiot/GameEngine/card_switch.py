import player


class AbstractCardSwitch:
    def __init__(self, player: player.Player) -> None:
        self.player = player

    def switch(self) -> None:
        while True:
            self.player.show_hand()
            self.player.show_visible_table_cards()
            done, hand_input, table_input = self.get_player_input()
            if done:
                break
            self.switch_cards(hand_input, table_input)

    def switch_cards(self, hand_index, table_index) -> None:
        self.player.hand[hand_index], self.player.table_visible[table_index] = (
            self.player.table_visible[table_index],
            self.player.hand[hand_index],
        )

    def get_player_input(self) -> None:
        pass


class PlayerCardSwitch(AbstractCardSwitch):
    def __init__(self, player: player.Player) -> None:
        super().__init__(player)

    def get_player_input(self) -> None:
        done = False
        valid_hand_input = False
        while not valid_hand_input:
            msg = "Velg hvilken indeks fra hånd: "
            hand_input = input(msg)
            if hand_input.isdigit():
                hand_input = int(hand_input)
                if 0 <= hand_input <= 3:
                    valid_hand_input = True
                else:
                    print("Ikke gyldig input")
            elif hand_input.capitalize() == "N":
                done = True
                return done, None, None

        valid_table_input = False
        while not valid_table_input:
            msg = "Velg indeks fra bordet: "
            table_input = input(msg)
            if table_input.isdigit():
                table_input = int(table_input)
                if 0 <= table_input <= 3:
                    valid_table_input = True
                else:
                    print("Ikke gyldig input")
            elif table_input.capitalize() == "N":
                done = True
                return done, None, None

        return done, hand_input, table_input
