import similarities_analysis as ta
import winrate_analysis as wa


def win_analysis():
    binomial = "binomial"
    groups = "groups"

    NEAT_vs_PlayLowSaving = r".\Log\log_neat_vs_PlayLowSaving.txt"
    PlayLowSaving_vs_NEAT = r".\Log\log_PlayLowSaving_vs_NEAT.txt"

    NEAT_vs_PlayLow = r".\Log\log_NEAT_vs_PlayLow.txt"
    PlayLow_vs_NEAT = r".\Log\log_PlayLow_vs_NEAT.txt"

    PlayHigh_vs_NEAT = r".\Log\log_PlayHigh_vs_NEAT.txt"

    id_PlayLowSaving = r".\Log\log_id_PlayLowSaving.txt"

    analyzer = wa.WinrateAnalysis()

    analyzer.neat_analysis(NEAT_vs_PlayLowSaving, binomial, "NEAT", "PlaylowSaving")
    analyzer.neat_analysis(NEAT_vs_PlayLowSaving, groups, "NEAT", "PlaylowSaving")
    analyzer.neat_analysis(PlayLowSaving_vs_NEAT, binomial, "PlayLowSaving", "NEAT")
    analyzer.neat_analysis(PlayLowSaving_vs_NEAT, groups, "PlayLowSaving", "NEAT")

    analyzer.neat_analysis(NEAT_vs_PlayLow, binomial, "NEAT", "Playlow")
    analyzer.neat_analysis(NEAT_vs_PlayLow, groups, "NEAT", "Playlow")
    analyzer.neat_analysis(PlayLow_vs_NEAT, binomial, "PlayLow", "NEAT")
    analyzer.neat_analysis(PlayLow_vs_NEAT, groups, "PlayLow", "NEAT")

    analyzer.neat_analysis(PlayHigh_vs_NEAT, binomial, "PlayHigh", "NEAT")
    analyzer.neat_analysis(PlayHigh_vs_NEAT, groups, "PlayHigh", "NEAT")

    analyzer.identical_agents_analysis(id_PlayLowSaving, binomial, "PlayLowSaving")
    analyzer.identical_agents_analysis(id_PlayLowSaving, groups, "PlayLowSaving")


def similarities_analysis():
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    MODE = "binomial"

    analyzer = ta.SimilaritiesAnalysis(LOG_TURNS_PATH, group_size=100, max_limit=100)
    analyzer.analyze(MODE)


def main():
    win_analysis()
    print("-" * 10)
    print("Similarities")
    similarities_analysis()


if __name__ == "__main__":
    main()
