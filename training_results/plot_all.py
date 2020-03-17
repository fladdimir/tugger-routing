import matplotlib.pyplot as plt
import pandas

base_path = "training_results/_temp_"
suffix = ".monitor.csv"

algorithms = ["ACER", "ACKTR", "DQN", "PPO2"]
episodes = [str(int(3e6)), str(int(1e6))]

plot_col = "finished_products"

random_moves_throughput = 51.2
random_moves_label = "random (avg 100ep)"
lowest_inventory_agent_throughput = 1100
lowest_inventory_agent_label = "lowest_inventory_FTL"

labels = []
algo_column = "Algorithm (episodes)"
final_throughput_column = "Final throughput"
max_throughput_column = "Max throughput"
data_list = []
max_episodes = 0
for algo in algorithms:
    for epi in episodes:
        algo_epi = algo + "_" + epi
        file_path = base_path + algo_epi + suffix
        df = pandas.read_csv(file_path, skiprows=1)
        data = df[plot_col]
        plt.plot(df.index, data)
        labels.append(algo_epi)
        num_episodes = len(data)
        max_episodes = num_episodes if num_episodes > max_episodes else max_episodes
        max_value = max(data)
        final_value = data.iat[-1]
        data_list.append(
            {
                algo_column: algo_epi,
                final_throughput_column: final_value,
                max_throughput_column: max_value,
            }
        )

# append constant values
# lowest inventory heuristics
plt.plot([0, max_episodes], [lowest_inventory_agent_throughput for _ in range(2)])
labels.append(lowest_inventory_agent_label)
data_list.append(
    {
        algo_column: lowest_inventory_agent_label,
        final_throughput_column: lowest_inventory_agent_throughput,
        max_throughput_column: lowest_inventory_agent_throughput,
    }
)
# random moves
plt.plot([0, max_episodes], [random_moves_throughput for _ in range(2)])
labels.append(random_moves_label)
data_list.append(
    {
        algo_column: random_moves_label,
        final_throughput_column: random_moves_throughput,
        max_throughput_column: random_moves_throughput,
    }
)

# show graph
plt.title("Training progress of different RL algorithms [produced products / episode]")
plt.legend(labels, loc=4)
plt.show()

# max throughput
algo_data = pandas.DataFrame(data_list)
algo_data.sort_values(max_throughput_column, ascending=False, inplace=True)
print(algo_data)
algo_data.plot(kind="bar", x=algo_column, y=max_throughput_column)
# plt.show()
