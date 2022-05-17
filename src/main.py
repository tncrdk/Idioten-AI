import turn_analysis as ta
import winrate_analysis as wa


def win_analysis():
    LOG_WINS_PATH = r".\Log\log_neat_first_results.txt"
    MODE = "binomial"

    analyzer = wa.WinRateAnalysis()
    analyzer.analyze(LOG_WINS_PATH, MODE)


def turn_analysis():
    LOG_TURNS_PATH = r".\Log\log_turns.txt"
    MODE = "binomial"

    analyzer = ta.TurnAnalysis(LOG_TURNS_PATH, 1000, 100)
    analyzer.analyze(MODE)


def main():
    win_analysis()
    turn_analysis()


if __name__ == "__main__":
    main()
