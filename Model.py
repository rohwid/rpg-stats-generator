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


def round_number(number):
    if math.ceil(number) - number > number - math.floor(number):
        return math.floor(number)
    elif math.ceil(number) - number < number - math.floor(number):
        return math.ceil(number)
    else:
        return math.ceil(number)


def split_range(range_number, number_splitter, density=False):
    number = 0

    # for level and enemies
    if not density:
        number = len(number_splitter)

    # for scale density
    if density:
        number = number_splitter

    value = np.zeros(number)

    # Rounding process
    if range_number % number == 0:
        for i in range(number):
            value[i] = range_number / number
    else:
        for i in range(number):
            value[i] = range_number / number

        if number % 2 == 0:
            # 0 - 2 (if 6) - left
            even_left = 0

            for i in range(int(number / 2)):
                # extract the unrounded value
                temp_even_1 = value[i] - math.floor(value[i])
                even_left = even_left + temp_even_1
                value[i] = math.floor(value[i])

            # add to the mid of range
            value[int(number / 2) - 1] = value[int(number / 2) - 1] + round_number(even_left)

            # 3 - 5 (if 6) - right
            even_right = 0

            for i in range(int(number / 2)):
                # extract the unrounded value
                temp_even_right = value[i + int(number / 2)] - math.floor(value[i + int(number / 2)])
                even_right = even_right + temp_even_right
                value[int(number / 2) + i] = math.floor(value[int(number / 2) + i])

            # add to the mid of range
            value[int(number / 2)] = value[int(number / 2)] + round_number(even_right)
        else:
            odd = 0

            for i in range(number):
                temp_odd = value[i] - math.floor(value[i])
                odd = odd + temp_odd
                value[i] = math.floor(value[i])

            # add to the mid of value
            value[math.ceil(number / 2) - 1] = value[math.ceil(number / 2)] + round_number(odd)

    return value


def mean_values(all_values):
    sum_value = 0

    for i in range(len(all_values)):
        sum_value = sum_value + all_values[i]

    return sum_value / len(all_values)


def var_val(all_values, mean):
    sum_values = 0

    for i in range(len(all_values)):
        temp_sum_values = (all_values[i] + mean) ** 2
        sum_values = sum_values + temp_sum_values

    return sum_values / len(all_values)
