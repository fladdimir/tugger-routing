import sys

sys.path.append(".")
from tugger_src.rl.stable_baselines.base import plot

# manually choose which file to plot

FILE_PATH = "training_results/_temp_ACKTR_1000000.monitor.csv"
COLUMN = "finished_products"

if __name__ == "__main__":
    plot(FILE_PATH, column=COLUMN)
