import import_files
import game_engine as ge
import static_agents as sa
import time

"""
data = {
    "hand_cards": [...],
    "playable_cards": [...],
    "table_cards": [...],
    "pile": [...],
    "played_cards": [...],
    "burnt_cards": [...],
}
"""
start = time.time()

agents = [sa.PlayLowAgent1(), sa.PlayLowAgent1()]

for i in range(1000):
    main_game = ge.AgentGame(agents=agents)

tot_time = time.time() - start
print(f"Total tid: {tot_time}")
