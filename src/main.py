import similarities_analysis as ta
import winrate_analysis as wa


def win_analysis():
    LOG_WINS_PATH = r".\Log\log_neat_first_results.txt"
    MODE = "binomial"

    analyzer = wa.WinrateAnalysis(LOG_WINS_PATH)
    analyzer.neat_analysis(MODE)


def turn_analysis():
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    MODE = "binomial"

    analyzer = ta.SimilaritiesAnalysis(LOG_TURNS_PATH, 1000, 100)
    analyzer.analyze(MODE)


def main():
    win_analysis()
    # turn_analysis()


if __name__ == "__main__":
    main()
