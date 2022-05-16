import ast
import math
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np


class TurnAnalysis:
    def __init__(self, group_size) -> None:
        self.group_size = group_size

    def analyze_turns_in_groups(
        self, turns_log_path: str, max_limit: int | None = None
    ):
        """
        Sjekker om turene er identiske med den statiske agenten
        linje: [runde-nr, spilt kort, spillbare kort, må spille, kort i haugen]
        """
        with open(turns_log_path, "r") as f:
            results = []
            finished = False
            i = 0

            while not finished:
                finished, result = self.analyze_group(f)
                results.append(result)
                if max_limit:
                    i += 1
                    if i > max_limit:
                        break

        avg = np.average(results)
        self.plot_results(results, avg)
        standard_deviation = stats.stdev(results)

        print(
            f"Gjennomsnitt: {round(avg, 3)}     Stdev: {round(standard_deviation, 10)}"
        )
        return avg, standard_deviation

    def analyze_group(self, file_object):
        total_plays = 0
        identical_plays = 0
        finished = False

        for _ in range(self.group_size):
            data_str = file_object.readline().strip()
            if not data_str:
                finished = True
                break
            datapoint = ast.literal_eval(data_str)

            _, played_card, playable_cards, must_play, _ = datapoint
            playlow_move = self.playlow_agent_move(playable_cards, must_play)

            if playlow_move == played_card:
                identical_plays += 1
            total_plays += 1

        return finished, identical_plays / total_plays

    def analyze_turns_binomial(self, log_path: str, max_limit: int | None = None):
        identical_plays = 0
        total_plays = 0
        results = []

        with open(log_path, "r") as f:
            while True:
                data_str = f.readline()
                if not data_str:
                    break

                _, played_card, playable_cards, must_play, _ = ast.literal_eval(
                    data_str
                )
                playlow_move = self.playlow_agent_move(playable_cards, must_play)
                if playlow_move == played_card:
                    identical_plays += 1

                total_plays += 1
                results.append((identical_plays / total_plays))

                if max_limit and total_plays // self.group_size >= max_limit:
                    break

        avg = identical_plays / total_plays
        self.plot_binomial_results(results)
        std = math.sqrt(avg * total_plays * (1 - avg))
        std_rel = std / total_plays

        print(f"Identical plays: {identical_plays}    Avg: {avg}")
        print(f"Stdev: {round(std, 2)}   Stdev (rel): {round(std_rel, 6)}")

    def playlow_agent_move(self, playable_cards, must_play) -> int:
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

    def plot_results(self, results, avg):
        results = [100 * x for x in results]
        plt.plot(results, label="Identisk")
        plt.plot(np.arange(0, len(results)), [avg] * len(results), label="Gjennomsnitt")

        plt.title("NEAT identisk spillestil med Statisk agent")

        plt.xlabel("Antall trekk")
        plt.ylabel("Identisk (%)")

        plt.legend()
        plt.show()

    def plot_binomial_results(self, results):
        results = [100 * x for x in results]
        plt.plot(results, label="Gjennomsnittlig")

        plt.title("NEAT identisk spillestil med Statisk agent")

        plt.xlabel("Antall trekk")
        plt.ylabel("Identisk (%)")

        plt.legend()
        plt.show()


if __name__ == "__main__":
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    LOG_WINS_PATH = r".\Log\log_neat_first_results.txt"

    analyzer = TurnAnalysis(1000)
    analyzer.analyze_turns_binomial(LOG_TURNS_PATH, 2)
