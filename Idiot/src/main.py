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

agents1 = [sa.PlayLowAgent1(), sa.PlayLowAgent1()]
agents2 = [sa.PlayLowSaveAgent1("a"), sa.PlayLowSaveAgent1("b"), sa.PlayLowAgent1("c")]

results = {agents2[0].name: 0, agents2[1].name: 0, agents2[2].name: 0}

for i in range(100):
    main_game = ge.AgentGame(agents=agents2, run_game=False)
    standings = main_game.run_game()
    results[standings] += 1

# main_game = ge.AgentGame(agents=agents2)
print(results)
tot_time = time.time() - start
print(f"Total tid: {tot_time}")
