import similarities_analysis as ta
import winrate_analysis as wa


def win_analysis():
    binomial = "binomial"
    groups = "groups"
    neat_first_PlayLowSaving_log_path = r".\Log\log_neat_first_results.txt"
    static_first_PlayLowSaving_log_path = r".\Log\log_static_first_results.txt"

    analyzer = wa.WinrateAnalysis()
    analyzer.neat_analysis(neat_first_PlayLowSaving_log_path, binomial, "NEAT")
    # analyzer.neat_analysis(
    #     static_first_PlayLowSaving_log_path, binomial, "PlayLowSaving"
    # )
    # analyzer.neat_analysis(neat_first_PlayLowSaving_log_path, groups, "NEAT")
    # analyzer.neat_analysis(static_first_PlayLowSaving_log_path, groups, "PlayLowSaving")


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
