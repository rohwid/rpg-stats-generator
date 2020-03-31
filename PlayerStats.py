from PlayerDataContainer import Player

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


def protagonist_char():
    # Initialize with PLAYERS MAX LEVELS
    max_level = 100
    protagonist = Player(max_level)

    # [RANGE CHARACTERS LEVELS]
    start_level = 1

    protagonist.rangeLevels(start_level, 'Levels')
    protagonist.showRangeLevels()

    # [RANGE CHARACTERS HP]
    start_hp = 159
    next_hp = 163
    graph_title = "Player HP Distribution"

    protagonist.rangeHealtPoints(start_hp, next_hp, 'HP')
    protagonist.showRangeHealtPoints(graph_title, title=False)

    # [RANGE CHARACTERS MP]
    start_mp = 89
    next_mp = 93
    graph_title = "Player MP Distribution"

    protagonist.rangeMagicPoints(start_mp, next_mp, 'MP')
    protagonist.showRangeMagicPoints(graph_title, title=False)

    # [RANGE CHARACTERS WEAKNESSES]
    # CHARACTER ELEMENT DAMAGE IMPACT.
    # 0: Normal damage.
    # 1: Repel against (no damage).
    # 2: The damage weaknesses.
    # Override this function when have different weaknesses concept!

    elements_name = ['Phys', 'Water', 'Wind', 'Earth', 'Fire']
    char_weak_number = [0, 2, 0, 0, 1]

    protagonist.rangeElementWeak(elements_name, char_weak_number)
    protagonist.showElmntWeak()

    # [RANGE CHARACTERS STATS]
    name_stats = ['Strength', 'Magic', 'Endurance', 'Speed', 'Luck']
    stats_max_value = [74, 38, 63, 65, 60]
    stats_to_assign = [2, 1]
    graph_title = "Player Stats Distribution"

    protagonist.rangeStats(name_stats, stats_max_value, stats_to_assign)
    protagonist.showRangeStats(graph_title, title=False)

    # Parse All Data to The Tables
    protagonist.genStats()


if __name__ == "__main__":
    protagonist_char()
