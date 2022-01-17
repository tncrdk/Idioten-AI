import import_files
import game_engine as ge
import static_agents as sa
import time
import pickle
import neat
import os
import NEAT_agent as na

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


def create_NEAT_agent(config_path, genome_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    network = neat.nn.FeedForwardNetwork.create(genome, config)
    agent = na.NEAT_Agent2(genome, network)
    return agent


genome_path = "winner7.pkl"
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, r"Config-files\config2.txt")

neat_agent = create_NEAT_agent(config_path, genome_path)


agents1 = [sa.PlayLowAgent1(), sa.PlayLowAgent1()]
agents2 = [neat_agent, sa.PlayLowSaveAgent1("b")]

results = {agents2[0].name: 0, agents2[1].name: 0}
games = 10000
tot_turns = 0

start_time = time.time()

for i in range(games):
    main_game = ge.AgentGame(agents=agents2, run_game=False)
    standings, turns = main_game.run_game()
    if bool(standings):
        results[standings.name] += 1
    tot_turns += turns

tot_time = time.time() - start_time

print(results[agents2[0].name] / games)
print(results[agents2[1].name] / games)
print(tot_turns / games)
print(f"Total tid: {tot_time}")
