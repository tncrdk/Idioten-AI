import import_files
import game_engine as ge
import card_switch as cs
import deck
import static_agents as sa
import json
import numpy as np
import pandas as pd

l = [[[1, 2, 3], [4, 5, 6]], [[1, 2, 34], [4564, 456]]]

a = np.array(l)
with open("test.json", "w") as f:
    json.dump(l, f)
    json.dump(l, f)
    print(l)


# with open("test.json", "r") as f:
#     data = json.load(f)
#     print(data)
