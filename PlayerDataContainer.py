import sys

import numpy as np
import pandas as pd

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
- Anything which contain "show" in the function was used for debug or check the values.
- Every common function set to be more flexible and ready to be "override".
'''

import Visualization as Vs


class Player:
    def __init__(self, max_level):
        self.maxLevel = max_level
        self.startLevel = 0
        self.rangeLevel = []
        self.rangeHP = []
        self.rangeMP = []
        self.nameElement = []
        self.elementContainer = []
        self.nameStats = []
        self.statsContainer = []
        self.mainColumn = []
        self.dataContainer = []

    @staticmethod
    def set_column_main(pref, column_name, column_info):
        if pref == 0:
            if column_info == []:
                column_info = [column_name, 'HP(Auto)']

            if column_info[1] != 'HP(Auto)':
                column_info[0] = column_name

        if pref == 1:
            if column_info == []:
                column_info = ['Levels (Auto)', column_info]

            if column_info[0] != 'Level(Auto)':
                column_info[1] = column_name

        if (pref == 2):
            if (len(column_info) == 2):
                column_info.append(column_name)
            else:
                sys.exit("[ERROR] Please define HP and Level first!")

        return column_info

    "Levels"

    def rangeLevels(self, startLevel, columnName):
        self.startLevel = startLevel
        self.rangeLevel = np.arange(1, (self.maxLevel - startLevel) + 2)

        self.mainColumn = Player.set_column_main(columnName, self.mainColumn)

    def showRangeLevels(self):
        print("[DEBUG] ~ LEVELS")
        print("[DEBUG] Range Levels: ")
        print(self.rangeLevel)
        print("\n\n")

    "Health Points"

    def rangeHealtPoints(self, startHP, secondHP, columnName):
        self.rangeHP = np.arange(startHP, startHP + (self.maxLevel * (secondHP - startHP)), secondHP - startHP)

        self.mainColumn = Player.set_column_main(columnName, self.mainColumn)

    def showRangeHealtPoints(self, graphTitle, title=None):
        print("[DEBUG] ~ NAMES")
        print("[DEBUG] Range HP: ")
        print(self.rangeHP)

        Vs.playerHPGraph(self.rangeLevel, self.rangeHP, graphTitle, title)

        print("\n\n")

    "Magic Points"

    def rangeMagicPoints(self, startMP, secondMP, columnName):
        self.rangeMP = np.arange(startMP, startMP + (self.maxLevel * (secondMP - startMP)), secondMP - startMP)

        self.mainColumn = Player.set_column_main(columnName, self.mainColumn)

    def showRangeMagicPoints(self, graphTitle, title=None):
        print("[DEBUG] ~ MP")

        if (self.rangeMP == []):
            print("[DEBUG] The game is not using MP.")
        else:
            print("[DEBUG] Range MP: ")
            print(self.rangeMP)

            Vs.playerMPGraph(self.rangeLevel, self.rangeMP, graphTitle, title)

        print("\n\n")

    "Element Weaknesses"

    def rangeElementWeak(self, nameElement, charWeakNumber):
        self.nameElement = nameElement

        for i in range(len(charWeakNumber)):
            if (charWeakNumber[i] == 2):
                if (self.elementContainer == []):
                    self.elementContainer = np.full((self.maxLevel, 1), 2)
                else:
                    self.elementContainer = np.concatenate((self.elementContainer, np.full((self.maxLevel, 1), 2)),
                                                           axis=1)

            if (charWeakNumber[i] == 1):
                if (self.elementContainer == []):
                    self.elementContainer = np.ones((self.maxLevel, 1))
                else:
                    self.elementContainer = np.concatenate((self.elementContainer, np.ones((self.maxLevel, 1))), axis=1)

            if (charWeakNumber[i] == 0):
                tempContnr = np.zeros((self.maxLevel, 1))
                if (self.elementContainer == []):
                    self.elementContainer = np.zeros((self.maxLevel, 1))
                else:
                    self.elementContainer = np.concatenate((self.elementContainer, np.zeros((self.maxLevel, 1))),
                                                           axis=1)

    def showElmntWeak(self):
        print("[DEBUG] ~ WEAKNESSES")

        if (self.nameElement == []):
            print("[DEBUG] The game is not using Element of Weaknesses.")
        else:
            print("[DEBUG] List of characters elements: ", self.nameElement)
            print("[DEBUG] List of characters elements stats: ")
            print(self.elementContainer)

        print("\n\n")

    "Player Stats"

    def rangeStats(self, nameStats, statsMaxValue, statsToAssign):
        self.nameStats = nameStats
        self.statsContainer = np.zeros((self.maxLevel, len(statsMaxValue)))

        distribLimit = np.zeros((len(statsToAssign), len(statsMaxValue)))

        for i in range(len(statsMaxValue)):
            limitCache = np.zeros(len(statsToAssign))
            checkLimit = 0

            for j in range(len(statsToAssign)):
                for k in range(len(statsToAssign)):
                    checkLimit = checkLimit + limitCache[k]

                if (checkLimit > statsMaxValue[i]):
                    break

                if (checkLimit == 0):
                    limit = int(statsMaxValue[i] / statsToAssign[j])
                    distribLimit[j][i] = np.random.randint(0, limit + 1)
                    limitCache[j] = distribLimit[j][i] * statsToAssign[j]
                else:
                    if ((len(statsToAssign) - j) == 1):
                        distribLimit[j][i] = statsMaxValue[i] - checkLimit
                        limitCache[j] = distribLimit[j][i] * statsToAssign[j]
                    else:
                        limit = int((statsMaxValue[i] - checkLimit) / statsToAssign[j])
                        distribLimit[j][i] = np.random.randint(0, limit + 1)
                        limitCache[j] = distribLimit[j][i] * statsToAssign[j]

        # Assign all stats data to container
        for i in range(len(statsMaxValue)):
            lastStats = 0

            for j in range(len(statsToAssign)):
                for k in range(int(distribLimit[j][i])):
                    if (lastStats == 0):
                        self.statsContainer[k][i] = statsToAssign[j]
                    else:
                        self.statsContainer[lastStats + k][i] = statsToAssign[j]

                    if (distribLimit[j][i] - k == 1):
                        lastStats = k + 1

        # Shuffle the stats
        for i in range(len(statsMaxValue)):
            np.random.shuffle(self.statsContainer[:, i])

    def showRangeStats(self, graphTitle, title=None):
        print("[DEBUG] ~ STATS")
        print("List of characters stats: ")
        print(self.statsContainer)

        Vs.playerStatsGraph(self.statsContainer, self.rangeLevel, self.nameStats, graphTitle, title)

        print("\n\n")

    "All Player Stats Container"

    def setLvContnr(dataContainer, columnInfo, maxLevel, rangeLevel):
        if (dataContainer[columnInfo[0]].shape[0] == maxLevel):
            dataContainer[columnInfo[0]] = rangeLevel
            return dataContainer
        else:
            sys.exit("[ERROR] The levels not match with the rows of data container!")

    def setHPContnr(dataContainer, columnInfo, maxLevel, rangeHP):
        if (dataContainer[columnInfo[1]].shape[0] == maxLevel):
            dataContainer[columnInfo[1]] = rangeHP

            return dataContainer
        else:
            sys.exit("[ERROR] The HP's rows not match with the rows of data container!")

    def setMPContnr(dataContainer, columnInfo, maxLevel, rangeMP):
        if (dataContainer[columnInfo[2]].shape[0] == maxLevel):
            dataContainer[columnInfo[2]] = rangeMP
            return dataContainer
        else:
            sys.exit("[ERROR] The MP's rows not match with the rows of data container!")

    def setElContnr(dataContainer, initColumn, columnInfo, maxLevel, elementContainer):
        if (elementContainer.shape[0] == maxLevel):
            # With MP (Usually Turn-based)
            if (len(initColumn) == 3):
                for i in range(elementContainer.shape[1]):
                    dataContainer[columnInfo[3 + i]] = elementContainer[:, i]
            # Without MP (Usually Action)
            else:
                for i in range(elementContainer.shape[1]):
                    dataContainer[columnInfo[2 + i]] = elementContainer[:, i]

            return dataContainer
        else:
            sys.exit("[ERROR] The Element's rows not match with the rows of data container!")

    def setStats(dataContainer, initColumn, columnInfo, maxLevel, statsContainer):
        if (statsContainer.shape[0] == maxLevel):
            # Without Element (Usually Action)
            if (len(initColumn) == 3):
                lenElContnr = columnInfo.shape[0] - (len(initColumn) + statsContainer.shape[1])

                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo[len(initColumn) + lenElContnr + i]] = statsContainer[:, i]

            # Without MP and Element (Usually Action)
            elif (len(initColumn) == 2):
                lenElContnr = columnInfo.shape[0] - (len(initColumn) + statsContainer.shape[1])

                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo[len(initColumn) + lenElContnr + i]] = statsContainer[:, i]

            # Others
            else:
                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo.shape[2 + i]] = statsContainer[:, i]

            return dataContainer
        else:
            sys.exit("[ERROR] The Stats's rows not match with the rows of data container!")

    def genStats(self):
        rowLvl = np.arange((self.maxLevel - (self.maxLevel - self.startLevel)), self.maxLevel + 1)
        initColumn = self.mainColumn

        if (self.rangeMP == []):
            if (self.nameElement == []):
                columnInfo = np.concatenate((initColumn, self.nameStats), axis=None)
                self.dataContainer = pd.DataFrame(0, rowLvl, columnInfo)
                self.dataContainer = Player.setLvContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeLevel)
                self.dataContainer = Player.setHPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeHP)
                self.dataContainer = Player.setStats(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                     self.statsContainer)
            else:
                columnInfo = np.concatenate((initColumn, self.nmElment, self.nameStats), axis=None)
                self.dataContainer = pd.DataFrame(0, rowLvl, columnInfo)
                self.dataContainer = Player.setLvContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeLevel)
                self.dataContainer = Player.setHPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeHP)
                self.dataContainer = Player.setElContnr(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                        self.elementContainer)
                self.dataContainer = Player.setStats(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                     self.statsContainer)
        elif (self.nameElement == []):
            columnInfo = np.concatenate((initColumn, self.nameStats), axis=None)
            self.dataContainer = pd.DataFrame(0, rowLvl, columnInfo)
            self.dataContainer = Player.setLvContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeLevel)
            self.dataContainer = Player.setHPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeHP)
            self.dataContainer = Player.setMPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeMP)
            self.dataContainer = Player.setStats(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                 self.statsContainer)
        else:
            columnInfo = np.concatenate((initColumn, self.nameElement, self.nameStats), axis=None)
            self.dataContainer = pd.DataFrame(0, rowLvl, columnInfo)
            self.dataContainer = Player.setLvContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeLevel)
            self.dataContainer = Player.setHPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeHP)
            self.dataContainer = Player.setMPContnr(self.dataContainer, columnInfo, self.maxLevel, self.rangeMP)
            self.dataContainer = Player.setElContnr(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                    self.elementContainer)
            self.dataContainer = Player.setStats(self.dataContainer, initColumn, columnInfo, self.maxLevel,
                                                 self.statsContainer)

        pd.set_option('display.max_rows', 200)

        print("[RESULT] All Player Character Stats: \n")
        print(self.dataContainer)

        print("\n[DEBUG] Current TOTAL STATS: ", self.statsContainer.sum(axis=0), "\n")

        self.dataContainer.to_csv('csv_output_result/PlayerStats.csv', index=True)
