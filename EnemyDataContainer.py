import sys
import math
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

import Model as md
import Visualization as vs

"ENEMIES CLASS"
class Enemy:
    "Enemy data stats container"
    def __init__(self, enemiesNumber, maxLevel):
        self.maxLevel = maxLevel
        self.levelsNumber = 0
        self.rangeLevel = []
        self.enemiesNumber = enemiesNumber
        self.enemiesName = []
        self.enemiesTypeName = []
        self.enemiesTypes = []
        self.minHP = 0
        self.minMP = 0
        self.maxHP = 0
        self.maxMP = 0
        self.rangeHP = []
        self.rangeMP = []
        self.damageName = []
        self.elementName = []
        self.elementContainer = []
        self.statsName = []
        self.statsContainer = []
        self.mainColumn = []
        self.dataContainer = []

    "Init Container"
    def setColuMain(pref, columnName, columnInfo):
        # Name
        if (pref == 0):
            if (columnInfo == []):
                columnInfo = [columnName, 'Level (Auto)', 'HP (AUTO)']

            if (columnInfo[1] != 'Level (Auto)' or columnInfo[2] != 'HP (Auto)'):
                columnInfo[0] = columnName

        # Levels
        if (pref == 1):
            if (columnInfo == []):
                columnInfo = ['Name (Auto)', columnInfo, 'HP (AUTO)']

            if (columnInfo[0] != 'Name (Auto)' or columnInfo[2] != 'HP (Auto)'):
                columnInfo[1] = columnName

        # HP
        if (pref == 2):
            if (columnInfo == []):
                columnInfo = ['Name (Auto)', 'Level (Auto)', columnInfo]

            if (columnInfo[0] != 'Name (Auto)' or columnInfo[1] != 'Level (Auto)'):
                columnInfo[2] = columnName

        # MP
        if (pref == 3):
            if (len(columnInfo) == 3):
                columnInfo.append(columnName)
            else:
                sys.exit("[ERROR] Please define Name, Level and HP first!")

        # Type
        if (pref == 4):
            if (len(columnInfo) == 4):
                columnInfo.append(columnName)
            else:
                sys.exit("[ERROR] Please define Name, Level,  and HP, and MP first!")

        return columnInfo


    "Enemies Name"
    # NOTE: THE EXPLAINATION ABOUT THE ENEMIES NAME WAS DISTRIBUTE HERE!
    # This section was created for users to define the name distribution.
    # You must override it, if you want different enemies types
    # distribution method.

    def genName(enName, enemiesNumber):
        namEnContrn = [None] * enemiesNumber

        for i in range(enemiesNumber):
            namEnContrn[i] = ("Enemy " + str(i + 1))

        return namEnContrn

    def rangeEnemyName(self, enName, columnName, auto=None):
        if (auto == "yes" or auto == "YES" or auto == "Yes"):
            self.enemiesName = Enemy.genName(enName, self.enemiesNumber)
        elif (auto == "no" or auto == "YES" or auto == "Yes"):
            self.enemiesName = enName
        else:
            sys.exit("[ERROR] Wrong \"auto\" value, can assign name to the enemies!")

        self.mainColumn = Enemy.setColuMain(0, columnName, self.mainColumn)


    "Levels"
    # NOTE: THE EXPLAINATION ABOUT THE ENEMIES LEVELS WAS DISTRIBUTE HERE!
    # This section was created for users to define the levels distribution.
    # You must override it, if you want different enemies levels
    # distribution method.

    def rangeLevels(self, minLevel, levelsClass, columnName, density=None, scale=0):
        self.levelsNumber = (self.maxLevel - minLevel) + 1

        # Split levels by levels of class levels
        partLevels = md.splitRange(self.levelsNumber, levelsClass, density=False)

        print("[DEBUG] ~ LEVELS")
        print("[DEBUG] Range LEVEL Distribution:       ", partLevels)

        # Split enemies numbers by class levels
        partEnemies = md.splitRange(self.enemiesNumber, levelsClass, density=False)

        print("[DEBUG] Range ENEMIES Distribution:     ", partEnemies)

        self.rangeLevel = np.zeros(self.enemiesNumber)

        i_Level = 1
        i_Enemy = 0

        for i in range(len(partLevels)):
            subPartLevels = md.splitRange(partLevels[i], scale, density=True)
            subPartEnemies = md.splitRange(partEnemies[i], scale, density=True)

            print("[DEBUG] Range Sub-LEVEL Distribution:   ", subPartLevels)
            print("[DEBUG] Range Sub-ENEMIES Distribution: ", subPartEnemies)

            for j in range(len(subPartEnemies)):
                for k in range(int(subPartEnemies[j])):
                    print("[DEBUG] Current Levels:         ", i_Level)
                    print("[DEBUG] Current subPartLevels:  ", subPartLevels[j])

                    self.rangeLevel[i_Enemy] = np.random.randint(i_Level, (i_Level + subPartLevels[j]))
                    print("[DEBUG] Current Emeny:          ", i_Enemy)
                    print("[DEBUG] Enemy levels:           ", self.rangeLevel[i_Enemy])
                    print("\n")

                    i_Enemy = i_Enemy + 1

                i_Level = i_Level + subPartLevels[i]

        self.rangeLevel.sort()

        self.mainColumn = Enemy.setColuMain(1, columnName, self.mainColumn)

    def showRangeLevels(self, graphTitle, title):
        print("[DEBUG] Range Levels Length: ", len(self.rangeLevel))
        print("[DEBUG] Range Levels: ")
        print(self.rangeLevel)
        print('\n\n')

        vs.enemyLevelGraph(self.rangeLevel, graphTitle, title)
        vs.enemyLevelNormDist(self.rangeLevel, graphTitle, title)


    "Enemy Type"
    # NOTE: THE EXPLAINATION ABOUT THE ENEMIES TYPE WAS DISTRIBUTE HERE!
    # This section was created for users to define the type distribution.
    # You must override it, if you want different enemies types
    # distribution method.

    def rangeEnemyType(self, enemyType, distribPercent, columnName):
        self.mainColumn = Enemy.setColuMain(4, columnName, self.mainColumn)
        self.enemiesTypeName = enemyType

        if (len(enemyType) != len(distribPercent)):
            sys.exit("[ERROR] The dimension of type and percentage distribution not match!")

        # Split levels into type by percentage
        distribNumber = np.zeros(len(enemyType))

        # Get actual range value from percentage
        for i in range(len(enemyType)):
            distribNumber[i] = md.roundNum((distribPercent[i] * len(self.rangeLevel)) / 100)

        # Map or distribute the enemy type
        distribLevel = np.zeros(len(enemyType))
        restDistribLevel = np.zeros(len(enemyType))
        self.enemiesTypes = np.zeros(self.enemiesNumber)

        # Check the amount of data
        totalDistEnemy = 0
        enemyDistrib = np.zeros(len(enemyType))

        # Distribute the level data
        for i in range(len(enemyType)):
            t_enemyDistrib = int(distribNumber[i] / len(distribPercent))
            distribLevel[i] = t_enemyDistrib

            # Get the rest of data
            restDistribLevel[i] = distribNumber[i] % len(distribPercent)

            # Checking amount of enemy
            for j in range(len(distribPercent)):
                totalDistEnemy = totalDistEnemy + t_enemyDistrib
                enemyDistrib[j] = enemyDistrib[j] + t_enemyDistrib

        print("[DEBUG] ~ TYPES")
        print("[DEBUG] ENEMIES to distribute: ", enemyDistrib)
        print("[DEBUG] Enemy NUMBERS distribution map (divide to 5 section): ", distribNumber)
        print("[DEBUG] Total Distributed ENEMIES: ", totalDistEnemy)
        print("\n")

        print("[DEBUG] Enemy LEVELS distribution map (divide to 5 section): ", distribLevel)
        print("[DEBUG] Rest of enemy LEVEL distribution: ", restDistribLevel)
        print("\n")

        # Checking amount of levels
        for i in range(len(distribLevel)):
            if (i == 0):
                distribLevel[i] = distribLevel[i]
            else:
                distribLevel[i] = distribLevel[i] + distribLevel[i - 1]

        print("[DEBUG] Range Enemy LEVEL Distribution Map: ", distribLevel)
        print("\n")

        # Initiate data with arrange or generate sequential number (0 - 80)
        suff_type = np.arange(1, enemyDistrib[0] + 1)

        # Suffled the generated number assumed as random
        np.random.shuffle(suff_type)

        # Continue and repeat the process above and merge it as one container
        for i in range(len(enemyType) - 1):
            t_suff_type = np.arange(1, enemyDistrib[0] + 1)
            np.random.shuffle(t_suff_type)

            suff_type = np.concatenate((suff_type, t_suff_type), axis=None)

        print("[DEBUG] Suffled Dimension Type Distribution: ", len(suff_type))
        print("[DEBUG] Suffled Type Distribution: ")
        print(suff_type)
        print("\n")

        # Set enemy types
        for i in range(len(suff_type)):
            for j in range(len(distribLevel)):
                # Check with distribLevel[0]
                if (suff_type[i] <= distribLevel[0]):
                    self.enemiesTypes[i] = j
                    break

                # Check with distribLevel[0] and distribLevel[1]
                if (suff_type[i] > distribLevel[j - 1] and suff_type[i] <= distribLevel[j]):
                    self.enemiesTypes[i] = j
                    break

        print("[DEBUG] Range Enemies Type: ")
        print(self.enemiesTypes)
        print("\n")

        # Handle rest of data
        restEnemy = len(self.enemiesTypes) - len(suff_type)

        # Set rest of enemy type
        if (restEnemy > 0):
            # Set the index to continue from suff_type
            restEnemyIndex = len(suff_type)

            for i in range(len(restDistribLevel)):
                if (restDistribLevel[i] > 0):
                    for j in range(int(restDistribLevel[i])):
                        # Continue to assign the rest
                        self.enemiesTypes[restEnemyIndex] = i
                        restEnemyIndex = restEnemyIndex + 1

    def showRangeEnemyType(self, graphTitle, title):
        print("[DEBUG] Range Enemies Type Dimension: ", self.enemiesTypes.shape)
        print("[DEBUG] Range Enemies Type: ")
        print(self.enemiesTypes)

        vs.enemyTypeGraph(self.enemiesTypeName, self.enemiesTypes, graphTitle, title)
        print('\n\n')


    "Health Points"
    def rangeHealthPoints(self, minHP, maxHP, columnName):
        self.mainColumn = Enemy.setColuMain(2, columnName, self.mainColumn)
        self.minHP = minHP
        self.maxHP = maxHP


    "Magic Points"
    def rangeMagicPoints(self, minMP, maxMP, columnName):
        self.mainColumn = Enemy.setColuMain(3, columnName, self.mainColumn)
        self.minMP = minMP
        self.maxMP = maxMP


    "Enemies Weaknesses"
    # NOTE: THE EXPLAINATION ABOUT THE ENEMIES WEAKNESSES WAS DISTRIBUTE HERE!
    # This section was created for users to define the weaknesses distribution.
    # You must override it, if you want different enemies weaknesses
    # distribution method.

    def rangeElementWeak(self, elementName, damageName):
        self.elementName = elementName
        self.damageName = damageName
        self.elementContainer = np.zeros((self.enemiesNumber, len(elementName)))

        # Set the damage affected was 3 per enemy
        # Operate between the number 1 (Repel), 2 (Weak)
        # And 0 (Normal) set as default number
        damageNumber = np.zeros(len(damageName) - 1)

        for i in range(len(self.elementContainer)):
            countDmgIndex = len(damageName)
            damageNumber[0] = np.random.randint(0, len(damageName) + 1)
            countDmgIndex = countDmgIndex - damageNumber[0]

            if (countDmgIndex > 0):
                for j in range(len(damageNumber) - 1):
                    if (countDmgIndex <= 0):
                        break

                    damageNumber[j + 1] = np.random.randint(0, countDmgIndex)
                    countDmgIndex = countDmgIndex - damageNumber[j + 1]
            else:
                for j in range(len(damageNumber) - 1):
                    damageNumber[j + 1] = len(damageName) - damageNumber[0]

            setDamage = np.zeros(len(elementName))

            for j in range(len(damageNumber)):
                if (damageNumber[j] != 0):
                    randSetDamage = 0

                    while (randSetDamage < damageNumber[j]):
                        index = np.random.randint(0, len(setDamage))

                        if (setDamage[index] == 0):
                            setDamage[index] = j + 1
                            randSetDamage = randSetDamage + 1

            self.elementContainer[i] = setDamage

    def showElementWeak(self, graphTitle, title):
        print("[DEBUG] ~ WEAKNESSES")

        if(self.elementName == []):
            print("[DEBUG] The game is not using Element of Weaknesses.\n")
        else:
            print("[DEBUG] List of characters elements: ", self.elementName)
            print("[DEBUG] List of characters elements stats: ")
            print(self.elementContainer)

            vs.enemyWeakGraph(self.elementName, self.damageName, self.elementContainer, graphTitle, title)
            print('\n\n')


    "Enemies Stats"
    # NOTE: THE EXPLAINATION ABOUT THE ENEMIES STATS WAS DISTRIBUTE HERE!
    # This section was created for users to define the stats distribution.
    # You must override it, if you want different stats distribution method.

    def rangeStats(self, statsName, basicMinStats, basicMaxStats):
        self.statsName = statsName
        self.rangeHP = np.zeros(len(self.enemiesTypes))
        self.rangeMP = np.zeros(len(self.enemiesTypes))
        self.statsContainer = np.zeros((len(self.enemiesTypes), len(statsName)))

        for i in range(len(self.enemiesTypes)):
            # Mixed
            if (self.enemiesTypes[i] == 0):
                mix_type = np.random.randint(1, 3)

                # MP Focused
                if (mix_type == 1):
                    botLimitHP = self.minHP
                    topLimitHP = botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                    print("Mixed(MP) Top HP: ", topLimitHP)

                    self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                    botLimitMP = self.minMP
                    topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                    print("Mixed(MP) Top MP: ", topLimitMP)

                    self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                    # Stats Correction
                    if (self.rangeHP[i] >= self.rangeMP[i]):
                        botLimitMP = self.rangeHP[i]
                        topLimitMP = botLimitMP + self.rangeHP[i] + 10
                        self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                    for j in range(self.statsContainer.shape[1]):
                        botLimitST = basicMinStats[j]
                        topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j]) # ceil (avoid out of range)
                        self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                    # Stats Correction
                    if (self.statsContainer[i][2] >= self.statsContainer[i][1]):
                        botLimitST = self.statsContainer[i][2]
                        topLimitST = botLimitST + 10
                        self.statsContainer[i][1] = np.random.randint(botLimitST, topLimitST)

                # HP Focused
                if (mix_type == 2):
                    botLimitHP = self.minHP
                    topLimitHP = botLimitHP + botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                    print("Mixed(HP) Top HP: ", topLimitHP)

                    self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                    botLimitMP = self.minMP
                    topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                    print("Mixed(HP) Top MP: ", topLimitMP)

                    self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                    # Stats Correction
                    if (self.rangeMP[i] >= self.rangeHP[i]):
                        botLimitHP = self.rangeMP[i]
                        topLimitHP = botLimitHP + 10
                        self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                    for j in range(self.statsContainer.shape[1]):
                        botLimitST = basicMinStats[j]
                        topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j]) # ceil (avoid out of range)
                        self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                    # Stats Correction
                    if (self.statsContainer[i][1] >= self.statsContainer[i][2]):
                        botLimitST = self.statsContainer[i][1]
                        topLimitST = botLimitST + self.statsContainer[i][1] + 10
                        self.statsContainer[i][2] = np.random.randint(botLimitST, topLimitST)

            # Hard Magic
            if (self.enemiesTypes[i] == 1):
                botLimitHP = self.minHP
                topLimitHP = botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                print("Hard Magic Top HP: ", topLimitHP)

                self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                botLimitMP = self.minMP
                topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                print("Hard Magic Top MP: ", topLimitMP)

                self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                # Stats Correction
                if (self.rangeHP[i] >= self.rangeMP[i]):
                    botLimitMP = self.rangeHP[i] + 100
                    topLimitMP = botLimitMP + 200
                    self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                for j in range(self.statsContainer.shape[1]):
                    botLimitST = basicMinStats[j]
                    topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j]) # ceil (avoid out of range)
                    self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                # Stats Correction
                if (self.statsContainer[i][2] - self.statsContainer[i][1] <= 10):
                    if (self.statsContainer[i][2] > self.statsContainer[i][1]):
                        botLimitST = self.statsContainer[i][2]
                        topLimitST = botLimitST + 10
                    else:
                        botLimitST = self.statsContainer[i][1]
                        topLimitST = botLimitST + 10

                    self.statsContainer[i][2] = np.random.randint(botLimitST, topLimitST)

            # Soft Magic
            if (self.enemiesTypes[i] == 2):
                botLimitHP = self.minHP
                topLimitHP = botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                print("Soft Magic Top HP: ", topLimitHP)

                self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                botLimitMP = self.minMP
                topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                print("Soft Magic Top MP: ", topLimitMP)

                self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                # Stats Correction
                if (self.rangeHP[i] >= self.rangeMP[i]):
                    botLimitMP = self.rangeHP[i]
                    topLimitMP = botLimitMP + 10
                    self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                for j in range(self.statsContainer.shape[1]):
                    botLimitST = basicMinStats[j]
                    topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j])
                    self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                # Stats Correction
                if (self.statsContainer[i][1] >= self.statsContainer[i][2]):
                    botLimitST = basicMinStats[1]
                    topLimitST = botLimitST + 10
                    self.statsContainer[i][2] = np.random.randint(botLimitST, topLimitST)

            # Hard Strength
            if (self.enemiesTypes[i] == 3):
                botLimitHP = self.minHP
                topLimitHP = botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                print("Hard Strength Top HP: ", topLimitHP)

                self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                botLimitMP = self.minMP
                topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                print("Hard Strength Top MP: ", topLimitMP)

                self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                # Stats Correction
                if (self.rangeMP[i] >= self.rangeHP[i]):
                    botLimitHP = self.rangeMP[i] + 100
                    topLimitHP = botLimitHP + 200
                    self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                for j in range(self.statsContainer.shape[1]):
                    botLimitST = basicMinStats[j]
                    topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j]) # ceil (avoid out of range)
                    self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                # Stats Correction
                if (self.statsContainer[i][1] - self.statsContainer[i][2] <= 10):
                    if (self.statsContainer[i][1] > self.statsContainer[i][2]):
                        botLimitST = self.statsContainer[i][1]
                        topLimitST = botLimitST + 10
                    else:
                        botLimitST = self.statsContainer[i][2]
                        topLimitST = botLimitST + 10

                    self.statsContainer[i][1] = np.random.randint(botLimitST, topLimitST)

            # Soft Strength
            if (self.enemiesTypes[i] == 4):
                botLimitHP = self.minHP
                topLimitHP = botLimitHP + md.roundNum((self.rangeLevel[i] / 100) * self.maxHP)
                print("Soft Strength Top HP: ", topLimitHP)

                self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                botLimitMP = self.minMP
                topLimitMP = botLimitMP + md.roundNum((self.rangeLevel[i] / 100) * self.maxMP)
                print("Soft Strength Top MP: ", topLimitMP)

                self.rangeMP[i] = np.random.randint(botLimitMP, topLimitMP)

                # Stats Correction
                if (self.rangeMP[i] >= self.rangeHP[i]):
                    botLimitHP = self.rangeMP[i]
                    topLimitHP = botLimitHP + 10
                    self.rangeHP[i] = np.random.randint(botLimitHP, topLimitHP)

                for j in range(self.statsContainer.shape[1]):
                    botLimitST = basicMinStats[j]
                    topLimitST = botLimitST + math.ceil((self.rangeLevel[i] / 100) * basicMaxStats[j]) # ceil (avoid out of range)
                    self.statsContainer[i][j] = np.random.randint(botLimitST, topLimitST)

                # Stats Correction
                if (self.statsContainer[i][2] >= self.statsContainer[i][1]):
                    botLimitST = basicMinStats[2]
                    topLimitST = botLimitST + 10
                    self.statsContainer[i][1] = np.random.randint(botLimitST, topLimitST)

    def showRangeStats(self, graphTitle, title):
        print("[DEBUG] ~ STATS")
        print("[DEBUG] Range Enemies Stats Dimension: ", self.statsContainer.shape)
        print("[DEBUG] Range Enemies Stats: ")
        print(self.statsContainer)

        vs.enemyHPGraph(self.rangeLevel, self.enemiesName, self.rangeHP, title)
        vs.enemyMPGraph(self.rangeLevel, self.enemiesName, self.rangeMP, title)
        vs.enemyStatsGraph(self.rangeLevel, self.enemiesName, self.statsName, self.statsContainer, graphTitle, title)
        print('\n\n')


    "All Enemies Stats Container"
    def setNamContnr(dataContainer, columnInfo, enemiesNumber, enemiesName):
        if(dataContainer[columnInfo[0]].shape[0] == enemiesNumber):
            dataContainer[columnInfo[0]] = enemiesName
            return dataContainer
        else:
            sys.exit("[ERROR] The list of names not match with the rows of data container!")

    def setLvContnr(dataContainer, columnInfo, enemiesNumber, rangeLevel):
        if(dataContainer[columnInfo[1]].shape[0] == enemiesNumber):
            dataContainer[columnInfo[1]] = rangeLevel
            return dataContainer
        else:
            sys.exit("[ERROR] The levels not match with the rows of data container!")

    def setHPContnr(dataContainer, columnInfo, enemiesNumber, rangeHP):
        if(dataContainer[columnInfo[2]].shape[0] == enemiesNumber):
            dataContainer[columnInfo[2]] = rangeHP
            return dataContainer
        else:
            sys.exit("[ERROR] The HP's rows not match with the rows of data container!")

    def setMPContnr(dataContainer, columnInfo, enemiesNumber, rangeMP):
        if(dataContainer[columnInfo[3]].shape[0] == enemiesNumber):
            dataContainer[columnInfo[3]] = rangeMP
            return dataContainer
        else:
            sys.exit("[ERROR] The MP's rows not match with the rows of data container!")

    def setTypeContnr(dataContainer, columnInfo, enemiesNumber, rangeTypes):
        if(dataContainer[columnInfo[4]].shape[0] == enemiesNumber):
            dataContainer[columnInfo[4]] = rangeTypes
            return dataContainer
        else:
            sys.exit("[ERROR] The MP's rows not match with the rows of data container!")

    def setElContnr(dataContainer, initColu, columnInfo, enemiesNumber, elementContainer):
        if(elementContainer.shape[0] == enemiesNumber):
            # With MP (Usually Turn-based)
            if(len(initColu) == 6):
                for i in range(elementContainer.shape[1]):
                    dataContainer[columnInfo[6 + i]] = elementContainer[:, i]

            # Without MP (Usually Action)
            else:
                for i in range(elementContainer.shape[1]):
                    dataContainer[columnInfo[5 + i]] = elementContainer[:, i]

            return dataContainer
        else:
            sys.exit("[ERROR] The Element's rows not match with the rows of data container!")

    def setStats(dataContainer, initColu, columnInfo, enemiesNumber, statsContainer):
        if(statsContainer.shape[0] == enemiesNumber):
            # Without Element (Usually Action)
            if(len(initColu) == 6):
                lenElContnr = columnInfo.shape[0] - (len(initColu) + statsContainer.shape[1])

                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo[len(initColu) + lenElContnr + i]] = statsContainer[:, i]

            # Without MP and Element (Usually Action)
            elif(len(initColu) == 5):
                lenElContnr = columnInfo.shape[0] - (len(initColu) + statsContainer.shape[1])

                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo[len(initColu) + lenElContnr + i]] = statsContainer[:, i]

            # Others
            else:
                for i in range(statsContainer.shape[1]):
                    dataContainer[columnInfo.shape[2 + i]] = statsContainer[:, i]

            return dataContainer
        else:
            sys.exit("[ERROR] The Stats's rows not match with the rows of data container!")

    def genEnemy(self):
        rowNum = np.arange((self.enemiesNumber - (self.enemiesNumber - 1)), self.enemiesNumber + 1)
        initColu = self.mainColumn

        if (self.rangeMP == []):
            if (self.elementName == []):
                columnInfo = np.concatenate((initColu, self.statsName), axis = None)
                self.dataContainer = pd.DataFrame(0, rowNum, columnInfo)
                self.dataContainer = Enemy.setNamContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesName)
                self.dataContainer = Enemy.setLvContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeLevel)
                self.dataContainer = Enemy.setHPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeHP)
                self.dataContainer = Enemy.setTypeContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesTypes)
                self.dataContainer = Enemy.setStats(self.dataContainer, initColu, columnInfo, self.enemiesNumber, self.statsContainer)
            else:
                columnInfo = np.concatenate((initColu, self.elementName, self.statsName), axis = None)
                self.dataContainer = pd.DataFrame(0, rowNum, columnInfo)
                self.dataContainer = Enemy.setNamContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesName)
                self.dataContainer = Enemy.setLvContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeLevel)
                self.dataContainer = Enemy.setHPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeHP)
                self.dataContainer = Enemy.setTypeContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesTypes)
                self.dataContainer = Enemy.setElContnr(self.dataContainer, initColu, columnInfo, self.elementContainer, self.elementContainer)
                self.dataContainer = Enemy.setStats(self.dataContainer, initColu, columnInfo, self.enemiesNumber, self.statsContainer)
        elif (self.elementName == []):
            columnInfo = np.concatenate((initColu, self.statsName), axis = None)
            self.dataContainer = pd.DataFrame(0, rowNum, columnInfo)
            self.dataContainer = Enemy.setNamContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesName)
            self.dataContainer = Enemy.setLvContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeLevel)
            self.dataContainer = Enemy.setHPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeHP)
            self.dataContainer = Enemy.setMPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeMP)
            self.dataContainer = Enemy.setTypeContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesTypes)
            self.dataContainer = Enemy.setStats(self.dataContainer, initColu, columnInfo, self.enemiesNumber, self.statsContainer)
        else:
            columnInfo = np.concatenate((initColu, self.elementName, self.statsName), axis = None)
            self.dataContainer = pd.DataFrame(0, rowNum, columnInfo)
            self.dataContainer = Enemy.setNamContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesName)
            self.dataContainer = Enemy.setLvContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeLevel)
            self.dataContainer = Enemy.setHPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeHP)
            self.dataContainer = Enemy.setMPContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.rangeMP)
            self.dataContainer = Enemy.setTypeContnr(self.dataContainer, columnInfo, self.enemiesNumber, self.enemiesTypes)
            self.dataContainer = Enemy.setElContnr(self.dataContainer, initColu, columnInfo, self.enemiesNumber, self.elementContainer)
            self.dataContainer = Enemy.setStats(self.dataContainer, initColu, columnInfo, self.enemiesNumber, self.statsContainer)

        pd.set_option('display.max_rows', 400)

        print("[RESULT] All Enemies Stats: \n")
        print(self.dataContainer)
        print('\n')

        self.dataContainer.to_csv('csv_output_result/EnemyStats.csv', index=True)
