import import_files
import game_engine as ge
import card_switch as cs
import deck
import static_agents as sa
import math
import os


def choose_card(output_data, playable_cards):
    output_data = list(enumerate(output_data))
    output_data.sort(key=lambda x: x[1], reverse=True)

    for index, _ in output_data:
        for i, card in playable_cards:
            if index + 2 == card:
                return card, i


playable_cards = [(0, 3), (1, 6), (2, 8), (3, 9), (4, 9), (5, 9)]
output_data = [1, 2, 3, 4, 4]

print(choose_card(output_data, playable_cards))
