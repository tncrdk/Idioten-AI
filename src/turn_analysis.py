import ast
import math
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np


class TurnAnalysis:
    def __init__(
        self, log_path: str, group_size: int, max_limit: int | None = None
    ) -> None:
        self.log_path = log_path
        self.group_size = group_size
        self.max_limit = max_limit

    def analyze(self, mode):
        if mode == "binomial":
            self.binomial_analysis()
        elif mode == "groups":
            self.groups_analysis()
        else:
            raise Exception("Det er ikke en modus")

    def groups_analysis(self):
        """
        Sjekker om turene er identiske med den statiske agenten
        linje: [runde-nr, spilt kort, spillbare kort, må spille, kort i haugen]
        """
        with open(self.log_path, "r") as f:
            results = []
            finished = False
            i = 0

            while not finished:
                finished, result = self.analyze_group(f)
                results.append(result)
                if self.max_limit:
                    i += 1
                    if i > self.max_limit:
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

    def binomial_analysis(self):
        identical_plays = 0
        total_plays = 0
        results = []

        with open(self.log_path, "r") as f:
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

                if (
                    self.max_limit
                    and (total_plays // self.group_size) >= self.max_limit
                ):
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
        plt.plot(results, label="Enkeltsett")
        plt.plot(
            np.arange(len(results)), [avg * 100] * len(results), label="Gjennomsnitt"
        )

        plt.title("NEAT identisk spillestil med Statisk agent")

        plt.xlabel(f"Antall sett ({self.group_size} trekk i hvert sett)")
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
    pass
