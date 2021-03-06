import datetime

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

from PlayerDataContainer import Player

def protagonist_char():
    # Initialize with PLAYERS MAX LEVELS
    max_level = 100
    protagonist = Player(max_level)

    # [RANGE CHARACTERS LEVELS]
    start_level = 1

    # Show Debug
    debug = False

    protagonist.range_levels(start_level, 'Levels')
    protagonist.show_range_levels(debug)

    # [RANGE CHARACTERS HP]
    start_hp = 224
    next_hp = 228

    # Show Graph and Debug
    graph = True
    debug = False

    # Show Graph Title
    graph_title = 'Player HP Distribution'
    title = True

    protagonist.range_health_points(start_hp, next_hp, 'HP')
    protagonist.show_range_health_points(graph_title, graph, title, debug)

    # [RANGE CHARACTERS MP]
    start_mp = 100
    next_mp = 102

    # Show Graph and Debug
    graph = True
    debug = False

    # Show Graph Title
    graph_title = 'Player MP Distribution'
    title = True

    protagonist.range_magic_points(start_mp, next_mp, 'MP')
    protagonist.show_range_magic_points(graph_title, graph, title, debug)

    """
    [RANGE CHARACTERS WEAKNESSES]
    CHARACTER ELEMENT DAMAGE IMPACT.
    0: Normal damage.
    1: Repel against (no damage).
    2: The damage weaknesses.
    Override this function when have different weaknesses concept!
    """
    elements_name = ['Phys', 'Water', 'Wind', 'Earth', 'Fire']
    char_weak_number = [0, 0, 2, 1, 2]

    # Show Debug
    debug = False

    protagonist.range_element_weak(elements_name, char_weak_number)
    protagonist.show_element_weak(debug)

    # [RANGE CHARACTERS STATS]
    name_stats = ['Strength', 'Magic', 'Endurance', 'Speed', 'Luck']
    stats_max_value = [88, 32, 81, 43, 56]
    stats_to_assign = [2, 1]

    # Show Graph and Debug
    graph = True
    debug = False

    # Show Graph Title
    graph_title = 'Player Stats Distribution'
    title = True

    protagonist.range_stats(name_stats, stats_max_value, stats_to_assign)
    protagonist.show_range_stats(graph_title, graph, title, debug)

    # Parse All Data to The Tables
    protagonist.generate_stats()


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    protagonist_char()
    print('\nTime to run this program: ', datetime.datetime.now() - begin_time)
