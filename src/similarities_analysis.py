import ast
import math
import csv
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np


class SimilaritiesAnalysis:
    def __init__(
        self, log_path: str, group_size: int, max_limit: int | None = None
    ) -> None:
        self.log_path = log_path
        self.group_size = group_size
        self.max_limit = max_limit

    def analyze(self, mode: str):
        """
        Sjekker om turene er identiske med den statiske agenten
        linje: [runde-nr, spilt kort, spillbare kort, må spille, kort i haugen]
        """
        if mode == "binomial":
            self.binomial_analysis()
        elif mode == "groups":
            self.groups_analysis()
        else:
            raise Exception("Den gitte modus er ikke en modus")
        print("-" * 10)

    def groups_analysis(self):
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
        self.plot_groups_results(results, avg)
        stdev = stats.stdev(results)

        print(f"Gjennomsnitt: {round(avg, 3)}     Stdev: {round(stdev, 10)}")
        file_path = r".\Results\sim_groups_analysis.csv"
        self.save_to_csv_file(file_path, [avg, stdev], ["Avg", "Stdev"])

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
            playlow_move = self.playlowsaving_agent_policy(playable_cards, must_play)

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
                playlow_agent_move = self.playlowsaving_agent_policy(
                    playable_cards, must_play
                )
                if playlow_agent_move == played_card:
                    identical_plays += 1
                total_plays += 1
                results.append((identical_plays / total_plays))
                if (
                    self.max_limit
                    and (total_plays // self.group_size) >= self.max_limit
                ):
                    break

        avg = identical_plays / total_plays
        stdev = math.sqrt(avg * total_plays * (1 - avg))
        stdev_rel = stdev / total_plays

        print(f"Identical plays: {identical_plays}    Avg: {avg}")
        print(f"Stdev: {round(stdev, 2)}   Stdev (rel): {round(stdev_rel, 6)}")

        file_path = r".\Results\sim_binomial_analysis.csv"
        self.save_to_csv_file(
            file_path,
            [identical_plays, avg, stdev, stdev_rel],
            ["Identical plays", "Avg", "Stdev", "Relative Stdev"],
        )
        self.plot_binomial_results(results)

    def playlowsaving_agent_policy(self, playable_cards, must_play) -> int:
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

    def plot_groups_results(self, results, avg):
        results = [100 * x for x in results]
        plt.plot(results, label="Gruppe-verdier")
        plt.plot(
            np.arange(len(results)),
            np.full(len(results), avg * 100),
            label="Gjennomsnitt",
        )

        plt.title("Likhet mellom NEAT-agent og PlaylowSaving-agent")
        plt.xlabel(f"Gruppe-nummer ({self.group_size} trekk i hver gruppe)")
        plt.ylabel("Identisk (%)")
        plt.legend()

        file_path = r".\Plots\sim_binom_{}_{}.png".format(
            self.group_size, self.max_limit
        )
        plt.savefig(file_path)
        plt.clf()

    def plot_binomial_results(self, results):
        results = [100 * x for x in results]
        plt.plot(results, label="Gjennomsnitt")

        plt.title("Likhet mellom NEAT-agent og PlaylowSaving-agent")
        plt.xlabel("Trekk-nummer")
        plt.ylabel("Identisk (%)")
        plt.legend()

        file_path = r".\Plots\sim_groups_{}_{}.png".format(
            self.group_size, self.max_limit
        )
        plt.savefig(file_path)
        plt.clf()

    def save_to_csv_file(self, file_path: str, csv_data: list[int], headers: list[int]):
        with open(file_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            writer.writerow(csv_data)


if __name__ == "__main__":
    pass
