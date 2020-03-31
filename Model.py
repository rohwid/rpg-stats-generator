import sys
import math
import numpy as np

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

def roundNum(number):
    if (math.ceil(number) - number > number - math.floor(number)):
        return math.floor(number)
    elif (math.ceil(number) - number < number - math.floor(number)):
        return math.ceil(number)
    else:
        return math.ceil(number)


def splitRange(rangeNumber, numberSplitter, density=False):
    # for level and enemies
    if (density == False):
        number = len(numberSplitter)

    # for scale density
    if (density == True):
        number = numberSplitter

    value = np.zeros(number)

    # Rounding process
    if (rangeNumber % number == 0):
        for i in range(number):
            value[i] = rangeNumber / number
    else:
        for i in range(number):
            value[i] = rangeNumber / number

        if (number % 2 == 0):
            # 0 - 2 (if 6) - left
            even_1 = 0

            for i in range(int(number / 2)):
                # extract the unrounded value
                t_even_1 = value[i] - math.floor(value[i])
                even_1 = even_1 + t_even_1
                value[i] = math.floor(value[i])

            # add to the mid of range
            value[int(number / 2) - 1] = value[int(number / 2) - 1] + roundNum(even_1)

            # 3 - 5 (if 6) - right
            even_2 = 0

            for i in range(int(number / 2)):
                # extract the unrounded value
                t_even_2 = value[i + int(number / 2)] - math.floor(value[i + int(number / 2)])
                even_2 = even_2 + t_even_2
                value[int(number / 2) + i] = math.floor(value[int(number / 2) + i])

            # add to the mid of range
            value[int(number / 2)] = value[int(number / 2)] + roundNum(even_2)
        else:
            odd = 0

            for i in range(number):
                t_odd = value[i] - math.floor(value[i])
                odd = odd + t_odd
                value[i] = math.floor(value[i])

            # add to the mid of value
            value[math.ceil(number / 2) - 1] = value[math.ceil(number / 2)] + roundNum(odd)

    return value


def meanValue(allValue):
    sumValue = 0

    for i in range(len(allValue)):
        sumValue = sumValue + allValue[i]

    return sumValue / len(allValue)


def varVal(allValue, mean):
    sumValue = 0

    for i in range(len(allValue)):
        t_sumVal = (allValue[i] + mean)**2
        sumValue = sumValue + t_sumVal

    return sumValue / len(allValue)
