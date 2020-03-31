# Generate turn-based and action RPG stats

The main purpose of this program is to generate turn-based and action RPG stats, it generated with k-NN and Naive Bayes algorithm. This program contain:

+ `PlayerStats.py`: This is the main script or interfaces for generate player stats, override the function if you want make some change or try different algorithm.
+ `EnemyStats.py`: This is the main script or interfaces for generate enemy stats, override the function if you want make some change or try different algorithm.
+ `DataContainer.py`: The script which handle all operation include the main algorithm in every function and handle data container management. The data container mean, the process to combine all generated data into one or stats.
+ `Model.py`: Just contain common function or algorithm such as customable round number and etc.
+ `Visualization.py`: The script to create the visualization of the data distribution. If you want visualize the new data, just write the new function in this file.

This project still on going and didn't finish yet ;)
