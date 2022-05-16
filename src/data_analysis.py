import math
import ast
import json
import matplotlib.pyplot as plt


class TurnAnalysis:
    def analyze_turns(self, turns_log_path: str, group_size: int):
        """
        Sjekker om turene er identiske med den statiske agenten
        linje: [runde-nr, spilt kort, spillbare kort, må spille, kort i haugen]
        """
        with open(turns_log_path, "r") as f:
            results = []
            finished = False
            i = 0
            while not finished:
                finished, result = self.analyze_group(f, group_size)
                results.append(result)
                i += 1
        self.plot_results(results)
        avg, std = self.analyze_results(results)
        print(f"{avg} +/- {std}")
        return avg, std

    def analyze_group(self, file_object, group_size):
        total_plays = 0
        identical_plays = 0
        finished = False

        for _ in range(group_size):
            data_str = file_object.readline().strip()
            if not data_str:
                finished = True
                break
            datapoint = ast.literal_eval(data_str)

            playable_cards = datapoint[2]
            must_play = datapoint[3]
            played_card = datapoint[1]
            playlow_move = self.get_playlow_move(playable_cards, must_play)

            if playlow_move == played_card:
                identical_plays += 1
            total_plays += 1

        return finished, identical_plays / total_plays

    def analyze_results(self, results: list) -> tuple[int]:
        avg = self.get_average(results)
        std = self.get_std(results, avg)
        return avg, std

    def get_playlow_move(self, playable_cards, must_play) -> int:
        cards_sorted = sorted(playable_cards)
        if must_play:
            for card in cards_sorted:
                if card not in {2, 10}:
                    return card
            return cards_sorted[0]

        for card in cards_sorted:
            if card not in {2, 10}:
                return card

        if len(cards_sorted) > 1:
            return cards_sorted[0]

    def get_std(self, results, avg) -> float:
        var_sum = 0
        pop_size = len(results)
        for i in results:
            var_sum += pow((i - avg), 2)
        return math.sqrt(var_sum / pop_size)

    def get_average(self, results):
        return sum(results) / len(results)

    def plot_results(self, results):
        plt.plot(results)
        plt.show()


class WinRateAnalysis:
    def analyze_groups(self, log_path: str):
        with open(log_path, "r") as f:
            winrates = []
            while True:
                data_str = f.readline().strip()
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins = datapoint["NEAT_V3"]["wins"]
                games = datapoint["NEAT_V3"]["games"]
                winrate = wins / games
                winrates.append(winrate)

        self.plot_winrates(winrates)
        avg = self.get_average(winrates)
        std = self.get_std(winrates, avg)
        print(avg, std)
        return avg, std

    def analyze_binomial(self, log_path):
        wins = 0
        games = 0

        with open(log_path, "r") as f:
            while True:
                data_str = f.readline().strip()
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins += datapoint["NEAT_V3"]["wins"]
                games += datapoint["NEAT_V3"]["games"]

        win_rates = wins / games
        print(win_rates)

    def get_std(self, results, avg):
        var_sum = 0
        pop_size = len(results)
        for i in results:
            var_sum += pow((i - avg), 2)
        return math.sqrt(var_sum / pop_size)

    def get_average(self, results):
        return sum(results) / len(results)

    def plot_winrates(self, winrates):
        plt.plot(winrates)
        plt.show()


if __name__ == "__main__":
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    LOG_WINS_PATH = r".\Log\log_neat_first_results.txt"

    # analyzer = TurnAnalysis()
    # analyzer.analyze_turns(LOG_TURNS_PATH, 10_000)
    win_analyzer = WinRateAnalysis()
    win_analyzer.analyze_groups(LOG_WINS_PATH)
