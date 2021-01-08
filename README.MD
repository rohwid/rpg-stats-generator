# Generate turn-based and action RPG stats

The main purpose of this program is to generate RPG stats or game attributes, it generates with k-NN and Naive Bayes algorithm. The output of the program is `.CSV` files and also represents with graphs.

## Prerequisite

Here are the packages that need to install:

+ python==3.6
+ numpy==1.19.3
+ matplotlib==3.3.3
+ pandas==1.1.5
+ scipy==1.5.4

This comment below uses to install all the required package of this program.

        $ pip install -r requirement.txt

## How to run in Linux or Windows

This comment uses to generate the player stats or gameplay attributes:

        $ python PlayerStats.py

This comment uses to generate the enemy stats or gameplay attributes:

        $ python EnemyStats.py

## Program Content Explanation

This program contain these files and folders:

+ `PlayerStats.py`: The main script or interfaces for generate player stats, override the function if you want make some change or try different algorithm.
+ `PlayerDataContainer.py`: The script which handle all operation include the main algorithm in every function and handle data container management. The data container mean, the process to combine all generated data into player stats.
+ `EnemyStats.py`: The main script or interfaces for generate enemy stats, override the function if you want make some change or try different algorithm.
+ `EnemyDataContainer.py`: The script which handle all operation include the main algorithm in every function and handle data container management. The data container mean, the process to combine all generated data into enemy stats.
+ `Model.py`: Just contain common function or algorithm such as customable round number and etc.
+ `Visualization.py`: The script to create the visualization of the data distribution.
+ `csv_output_result`: The output of the program, all the player and enemy stats as the result of the process with `.CSV` format will be appear here.
+ `graph_output_result`: The visualization of the program's output, all the graphs represents all the player and enemy stats.
