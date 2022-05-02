import import_files
import game_engine as ge
import card_switch as cs
import deck
import static_agents as sa
import math
import os

# def choose_card(output_data, playable_cards):
#     data = [(value, index) for index, value in enumerate(output_data)]
#     data.sort(reverse=True)

#     for _, index in data:
#         for i, value in playable_cards:
#             if index + 2 == value:
#                 return i, value


# playable_cards = [(0, 3), (1, 6), (2, 8), (3, 9), (4, 9), (5, 9)]
# output_data = [1, 2, 3, 4, 4]

# print(choose_card(output_data, playable_cards))
local_dir = os.path.dirname(__file__)
file_path = os.path.join(local_dir, "Winners\ehh.txt")
# with open(file_path, "w") as f:
#     f.write("Hallo")
#     f.close()
print(file_path)
