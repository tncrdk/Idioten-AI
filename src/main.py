import similarities_analysis as ta
import winrate_analysis as wa


def win_analysis():
    binomial = "binomial"
    groups = "groups"
    neat_vs_PlayLowSaving_log_path = r".\Log\log_neat_vs_PlayLowSaving.txt"
    PlayLowSaving_vs_NEAT_log_path = r".\Log\log_PlayLowSaving_vs_NEAT.txt"

    analyzer = wa.WinrateAnalysis()
    analyzer.neat_analysis(
        neat_vs_PlayLowSaving_log_path, binomial, "NEAT", "PlaylowSaving"
    )
    analyzer.neat_analysis(
        PlayLowSaving_vs_NEAT_log_path, binomial, "PlayLowSaving", "NEAT"
    )
    analyzer.neat_analysis(
        neat_vs_PlayLowSaving_log_path, groups, "NEAT", "PlaylowSaving"
    )
    analyzer.neat_analysis(
        PlayLowSaving_vs_NEAT_log_path, groups, "PlayLowSaving", "NEAT"
    )


def similarities_analysis():
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    MODE = "binomial"

    analyzer = ta.SimilaritiesAnalysis(LOG_TURNS_PATH, 1000, 100)
    analyzer.analyze(MODE)


def main():
    win_analysis()
    print("-" * 10)
    similarities_analysis()


if __name__ == "__main__":
    main()
