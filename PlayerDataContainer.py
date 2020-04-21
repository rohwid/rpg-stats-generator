import sys
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

import Visualization as Vis


class Player:
    def __init__(self, max_level):
        self.max_level = max_level
        self.start_level = 0
        self.range_level = np.array([])
        self.range_hp = np.array([])
        self.range_mp = np.array([])
        self.name_element = []
        self.element_container = np.array([])
        self.name_stats = np.array([])
        self.stats_container = np.array([])
        self.main_column = np.array([])
        self.data_container = np.array([])

    @staticmethod
    def set_column_main(pref, column_name, column_info):
        if pref == 0:
            if not column_info:
                column_info = [column_name, 'HP(Auto)']

            if column_info[1] != 'HP(Auto)':
                column_info[0] = column_name

        if pref == 1:
            if not column_info:
                column_info = ['Levels (Auto)', column_info]

            if column_info[0] != 'Level(Auto)':
                column_info[1] = column_name

        if pref == 2:
            if len(column_info) == 2:
                column_info.append(column_name)
            else:
                sys.exit("[ERROR] Please define HP and Level first!")

        return column_info

    def range_levels(self, start_level, column_name):
        self.start_level = start_level
        self.range_level = np.arange(1, (self.max_level - start_level) + 2)

        self.main_column = Player.set_column_main(0, column_name, self.main_column)

    def show_range_levels(self):
        print("[DEBUG] ~ LEVELS")
        print("[DEBUG] Range Levels: ")
        print(self.range_level)
        print("\n\n")

    def range_health_points(self, start_hp, second_hp, column_name):
        self.range_hp = np.arange(start_hp, start_hp + (self.max_level * (second_hp - start_hp)),
                                  second_hp - start_hp)

        self.main_column = Player.set_column_main(1, column_name, self.main_column)

    def show_range_health_points(self, graph_title, title=None):
        print("[DEBUG] ~ NAMES")
        print("[DEBUG] Range HP: ")
        print(self.range_hp)

        Vis.player_hp_graph(self.range_level, self.range_hp, graph_title, title)
        print("\n\n")

    def range_magic_points(self, start_mp, second_mp, column_name):
        self.range_mp = np.arange(start_mp, start_mp + (self.max_level * (second_mp - start_mp)),
                                  second_mp - start_mp)

        self.main_column = Player.set_column_main(2, column_name, self.main_column)

    def show_range_magic_points(self, graph_title, title=None):
        print("[DEBUG] ~ MP")
        print("[DEBUG] Range MP: ")
        print(self.range_mp)

        Vis.player_mp_graph(self.range_level, self.range_mp, graph_title, title)

        print("\n\n")

    def range_element_weak(self, name_element, char_weak_number):
        self.name_element = name_element

        for i in range(len(char_weak_number)):
            if char_weak_number[i] == 2:
                if self.element_container.all:
                    self.element_container = np.full((self.max_level, 1), 2)
                else:
                    self.element_container = np.concatenate((self.element_container,
                                                             np.full((self.max_level, 1), 2)), axis=1)

            if char_weak_number[i] == 1:
                if self.element_container.all:
                    self.element_container = np.ones((self.max_level, 1))
                else:
                    self.element_container = np.concatenate((self.element_container,
                                                             np.ones((self.max_level, 1))), axis=1)

            if char_weak_number[i] == 0:
                if self.element_container.all:
                    self.element_container = np.zeros((self.max_level, 1))
                else:
                    self.element_container = np.concatenate((self.element_container,
                                                             np.zeros((self.max_level, 1))), axis=1)

    def show_element_weak(self):
        print("[DEBUG] ~ WEAKNESSES")
        print("[DEBUG] List of characters elements: ", self.name_element)
        print("[DEBUG] List of characters elements stats: ")
        print(self.element_container)

        print("\n\n")

    def range_stats(self, name_stats, stats_max_value, stats_to_assign):
        self.name_stats = name_stats
        self.stats_container = np.zeros((self.max_level, len(stats_max_value)))

        distribute_limit = np.zeros((len(stats_to_assign), len(stats_max_value)))

        for i in range(len(stats_max_value)):
            limit_cache = np.zeros(len(stats_to_assign))
            check_limit = 0

            for j in range(len(stats_to_assign)):
                for k in range(len(stats_to_assign)):
                    check_limit = check_limit + limit_cache[k]

                if check_limit > stats_max_value[i]:
                    break

                if check_limit == 0:
                    limit = int(stats_max_value[i] / stats_to_assign[j])
                    distribute_limit[j][i] = np.random.randint(0, limit + 1)
                    limit_cache[j] = distribute_limit[j][i] * stats_to_assign[j]
                else:
                    if (len(stats_to_assign) - j) == 1:
                        distribute_limit[j][i] = stats_max_value[i] - check_limit
                        limit_cache[j] = distribute_limit[j][i] * stats_to_assign[j]
                    else:
                        limit = int((stats_max_value[i] - check_limit) / stats_to_assign[j])
                        distribute_limit[j][i] = np.random.randint(0, limit + 1)
                        limit_cache[j] = distribute_limit[j][i] * stats_to_assign[j]

        # Assign all stats data to container
        for i in range(len(stats_max_value)):
            last_stats = 0

            for j in range(len(stats_to_assign)):
                for k in range(int(distribute_limit[j][i])):
                    if last_stats == 0:
                        self.stats_container[k][i] = stats_to_assign[j]
                    else:
                        self.stats_container[last_stats + k][i] = stats_to_assign[j]

                    if distribute_limit[j][i] - k == 1:
                        last_stats = k + 1

        # Shuffle the stats
        for i in range(len(stats_max_value)):
            np.random.shuffle(self.stats_container[:, i])

    def show_range_stats(self, graph_title, title=None):
        print("[DEBUG] ~ STATS")
        print("List of characters stats: ")
        print(self.stats_container)

        Vis.player_stats_graph(self.stats_container, self.range_level, self.name_stats, graph_title, title)

        print("\n\n")

    @staticmethod
    def set_level_container(data_container, column_info, max_level, range_level):
        if data_container[column_info[0]].shape[0] == max_level:
            data_container[column_info[0]] = range_level
            return data_container
        else:
            sys.exit("[ERROR] The levels not match with the rows of data container!")

    @staticmethod
    def set_hp_container(data_container, column_info, max_level, range_hp):
        if data_container[column_info[1]].shape[0] == max_level:
            data_container[column_info[1]] = range_hp

            return data_container
        else:
            sys.exit("[ERROR] The HP's rows not match with the rows of data container!")

    @staticmethod
    def set_mp_container(data_container, column_info, max_level, range_mp):
        if data_container[column_info[2]].shape[0] == max_level:
            data_container[column_info[2]] = range_mp
            return data_container
        else:
            sys.exit("[ERROR] The MP's rows not match with the rows of data container!")

    @staticmethod
    def set_element_container(data_container, init_column, column_info, max_level, element_container):
        if element_container.shape[0] == max_level:

            # With MP (Usually Turn-based)
            if len(init_column) == 3:
                for i in range(element_container.shape[1]):
                    data_container[column_info[3 + i]] = element_container[:, i]

            # Without MP (Usually Action)
            else:
                for i in range(element_container.shape[1]):
                    data_container[column_info[2 + i]] = element_container[:, i]

            return data_container
        else:
            sys.exit("[ERROR] The Element's rows not match with the rows of data container!")

    @staticmethod
    def set_stats(data_container, init_column, column_info, max_level, stats_container):
        if stats_container.shape[0] == max_level:
            # Without Element (Usually Action)
            if len(init_column) == 3:
                len_element_container = column_info.shape[0] - (len(init_column) + stats_container.shape[1])

                for i in range(stats_container.shape[1]):
                    data_container[column_info[len(init_column) + len_element_container + i]] = stats_container[:, i]

            # Without MP and Element (Usually Action)
            elif len(init_column) == 2:
                len_element_container = column_info.shape[0] - (len(init_column) + stats_container.shape[1])

                for i in range(stats_container.shape[1]):
                    data_container[column_info[len(init_column) + len_element_container + i]] = stats_container[:, i]

            # Others
            else:
                for i in range(stats_container.shape[1]):
                    data_container[column_info.shape[2 + i]] = stats_container[:, i]

            return data_container
        else:
            sys.exit("[ERROR] The Stats's rows not match with the rows of data container!")

    def generate_stats(self):
        row_level = np.arange((self.max_level - (self.max_level - self.start_level)), self.max_level + 1)
        init_column = self.main_column

        if self.range_mp.all:
            if self.name_element:
                column_info = np.concatenate((init_column, self.name_stats), axis=None)

                self.data_container = pd.DataFrame(0, row_level[:], column_info[:])
                self.data_container = Player.set_level_container(self.data_container, column_info, self.max_level,
                                                                 self.range_level)
                self.data_container = Player.set_hp_container(self.data_container, column_info, self.max_level,
                                                              self.range_hp)
                self.data_container = Player.set_stats(self.data_container, init_column, column_info,
                                                       self.max_level, self.stats_container)
            else:
                column_info = np.concatenate((init_column, self.name_element, self.name_stats), axis=None)

                self.data_container = pd.DataFrame(0, row_level[:], column_info[:])
                self.data_container = Player.set_level_container(self.data_container, column_info, self.max_level,
                                                                 self.range_level)
                self.data_container = Player.set_hp_container(self.data_container, column_info, self.max_level,
                                                              self.range_hp)
                self.data_container = Player.set_element_container(self.data_container, init_column, column_info,
                                                                   self.max_level, self.element_container)
                self.data_container = Player.set_stats(self.data_container, init_column, column_info,
                                                       self.max_level, self.stats_container)
        elif not self.name_element:
            column_info = np.concatenate((init_column, self.name_stats), axis=None)

            self.data_container = pd.DataFrame(0, row_level[:], column_info[:])
            self.data_container = Player.set_level_container(self.data_container, column_info, self.max_level,
                                                             self.range_level)
            self.data_container = Player.set_hp_container(self.data_container, column_info, self.max_level,
                                                          self.range_hp)
            self.data_container = Player.set_mp_container(self.data_container, column_info, self.max_level,
                                                          self.range_mp)
            self.data_container = Player.set_stats(self.data_container, init_column, column_info,
                                                   self.max_level, self.stats_container)
        else:
            column_info = np.concatenate((init_column, self.name_element, self.name_stats), axis=None)

            self.data_container = pd.DataFrame(0, row_level[:], column_info[:])
            self.data_container = Player.set_level_container(self.data_container, column_info, self.max_level,
                                                             self.range_level)
            self.data_container = Player.set_hp_container(self.data_container, column_info, self.max_level,
                                                          self.range_hp)
            self.data_container = Player.set_mp_container(self.data_container, column_info, self.max_level,
                                                          self.range_mp)
            self.data_container = Player.set_element_container(self.data_container, init_column, column_info,
                                                               self.max_level, self.element_container)
            self.data_container = Player.set_stats(self.data_container, init_column, column_info,
                                                   self.max_level, self.stats_container)

        pd.set_option('display.max_rows', 200)

        print("[RESULT] All Player Character Stats: \n")
        print(self.data_container)

        print("\n[DEBUG] Current TOTAL STATS: ", self.stats_container.sum(axis=0), "\n")

        self.data_container.to_csv('csv_output_result/PlayerStats.csv', index=True)
