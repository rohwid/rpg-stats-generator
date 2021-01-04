import os
import sys
import math
import numpy as np
import pandas as pd

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
- Anything which contain "show" in the function was used for debug or check the values.
- Every common function set to be more flexible and ready to be "override".
"""

from Model import round_number, split_range
from Visualization import enemy_level_normal_distribution, enemy_stats_graph, enemy_type_graph
from Visualization import enemy_level_graph, enemy_hp_graph, enemy_weak_graph, enemy_mp_graph


class Enemy:
    def __init__(self, enemy_number, max_level):
        self.max_level = max_level
        self.levels_number = 0
        self.range_level = np.array([])
        self.enemy_number = enemy_number
        self.enemy_name = []
        self.enemy_type_name = []
        self.enemy_types = np.array([])
        self.min_hp = 0
        self.min_mp = 0
        self.max_hp = 0
        self.max_mp = 0
        self.range_hp = np.array([])
        self.range_mp = np.array([])
        self.damage_name = []
        self.element_name = []
        self.element_container = np.array([])
        self.stats_name = []
        self.stats_container = np.array([])
        self.main_column = []
        self.data_container = []

    @staticmethod
    def set_column_main(pref, column_name, column_info):
        # Name
        if pref == 0:
            if not column_info:
                column_info = [column_name, 'Level (Auto)', 'HP (AUTO)']

            if column_info[1] != 'Level (Auto)' or column_info[2] != 'HP (Auto)':
                column_info[0] = column_name

        # Levels
        if pref == 1:
            if not column_info:
                column_info = ['Name (Auto)', column_info, 'HP (AUTO)']

            if column_info[0] != 'Name (Auto)' or column_info[2] != 'HP (Auto)':
                column_info[1] = column_name

        # HP
        if pref == 2:
            if not column_info:
                column_info = ['Name (Auto)', 'Level (Auto)', column_info]

            if column_info[0] != 'Name (Auto)' or column_info[1] != 'Level (Auto)':
                column_info[2] = column_name

        # MP
        if pref == 3:
            if len(column_info) == 3:
                column_info.append(column_name)
            else:
                sys.exit('[ERROR] Please define Name, Level and HP first!')

        # Type
        if pref == 4:
            if len(column_info) == 4:
                column_info.append(column_name)
            else:
                sys.exit('[ERROR] Please define Name, Level,  and HP, and MP first!')

        return column_info

    """
    NOTE: THE EXPLANATION ABOUT THE ENEMY NAME WAS DISTRIBUTE HERE!
    This section was created for users to define the name distribution.
    You must override it, if you want different enemy types
    distribution method.
    """

    @staticmethod
    def generate_name(en_name, enemy_number):
        name_enemy_container = [None] * enemy_number

        for i in range(enemy_number):
            name_enemy_container[i] = (en_name + str(i + 1))

        return name_enemy_container

    def range_enemy_name(self, enemy_name, column_name, auto=None):
        if auto == 'yes' or auto == 'YES' or auto == 'Yes':
            self.enemy_name = Enemy.generate_name(enemy_name, self.enemy_number)
        elif auto == 'no' or auto == 'YES' or auto == 'Yes':
            self.enemy_name = enemy_name
        else:
            sys.exit('[ERROR] Wrong "auto" value, can assign name to the enemy!')

        self.main_column = Enemy.set_column_main(0, column_name, self.main_column)

    """
    NOTE: THE EXPLANATION ABOUT THE ENEMY LEVELS WAS DISTRIBUTE HERE!
    This section was created for users to define the levels distribution.
    You must override it, if you want different enemy levels
    distribution method.
    """

    def range_levels(self, min_level, levels_class, column_name, debug=None, scale=0):
        self.levels_number = (self.max_level - min_level) + 1

        # Split levels by levels of class levels
        part_levels = split_range(self.levels_number, levels_class, density=False)

        if debug:
            print('[DEBUG] ~ LEVELS')
            print('[DEBUG] Range LEVEL Distribution:       ', part_levels)

        # Split enemy numbers by class levels
        part_enemy = split_range(self.enemy_number, levels_class, density=False)

        if debug:
            print('[DEBUG] Range ENEMY Distribution:       ', part_enemy)

        self.range_level = np.zeros(self.enemy_number)

        count_level = 1
        count_enemy = 0

        for i in range(len(part_levels)):
            sub_part_levels = split_range(part_levels[i], scale, density=True)
            sub_part_enemy = split_range(part_enemy[i], scale, density=True)

            if debug:
                print('[DEBUG] Range Sub-LEVEL Distribution:   ', sub_part_levels)
                print('[DEBUG] Range Sub-ENEMY Distribution:   ', sub_part_enemy)

            for j in range(len(sub_part_enemy)):
                for k in range(int(sub_part_enemy[j])):
                    if debug:
                        print('[DEBUG] Current Levels:           ', count_level)
                        print('[DEBUG] Current sub_part_levels:  ', sub_part_levels[j])

                    self.range_level[count_enemy] = np.random.randint(count_level, (count_level + sub_part_levels[j]))

                    if debug:
                        print('[DEBUG] Current Enemy:            ', count_enemy)
                        print('[DEBUG] Enemy levels:             ', self.range_level[count_enemy])
                        print('\n')

                    count_enemy = count_enemy + 1

                count_level = count_level + sub_part_levels[i]

        self.range_level.sort()
        self.main_column = Enemy.set_column_main(1, column_name, self.main_column)

    def show_range_levels(self, graph_title, graph=None, title=None, debug=None):
        if debug:
            print('[DEBUG] Range Levels Length: ', len(self.range_level))
            print('[DEBUG] Range Levels: ')
            print(self.range_level)
            print('\n\n')

        enemy_level_graph(self.range_level, graph_title, graph, title)
        enemy_level_normal_distribution(self.range_level, graph_title, graph, title)

    """
    NOTE: THE EXPLANATION ABOUT THE ENEMY TYPE WAS DISTRIBUTE HERE!
    This section was created for users to define the type distribution.
    You must override it, if you want different enemy types
    distribution method.
    """

    def range_enemy_type(self, enemy_type, distribute_percent, column_name, debug=None):
        self.main_column = Enemy.set_column_main(4, column_name, self.main_column)
        self.enemy_type_name = enemy_type

        if len(enemy_type) != len(distribute_percent):
            sys.exit('[ERROR] The dimension of type and percentage distribution not match!')

        # Split levels into type by percentage
        distribute_number = np.zeros(len(enemy_type))

        # Get actual range value from percentage
        for i in range(len(enemy_type)):
            distribute_number[i] = round_number((distribute_percent[i] * len(self.range_level)) / 100)

        # Map or distribute the enemy type
        distribute_level = np.zeros(len(enemy_type))
        rest_distribute_level = np.zeros(len(enemy_type))
        self.enemy_types = np.zeros(self.enemy_number)

        # Check the amount of data
        total_distribute_enemy = 0
        enemy_distribute = np.zeros(len(enemy_type))

        # Distribute the level data
        for i in range(len(enemy_type)):
            temp_enemy_distribute = int(distribute_number[i] / len(distribute_percent))
            distribute_level[i] = temp_enemy_distribute

            # Get the rest of data
            rest_distribute_level[i] = distribute_number[i] % len(distribute_percent)

            # Checking amount of enemy
            for j in range(len(distribute_percent)):
                total_distribute_enemy = total_distribute_enemy + temp_enemy_distribute
                enemy_distribute[j] = enemy_distribute[j] + temp_enemy_distribute

        if debug:
            print('[DEBUG] ~ TYPES')
            print('[DEBUG] ENEMY to distribute: ', enemy_distribute)
            print('[DEBUG] Enemy NUMBERS distribution map (divide to 5 section): ', distribute_number)
            print('[DEBUG] Total Distributed ENEMY: ', total_distribute_enemy)
            print('\n')

            print('[DEBUG] Enemy LEVELS distribution map (divide to 5 section): ', distribute_level)
            print('[DEBUG] Rest of enemy LEVEL distribution: ', rest_distribute_level)
            print('\n')

        # Checking amount of levels
        for i in range(len(distribute_level)):
            if i == 0:
                distribute_level[i] = distribute_level[i]
            else:
                distribute_level[i] = distribute_level[i] + distribute_level[i - 1]

        if debug:
            print('[DEBUG] Range Enemy LEVEL Distribution Map: ', distribute_level)
            print('\n')

        # Initiate data with arrange or generate sequential number (0 - 80)
        shuffle_type = np.arange(1, enemy_distribute[0] + 1)

        # Shuffled the generated number assumed as random
        np.random.shuffle(shuffle_type)

        # Continue and repeat the process above and merge it as one container
        for i in range(len(enemy_type) - 1):
            temp_shuffle_type = np.arange(1, enemy_distribute[0] + 1)
            np.random.shuffle(temp_shuffle_type)

            shuffle_type = np.concatenate((shuffle_type, temp_shuffle_type), axis=None)

        if debug:
            print('[DEBUG] Shuffled Dimension Type Distribution: ', len(shuffle_type))
            print('[DEBUG] Shuffled Type Distribution: ')
            print(shuffle_type)
            print('\n')

        # Set enemy types
        for i in range(len(shuffle_type)):
            for j in range(len(distribute_level)):
                # Check with distribute_level[0]
                if shuffle_type[i] <= distribute_level[0]:
                    self.enemy_types[i] = j
                    break

                # Check with distribute_level[0] and distribute_level[1]
                if distribute_level[j - 1] < shuffle_type[i] <= distribute_level[j]:
                    self.enemy_types[i] = j
                    break

        if debug:
            print('[DEBUG] Range Enemy Type: ')
            print(self.enemy_types)
            print('\n')

        # Handle rest of data
        rest_enemy = len(self.enemy_types) - len(shuffle_type)

        # Set rest of enemy type
        if rest_enemy > 0:
            # Set the index to continue from shuffle_type
            rest_enemy_index = len(shuffle_type)

            for i in range(len(rest_distribute_level)):
                if rest_distribute_level[i] > 0:
                    for j in range(int(rest_distribute_level[i])):
                        # Continue to assign the rest
                        self.enemy_types[rest_enemy_index] = i
                        rest_enemy_index = rest_enemy_index + 1

    def show_range_enemy_type(self, graph_title, graph=None, title=None, debug=None):
        if debug:
            print('[DEBUG] Range Enemy Type Dimension: ', self.enemy_types.shape)
            print('[DEBUG] Range Enemy Type: ')
            print(self.enemy_types)
            print('\n\n')

        enemy_type_graph(self.enemy_type_name, self.enemy_types, graph_title, graph, title)

    def range_health_points(self, min_hp, max_hp, column_name):
        self.main_column = Enemy.set_column_main(2, column_name, self.main_column)
        self.min_hp = min_hp
        self.max_hp = max_hp

    def range_magic_points(self, min_mp, max_mp, column_name):
        self.main_column = Enemy.set_column_main(3, column_name, self.main_column)
        self.min_mp = min_mp
        self.max_mp = max_mp

    """
    NOTE: THE EXPLANATION ABOUT THE ENEMY WEAKNESSES WAS DISTRIBUTE HERE!
    This section was created for users to define the weaknesses distribution.
    You must override it, if you want different enemy weaknesses
    distribution method.
    """

    def range_element_weak(self, element_name, damage_name):
        self.element_name = element_name
        self.damage_name = damage_name
        self.element_container = np.zeros((self.enemy_number, len(element_name)))

        # Set the damage affected was 3 per enemy
        # Operate between the number 1 (Repel), 2 (Weak)
        # And 0 (Normal) set as default number
        damage_number = np.zeros(len(damage_name) - 1)

        for i in range(len(self.element_container)):
            count_dmg_index = len(damage_name)
            damage_number[0] = np.random.randint(0, len(damage_name) + 1)
            count_dmg_index = count_dmg_index - damage_number[0]

            if count_dmg_index > 0:
                for j in range(len(damage_number) - 1):
                    if count_dmg_index <= 0:
                        break

                    damage_number[j + 1] = np.random.randint(0, count_dmg_index)
                    count_dmg_index = count_dmg_index - damage_number[j + 1]
            else:
                for j in range(len(damage_number) - 1):
                    damage_number[j + 1] = len(damage_name) - damage_number[0]

            set_damage = np.zeros(len(element_name))

            for j in range(len(damage_number)):
                if damage_number[j] != 0:
                    rand_set_damage = 0

                    while rand_set_damage < damage_number[j]:
                        index = np.random.randint(0, len(set_damage))

                        if set_damage[index] == 0:
                            set_damage[index] = j + 1
                            rand_set_damage = rand_set_damage + 1

            self.element_container[i] = set_damage

    def show_element_weak(self, graph_title, graph=None, title=None, debug=None):
        if debug:
            print('[DEBUG] ~ WEAKNESSES')

        if not self.element_name:
            if debug:
                print('[DEBUG] The game is not using Element of Weaknesses.\n')
                print('\n\n')
        else:
            if debug:
                print('[DEBUG] List of characters elements: ', self.element_name)
                print('[DEBUG] List of characters elements stats: ')
                print(self.element_container)
                print('\n\n')

            enemy_weak_graph(
                self.element_name,
                self.damage_name,
                self.element_container,
                graph_title,
                graph,
                title
            )

    """
    NOTE: THE EXPLANATION ABOUT THE ENEMY STATS WAS DISTRIBUTE HERE!
    This section was created for users to define the stats distribution.
    You must override it, if you want different stats distribution method.
    """

    def range_stats(self, stats_name, basic_min_stats, basic_max_stats, debug=None):
        self.stats_name = stats_name
        self.range_hp = np.zeros(len(self.enemy_types))
        self.range_mp = np.zeros(len(self.enemy_types))
        self.stats_container = np.zeros((len(self.enemy_types), len(stats_name)))

        for i in range(len(self.enemy_types)):
            # Mixed
            if self.enemy_types[i] == 0:
                mix_type = np.random.randint(1, 3)

                # MP Focused
                if mix_type == 1:
                    bot_limit_hp = self.min_hp
                    top_limit_hp = bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                    if debug:
                        print('Mixed(MP) Top HP:     ', top_limit_hp)

                    self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                    bot_limit_mp = self.min_mp
                    top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                    if debug:
                        print('Mixed(MP) Top MP:     ', top_limit_mp)

                    self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                    # Stats Correction
                    if self.range_hp[i] >= self.range_mp[i]:
                        bot_limit_mp = self.range_hp[i]
                        top_limit_mp = bot_limit_mp + self.range_hp[i] + 10
                        self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                    for j in range(self.stats_container.shape[1]):
                        bot_limit_st = basic_min_stats[j]
                        top_limit_st = bot_limit_st + math.ceil(
                            (self.range_level[i] / 100) * basic_max_stats[j])  # ceil (avoid out of range)
                        self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                    # Stats Correction
                    if self.stats_container[i][2] >= self.stats_container[i][1]:
                        bot_limit_st = self.stats_container[i][2]
                        top_limit_st = bot_limit_st + 10
                        self.stats_container[i][1] = np.random.randint(bot_limit_st, top_limit_st)

                # HP Focused
                if mix_type == 2:
                    bot_limit_hp = self.min_hp
                    top_limit_hp = bot_limit_hp + bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                    if debug:
                        print('Mixed(HP) Top HP:     ', top_limit_hp)

                    self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                    bot_limit_mp = self.min_mp
                    top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                    if debug:
                        print('Mixed(HP) Top MP:     ', top_limit_mp)

                    self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                    # Stats Correction
                    if self.range_mp[i] >= self.range_hp[i]:
                        bot_limit_hp = self.range_mp[i]
                        top_limit_hp = bot_limit_hp + 10
                        self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                    for j in range(self.stats_container.shape[1]):
                        bot_limit_st = basic_min_stats[j]
                        top_limit_st = bot_limit_st + math.ceil(
                            (self.range_level[i] / 100) * basic_max_stats[j]
                        )  # ceil (avoid out of range)

                        self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                    # Stats Correction
                    if self.stats_container[i][1] >= self.stats_container[i][2]:
                        bot_limit_st = self.stats_container[i][1]
                        top_limit_st = bot_limit_st + self.stats_container[i][1] + 10
                        self.stats_container[i][2] = np.random.randint(bot_limit_st, top_limit_st)

            # Hard Magic
            if self.enemy_types[i] == 1:
                bot_limit_hp = self.min_hp
                top_limit_hp = bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                if debug:
                    print('Hard Magic Top HP:    ', top_limit_hp)

                self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                bot_limit_mp = self.min_mp
                top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                if debug:
                    print('Hard Magic Top MP:    ', top_limit_mp)

                self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                # Stats Correction
                if self.range_hp[i] >= self.range_mp[i]:
                    bot_limit_mp = self.range_hp[i] + 100
                    top_limit_mp = bot_limit_mp + 200
                    self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                for j in range(self.stats_container.shape[1]):
                    bot_limit_st = basic_min_stats[j]

                    # ceil (avoid out of range)
                    top_limit_st = bot_limit_st + math.ceil(
                        (self.range_level[i] / 100) * basic_max_stats[j]
                    )

                    self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                # Stats Correction
                if self.stats_container[i][2] - self.stats_container[i][1] <= 10:
                    if self.stats_container[i][2] > self.stats_container[i][1]:
                        bot_limit_st = self.stats_container[i][2]
                        top_limit_st = bot_limit_st + 10
                    else:
                        bot_limit_st = self.stats_container[i][1]
                        top_limit_st = bot_limit_st + 10

                    self.stats_container[i][2] = np.random.randint(bot_limit_st, top_limit_st)

            # Soft Magic
            if self.enemy_types[i] == 2:
                bot_limit_hp = self.min_hp
                top_limit_hp = bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                if debug:
                    print('Soft Magic Top HP:    ', top_limit_hp)

                self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                bot_limit_mp = self.min_mp
                top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                if debug:
                    print('Soft Magic Top MP:    ', top_limit_mp)

                self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                # Stats Correction
                if self.range_hp[i] >= self.range_mp[i]:
                    bot_limit_mp = self.range_hp[i]
                    top_limit_mp = bot_limit_mp + 10
                    self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                for j in range(self.stats_container.shape[1]):
                    bot_limit_st = basic_min_stats[j]
                    top_limit_st = bot_limit_st + math.ceil((self.range_level[i] / 100) * basic_max_stats[j])
                    self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                # Stats Correction
                if self.stats_container[i][1] >= self.stats_container[i][2]:
                    bot_limit_st = basic_min_stats[1]
                    top_limit_st = bot_limit_st + 10
                    self.stats_container[i][2] = np.random.randint(bot_limit_st, top_limit_st)

            # Hard Strength
            if self.enemy_types[i] == 3:
                bot_limit_hp = self.min_hp
                top_limit_hp = bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                if debug:
                    print('Hard Strength Top HP: ', top_limit_hp)

                self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                bot_limit_mp = self.min_mp
                top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                if debug:
                    print('Hard Strength Top MP: ', top_limit_mp)

                self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                # Stats Correction
                if self.range_mp[i] >= self.range_hp[i]:
                    bot_limit_hp = self.range_mp[i] + 100
                    top_limit_hp = bot_limit_hp + 200
                    self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                for j in range(self.stats_container.shape[1]):
                    bot_limit_st = basic_min_stats[j]

                    # ceil (avoid out of range)
                    top_limit_st = bot_limit_st + math.ceil(
                        (self.range_level[i] / 100) * basic_max_stats[j]
                    )

                    self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                # Stats Correction
                if self.stats_container[i][1] - self.stats_container[i][2] <= 10:
                    if self.stats_container[i][1] > self.stats_container[i][2]:
                        bot_limit_st = self.stats_container[i][1]
                        top_limit_st = bot_limit_st + 10
                    else:
                        bot_limit_st = self.stats_container[i][2]
                        top_limit_st = bot_limit_st + 10

                    self.stats_container[i][1] = np.random.randint(bot_limit_st, top_limit_st)

            # Soft Strength
            if self.enemy_types[i] == 4:
                bot_limit_hp = self.min_hp
                top_limit_hp = bot_limit_hp + round_number((self.range_level[i] / 100) * self.max_hp)

                if debug:
                    print('Soft Strength Top HP: ', top_limit_hp)

                self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                bot_limit_mp = self.min_mp
                top_limit_mp = bot_limit_mp + round_number((self.range_level[i] / 100) * self.max_mp)

                if debug:
                    print('Soft Strength Top MP: ', top_limit_mp)

                self.range_mp[i] = np.random.randint(bot_limit_mp, top_limit_mp)

                # Stats Correction
                if self.range_mp[i] >= self.range_hp[i]:
                    bot_limit_hp = self.range_mp[i]
                    top_limit_hp = bot_limit_hp + 10
                    self.range_hp[i] = np.random.randint(bot_limit_hp, top_limit_hp)

                for j in range(self.stats_container.shape[1]):
                    bot_limit_st = basic_min_stats[j]

                    # ceil (avoid out of range)
                    top_limit_st = bot_limit_st + math.ceil(
                        (self.range_level[i] / 100) * basic_max_stats[j]
                    )

                    self.stats_container[i][j] = np.random.randint(bot_limit_st, top_limit_st)

                # Stats Correction
                if self.stats_container[i][2] >= self.stats_container[i][1]:
                    bot_limit_st = basic_min_stats[2]
                    top_limit_st = bot_limit_st + 10
                    self.stats_container[i][1] = np.random.randint(bot_limit_st, top_limit_st)

    def show_range_stats(self, graph_title, graph=None, title=None, debug=None):
        if debug:
            print('[DEBUG] ~ STATS')
            print('[DEBUG] Range Enemy Stats Dimension: ', self.stats_container.shape)
            print('[DEBUG] Range Enemy Stats: ')
            print(self.stats_container)
            print('\n\n')

        enemy_hp_graph(self.range_level, self.enemy_name, self.range_hp, graph, title)
        enemy_mp_graph(self.range_level, self.enemy_name, self.range_mp, graph, title)

        enemy_stats_graph(
            self.range_level,
            self.enemy_name,
            self.stats_name,
            self.stats_container,
            graph_title,
            graph,
            title
        )

    @staticmethod
    def set_name_container(data_container, column_info, enemy_number, enemy_name):
        if data_container[column_info[0]].shape[0] == enemy_number:
            data_container[column_info[0]] = enemy_name
            return data_container
        else:
            sys.exit('[ERROR] The list of names not match with the rows of data container!')

    @staticmethod
    def set_level_container(data_container, column_info, enemy_number, range_level):
        if data_container[column_info[1]].shape[0] == enemy_number:
            data_container[column_info[1]] = range_level
            return data_container
        else:
            sys.exit('[ERROR] The levels not match with the rows of data container!')

    @staticmethod
    def set_hp_container(data_container, column_info, enemy_number, range_hp):
        if data_container[column_info[2]].shape[0] == enemy_number:
            data_container[column_info[2]] = range_hp
            return data_container
        else:
            sys.exit('[ERROR] The HP\'s rows not match with the rows of data container!')

    @staticmethod
    def set_mp_container(data_container, column_info, enemy_number, range_mp):
        if data_container[column_info[3]].shape[0] == enemy_number:
            data_container[column_info[3]] = range_mp
            return data_container
        else:
            sys.exit('[ERROR] The MP\'s rows not match with the rows of data container!')

    @staticmethod
    def set_type_container(data_container, column_info, enemy_number, range_types):
        if data_container[column_info[4]].shape[0] == enemy_number:
            data_container[column_info[4]] = range_types
            return data_container
        else:
            sys.exit('[ERROR] The MP\'s rows not match with the rows of data container!')

    @staticmethod
    def set_element_container(data_container, init_column, column_info, enemy_number, element_container):
        if element_container.shape[0] == enemy_number:

            # With MP (Usually Turn-based)
            if len(init_column) == 6:
                for i in range(element_container.shape[1]):
                    data_container[column_info[6 + i]] = element_container[:, i]

            # Without MP (Usually Action)
            else:
                for i in range(element_container.shape[1]):
                    data_container[column_info[5 + i]] = element_container[:, i]

            return data_container
        else:
            sys.exit('[ERROR] The Element\'s rows not match with the rows of data container!')

    @staticmethod
    def set_stats(data_container, init_column, column_info, enemies_number, stats_container):
        if stats_container.shape[0] == enemies_number:

            # Without Element (Usually Action)
            if len(init_column) == 6:
                len_element_container = column_info.shape[0] - (len(init_column) + stats_container.shape[1])

                for i in range(stats_container.shape[1]):
                    data_container[column_info[len(init_column) + len_element_container + i]] = stats_container[:, i]

            # Without MP and Element (Usually Action)
            elif len(init_column) == 5:
                len_element_container = column_info.shape[0] - (len(init_column) + stats_container.shape[1])

                for i in range(stats_container.shape[1]):
                    data_container[column_info[len(init_column) + len_element_container + i]] = stats_container[:, i]

            # Others
            else:
                for i in range(stats_container.shape[1]):
                    data_container[column_info.shape[2 + i]] = stats_container[:, i]

            return data_container
        else:
            sys.exit('[ERROR] The Stats\'s rows not match with the rows of data container!')

    def generate_enemy(self):
        row_number = np.arange((self.enemy_number - (self.enemy_number - 1)), self.enemy_number + 1)
        init_column = self.main_column

        if self.range_mp.size == 0:
            if not self.element_name:
                column_info = np.concatenate((init_column, self.stats_name), axis=None)

                self.data_container = pd.DataFrame(0, row_number[:], column_info[:])

                self.data_container = Enemy.set_name_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.enemy_name
                )

                self.data_container = Enemy.set_level_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.range_level
                )

                self.data_container = Enemy.set_hp_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.range_hp
                )

                self.data_container = Enemy.set_type_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.enemy_types
                )

                self.data_container = Enemy.set_stats(
                    self.data_container,
                    init_column,
                    column_info,
                    self.enemy_number,
                    self.stats_container
                )

            else:
                column_info = np.concatenate((init_column, self.element_name, self.stats_name), axis=None)

                self.data_container = pd.DataFrame(0, row_number[:], column_info[:])

                self.data_container = Enemy.set_name_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.enemy_name
                )

                self.data_container = Enemy.set_level_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.range_level
                )

                self.data_container = Enemy.set_hp_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.range_hp
                )

                self.data_container = Enemy.set_type_container(
                    self.data_container,
                    column_info,
                    self.enemy_number,
                    self.enemy_types
                )

                self.data_container = Enemy.set_element_container(
                    self.data_container,
                    init_column,
                    column_info,
                    self.enemy_number,
                    self.element_container
                )

                self.data_container = Enemy.set_stats(
                    self.data_container,
                    init_column,
                    column_info,
                    self.enemy_number,
                    self.stats_container
                )

        elif not self.element_name:
            column_info = np.concatenate((init_column, self.stats_name), axis=None)

            self.data_container = pd.DataFrame(0, row_number[:], column_info[:])

            self.data_container = Enemy.set_name_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.enemy_name
            )

            self.data_container = Enemy.set_level_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_level
            )

            self.data_container = Enemy.set_hp_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_hp
            )

            self.data_container = Enemy.set_mp_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_mp
            )

            self.data_container = Enemy.set_type_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.enemy_types
            )

            self.data_container = Enemy.set_stats(
                self.data_container,
                init_column,
                column_info,
                self.enemy_number,
                self.stats_container
            )

        else:
            column_info = np.concatenate((init_column, self.element_name, self.stats_name), axis=None)

            self.data_container = pd.DataFrame(0, row_number[:], column_info[:])

            self.data_container = Enemy.set_name_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.enemy_name
            )

            self.data_container = Enemy.set_level_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_level
            )

            self.data_container = Enemy.set_hp_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_hp
            )

            self.data_container = Enemy.set_mp_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.range_mp
            )

            self.data_container = Enemy.set_type_container(
                self.data_container,
                column_info,
                self.enemy_number,
                self.enemy_types
            )

            self.data_container = Enemy.set_element_container(
                self.data_container,
                init_column,
                column_info,
                self.enemy_number,
                self.element_container
            )

            self.data_container = Enemy.set_stats(
                self.data_container,
                init_column,
                column_info,
                self.enemy_number,
                self.stats_container
            )

        pd.set_option('display.max_rows', 400)

        print('[RESULT] All Enemy Stats: \n')
        print(self.data_container)

        current_work_dir = os.path.dirname(os.path.abspath(__file__))

        self.data_container.to_csv(current_work_dir + '/csv_output_result/EnemyStats.csv', index=True)
