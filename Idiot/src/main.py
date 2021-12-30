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
agents2 = [sa.RandomAgent("a"), sa.PlayLowSaveAgent1("b")]

results = {agents2[0].name: 0, agents2[1].name: 0}
games = 100
tot_turns = 0

for i in range(games):
    main_game = ge.AgentGame(agents=agents2, run_game=False)
    standings, turns = main_game.run_game()
    results[standings.name] += 1
    tot_turns += turns

# main_game = ge.AgentGame(agents=agents2)
print(results[agents2[0].name] / games)
print(results[agents2[1].name] / games)
print(tot_turns / games)

tot_time = time.time() - start
print(f"Total tid: {tot_time}")
