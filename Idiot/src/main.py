import sys

paths_to_include = [
    r"C:\Users\thorb\Documents\Python\TekForsk\Idioten Prosjekt\Idiot\GameEngine",
    r"C:\Users\thorb\Documents\Python\TekForsk\Idioten Prosjekt\Idiot\Agents\AI_agents",
    r"C:\Users\thorb\Documents\Python\TekForsk\Idioten Prosjekt\Idiot\Agents\Static_agents",
]
sys.path += paths_to_include

import game_engine as ge

game = ge.Game()
