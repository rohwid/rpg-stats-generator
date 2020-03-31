import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d
from scipy.stats import norm

'''
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
'''

import Model as md

colorDB = ["#E74C3C", "#8E44AD", "#3498DB", "#27AE60", "#F39C12", "#707B7C", "#2C3E50"]

def init_plt():
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams.update({'font.size': 12})


def label2DFig(axes, x_name, y_name, padSize, size):
    axes.set_xlabel(x_name, fontsize=size)
    axes.xaxis.labelpad = padSize
    axes.set_ylabel(y_name, fontsize=size)
    axes.yaxis.labelpad = padSize


def label2DPlot(x_name, y_name, padSize, size):
    plt.xlabel(x_name, fontsize=size, labelpad = padSize)
    plt.ylabel(y_name, fontsize=size, labelpad = padSize)


def label3DFig(axes, x_name, y_name, z_name, padSize, size):
    axes.set_xlabel(x_name, fontsize=size)
    axes.xaxis.labelpad = padSize
    axes.set_ylabel(y_name, fontsize=size)
    axes.yaxis.labelpad = padSize
    axes.set_zlabel(z_name, fontsize=size)
    axes.zaxis.labelpad = padSize


def playerHPGraph(hp, level, graphTitle, title):
    init_plt()

    fig = plt.figure()

    # left, button, width, height (range 0 to 1)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot(level, hp, color='#2980B9')

    label2DFig(axes, "Levels", "Player HP", 26, 16)

    if (graphTitle != "" and title != None and title != False):
        axes.set_title(graphTitle, fontsize=20, fontweight='bold')

    plt.show()
    fig.savefig('graph_output_result/PlayerHpDistrib.png')


def playerMPGraph(mp, level, graphTitle, title):
    init_plt()

    fig = plt.figure()

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, button, width, height (range 0 to 1)
    axes.plot(level, mp, color='#2980B9')

    label2DFig(axes, "Levels", "Player MP", 25, 16)

    if (graphTitle != "" and title != None and title != False):
        axes.set_title(graphTitle, fontsize=20, fontweight='bold')

    plt.show()
    fig.savefig('graph_output_result/PlayerMpDistrib.png')


def playerStatsGraph(stats, level, nameStats, graphTitle, title):
    init_plt()

    statsGraph = np.zeros((stats.shape[0], stats.shape[1]))

    for i in range(stats.shape[1]):
        t_statsGraph = 0

        for j in range(stats.shape[0]):
            t_statsGraph = t_statsGraph + stats[j][i]
            statsGraph[j][i] = t_statsGraph

    fig = plt.figure()

    # left, button, width, height (range 0 to 1)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    for i in range(statsGraph.shape[1]):
        axes.plot(level, statsGraph[:,i], label=nameStats[i])

    label2DFig(axes, "Levels", "Player Stats", 25, 16)

    if (graphTitle != "" and title != None and title != False):
        axes.set_title(graphTitle, fontsize=20, fontweight='bold')

    axes.legend()
    plt.show()
    fig.savefig('graph_output_result/PlayerStatsDistrib.png')


def enemyLevelGraph(rangeLevel, graphTitle, title):
    init_plt()

    num_bins = int(max(rangeLevel))
    n, bins, patches = plt.hist(rangeLevel, num_bins, edgecolor='black')

    label2DPlot('Levels', 'Enemy(n)', 25, 16)

    if (graphTitle != "" and title != None and title != False):
        plt.title(graphTitle, fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyLevelDistrib.png')
    plt.show()


def enemyLevelNormDist(rangeLevel, graphTitle, title):
    init_plt()

    mean = md.meanValue(rangeLevel)
    variance = md.varVal(rangeLevel, mean)
    sigma = math.sqrt(variance)

    x = np.linspace(mean - 3 * sigma, mean + 3 * sigma, len(rangeLevel))
    plt.plot(x, norm.pdf(x, mean, sigma))

    label2DPlot('Levels', 'Enemies(n)', 25, 16)

    if (graphTitle != "" and title != None and title != False):
        plt.title(graphTitle, fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyLevelDistribNdist.png')
    plt.show()


def enemyTypeGraph(enemyType, enemiesType, graphTitle, title):
    init_plt()

    name = np.arange(len(enemyType))
    countEnemies = np.zeros(len(enemyType))

    for i in range(len(countEnemies)):
        for j in range(len(enemiesType)):
            if (enemiesType[j] == i):
                countEnemies[i] = countEnemies[i] + 1

    plt.bar(name, countEnemies, color='#2980B9', width=0.5, align='center')
    plt.xticks(name, enemyType, fontsize=12)

    label2DPlot('Types', 'Enemies(n)', 25, 16)

    if (graphTitle != "" and title != None and title != False):
        plt.title('Enemies Type Distribution', fontsize=20, fontweight='bold')

    plt.savefig('graph_output_result/EnemyTypeDistrib.png')
    plt.show()


def enemyWeakGraph(elementName, damageName, weakContainer, graphTitle, title):
    init_plt()

    # set width of bar
    barWidth = 0.25

    # set height of bar
    data = np.zeros((len(damageName), len(elementName)))

    for i in range(len(damageName)):
        for j in range(weakContainer.shape[1]):
            for k in range(weakContainer.shape[0]):
                if (weakContainer[k][j] == i):
                    data[i][j] = data[i][j] + 1

    # Set position of bar on X axis
    r1 = np.arange(len(elementName))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Make the plot
    plt.bar(r1, data[0], color='#2980B9', width=barWidth, edgecolor='white', label='Normal Damage')
    plt.bar(r2, data[1], color='#F39C12', width=barWidth, edgecolor='white', label='Repel (No Damage)')
    plt.bar(r3, data[2], color='#2ECC71', width=barWidth, edgecolor='white', label='Weaknesses')

    # Add xticks on the middle of the group bars
    plt.xticks([r + barWidth for r in range(len(elementName))], elementName)

    label2DPlot('Weaknesses', 'Enemies(n)', 25, 16)

    if (graphTitle != "" and title != None and title != False):
        plt.title(graphTitle, fontsize=20, fontweight='bold')

    # Create legend & Show graphic
    plt.legend()

    plt.savefig('graph_output_result/EnemyWeakDistrib.png')
    plt.show()



def enemyHPGraph(level, enemiesName, hp, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    nameEnemies = np.arange(0, len(enemiesName))
    axes.scatter(level, nameEnemies, hp, color='#2980B9')

    label3DFig(axes, "Levels", "Enemies(n)", "HP", 20, 16)

    if (title != None and title != False):
        axes.set_title("Enemies HP Stats Distribution", fontsize=20, fontweight='bold')

    plt.show()

    fig.savefig('graph_output_result/EnemyHpDistrib.png')


def enemyMPGraph(level, enemiesName, mp, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    nameEnemies = np.arange(0, len(enemiesName))
    axes.scatter(level, nameEnemies, mp, color='#2980B9')

    label3DFig(axes, "Levels", "Enemies(n)", "MP", 20, 16)

    if (title != None and title != False):
        axes.set_title("Enemies MP Stats Distribution", fontsize=20, fontweight='bold')

    plt.show()
    fig.savefig('graph_output_result/EnemyMpDistrib.png')


def enemyStatsGraph(level, enemiesName, statsName, statsContainer, graphTitle, title):
    enemies = np.arange(0, len(enemiesName))

    singleStatsGraph(level, enemiesName, statsName, statsContainer, graphTitle, title)

    for i in range(statsContainer.shape[1]):
        iStatsName = statsName[i]
        iStatsContainer = statsContainer[:, i]
        color = colorDB[i]
        partedEnemyStats(level, enemies, iStatsName, iStatsContainer, color, title)

def singleStatsGraph(level, enemiesName, statsName, statsContainer, graphTitle, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    enemies = np.arange(0, len(enemiesName))

    for i in range(statsContainer.shape[1]):
        axes.scatter(level, enemies, statsContainer[:,i], color = colorDB[i], label=statsName[i])

    label3DFig(axes, "Levels", "Enemies(n)", "Stats", 20, 16)

    if (graphTitle != "" and title != None and title != False):
        axes.set_title(graphTitle, fontsize=20, fontweight='bold')

    axes.legend()
    plt.show()

    fig.savefig('graph_output_result/EnemyStatsDistrib.png')

def partedEnemyStats(level, enemies, statsName, statsContainer, colorSct, title):
    init_plt()

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    axes.scatter(level, enemies, statsContainer, color=colorSct, label=statsName)

    label3DFig(axes, "Levels", "Enemies(n)", "Stats", 20, 16)

    if (title != None and title != False):
        axes.set_title("Enemies " + statsName + " Stats Distribution", fontsize=20, fontweight='bold')

    plt.show()

    saveStatsName = "graph_output_result/Enemy" + statsName + "Distrib"

    fig.savefig(saveStatsName)
