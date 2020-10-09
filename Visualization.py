import math
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm

"""
STATS GENERATOR FOR TURN BASED OR ACTION RPG (ROLE PLAYING GAMES)
By: ROHMAN WIDIYANTO
GitHub: http://github.com/rohwid/

All component or object defined separately, here's the reason:
- Levels: Because sometimes the characters won't start from 1st level.
- Magic Point: Because sometimes the games doesn't need it (ex: action RPG).
- Number of Weaknesses: Same reason with Magic Point.
- Generate data container: Generate data container dynamically.

Notes:
- Anything which contain "show" in the function was used for debug or
  check the values.
"""

from Model import var_val, mean_values

colorDB = ["#E74C3C", "#8E44AD", "#3498DB", "#27AE60", "#F39C12", "#707B7C", "#2C3E50"]


def init_plt():
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams.update({'font.size': 12})


def label_2d_fig(axes, x_name, y_name, pad_size, size):
    axes.set_xlabel(x_name, fontsize=size)
    axes.xaxis.labelpad = pad_size
    axes.set_ylabel(y_name, fontsize=size)
    axes.yaxis.labelpad = pad_size


def label_2d_plot(x_name, y_name, pad_size, size):
    plt.xlabel(x_name, fontsize=size, labelpad=pad_size)
    plt.ylabel(y_name, fontsize=size, labelpad=pad_size)


def label_3d_fig(axes, x_name, y_name, z_name, pad_size, size):
    axes.set_xlabel(x_name, fontsize=size)
    axes.xaxis.labelpad = pad_size
    axes.set_ylabel(y_name, fontsize=size)
    axes.yaxis.labelpad = pad_size
    axes.set_zlabel(z_name, fontsize=size)
    axes.zaxis.labelpad = pad_size


def player_hp_graph(hp, level, graph_title, graph, title):
    init_plt()

    fig = plt.figure()

    # left, button, width, height (range 0 to 1)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot(level, hp, color='#2980B9')

    label_2d_fig(axes, "Levels", "Player HP", 26, 16)

    if graph_title != "" and title is not None and title:
        axes.set_title(graph_title, fontsize=20, fontweight='bold')

    fig.savefig('graph_output_result/PlayerHpDistribution.png')

    if graph:
        plt.show()


def player_mp_graph(mp, level, graph_title, graph, title):
    init_plt()

    fig = plt.figure()

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # left, button, width, height (range 0 to 1)
    axes.plot(level, mp, color='#2980B9')

    label_2d_fig(axes, "Levels", "Player MP", 25, 16)

    if graph_title != "" and title is not None and title:
        axes.set_title(graph_title, fontsize=20, fontweight='bold')

    fig.savefig('graph_output_result/PlayerMpDistribution.png')

    if graph:
        plt.show()


def player_stats_graph(stats, level, name_stats, graph_title, graph, title):
    init_plt()

    stats_graph = np.zeros((stats.shape[0], stats.shape[1]))

    for i in range(stats.shape[1]):
        temp_stats_graph = 0

        for j in range(stats.shape[0]):
            temp_stats_graph = temp_stats_graph + stats[j][i]
            stats_graph[j][i] = temp_stats_graph

    fig = plt.figure()

    # left, button, width, height (range 0 to 1)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    for i in range(stats_graph.shape[1]):
        axes.plot(level, stats_graph[:, i], label=name_stats[i])

    label_2d_fig(axes, "Levels", "Player Stats", 25, 16)

    if graph_title != "" and title is not None and title:
        axes.set_title(graph_title, fontsize=20, fontweight='bold')

    axes.legend()
    fig.savefig('graph_output_result/PlayerStatsDistribution.png')

    if graph:
        plt.show()


def enemy_level_graph(range_level, graph_title, graph, title):
    init_plt()

    num_bins = int(max(range_level))
    plt.hist(range_level, num_bins, edgecolor='black')

    label_2d_plot('Levels', 'Enemy(n)', 25, 16)

    if graph_title != "" and title is not None and title:
        plt.title(graph_title, fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyLevelDistribution.png')

    if graph:
        plt.show()


def enemy_level_normal_distribution(range_level, graph_title, graph, title):
    init_plt()

    mean = mean_values(range_level)
    variance = var_val(range_level, mean)
    sigma = math.sqrt(variance)

    x = np.linspace(mean - 3 * sigma, mean + 3 * sigma, len(range_level))
    plt.plot(x, norm.pdf(x, mean, sigma))

    label_2d_plot('Levels', 'Enemies(n)', 25, 16)

    if graph_title != "" and title is not None and title:
        plt.title(graph_title, fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyLevelDistributionNormal.png')

    if graph:
        plt.show()


def enemy_type_graph(enemy_type, enemies_type, graph_title, graph, title):
    init_plt()

    name = np.arange(len(enemy_type))
    count_enemies = np.zeros(len(enemy_type))

    for i in range(len(count_enemies)):
        for j in range(len(enemies_type)):
            if enemies_type[j] == i:
                count_enemies[i] = count_enemies[i] + 1

    plt.bar(name, count_enemies, color='#2980B9', width=0.5, align='center')
    plt.xticks(name, enemy_type, fontsize=12)

    label_2d_plot('Types', 'Enemies(n)', 25, 16)

    if graph_title != "" and title is not None and title:
        plt.title('Enemies Type Distribution', fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyTypeDistribution.png')

    if graph:
        plt.show()


def enemy_weak_graph(element_name, damage_name, weak_container, graph_title, graph, title):
    init_plt()

    # set width of bar
    bar_width = 0.25

    # set height of bar
    data = np.zeros((len(damage_name), len(element_name)))

    for i in range(len(damage_name)):
        for j in range(weak_container.shape[1]):
            for k in range(weak_container.shape[0]):
                if weak_container[k][j] == i:
                    data[i][j] = data[i][j] + 1

    # Set position of bar on X axis
    r1 = np.arange(len(element_name))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Make the plot
    plt.bar(r1, data[0], color='#2980B9', width=bar_width, edgecolor='white', label='Normal Damage')
    plt.bar(r2, data[1], color='#F39C12', width=bar_width, edgecolor='white', label='Repel (No Damage)')
    plt.bar(r3, data[2], color='#2ECC71', width=bar_width, edgecolor='white', label='Weaknesses')

    # Add xticks on the middle of the group bars
    plt.xticks([r + bar_width for r in range(len(element_name))], element_name)

    label_2d_plot('Weaknesses', 'Enemies(n)', 25, 16)

    if graph_title != "" and title is not None and title:
        plt.title(graph_title, fontsize=20, fontweight='bold')

    # Create legend & Show graphic
    plt.legend()

    plt.savefig('graph_output_result/EnemyWeakDistribution.png')

    if graph:
        plt.show()


def enemy_hp_graph(level, enemy_name, hp, graph, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    name_enemies = np.arange(0, len(enemy_name))
    axes.scatter(level, name_enemies, hp, color='#2980B9')

    label_3d_fig(axes, "Levels", "Enemies(n)", "HP", 20, 16)

    if title is not None and title:
        axes.set_title("Enemies HP Stats Distribution", fontsize=20, fontweight='bold')

    fig.savefig('graph_output_result/EnemyHpDistribution.png')

    if graph:
        plt.show()


def enemy_mp_graph(level, enemy_name, mp, graph, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    name_enemies = np.arange(0, len(enemy_name))
    axes.scatter(level, name_enemies, mp, color='#2980B9')

    label_3d_fig(axes, "Levels", "Enemies(n)", "MP", 20, 16)

    if title is not None and title:
        axes.set_title("Enemies MP Stats Distribution", fontsize=20, fontweight='bold')

    fig.savefig('graph_output_result/EnemyMpDistribution.png')

    if graph:
        plt.show()


def enemy_stats_graph(level, enemy_name, stats_name, stats_container, graph_title, graph, title):
    enemies = np.arange(0, len(enemy_name))

    single_stats_graph(level, enemy_name, stats_name, stats_container, graph_title, graph, title)

    for i in range(stats_container.shape[1]):
        i_stats_name = stats_name[i]
        i_stats_container = stats_container[:, i]
        color = colorDB[i]
        parted_enemy_stats(level, enemies, i_stats_name, i_stats_container, color, graph, title)


def single_stats_graph(level, enemies_name, stats_name, stats_container, graph_title, graph, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    enemies = np.arange(0, len(enemies_name))

    for i in range(stats_container.shape[1]):
        axes.scatter(level, enemies, stats_container[:, i], color=colorDB[i], label=stats_name[i])

    label_3d_fig(axes, "Levels", "Enemies(n)", "Stats", 20, 16)

    if graph_title != "" and title is not None and title:
        axes.set_title(graph_title, fontsize=20, fontweight='bold')

    axes.legend()

    fig.savefig('graph_output_result/EnemyStatsDistribute.png')

    if graph:
        plt.show()


def parted_enemy_stats(level, enemies, stats_name, stats_container, selected_color, graph, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    axes.scatter(level, enemies, stats_container, color=selected_color, label=stats_name)

    label_3d_fig(axes, "Levels", "Enemies(n)", "Stats", 20, 16)

    if title is not None and title:
        axes.set_title("Enemies " + stats_name + " Stats Distribution", fontsize=20, fontweight='bold')

    save_stats_name = "graph_output_result/Enemy" + stats_name + "Distribute"
    fig.savefig(save_stats_name)

    if graph:
        plt.show()
