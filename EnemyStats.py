from EnemyDataContainer import Enemy

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


def all_enemies():
    # Initialize with ENEMIES NUMBER and MAX LEVELS
    numbers_enemy = 400
    max_level = 80
    enemies = Enemy(numbers_enemy, max_level)

    """
    [RANGE ENEMIES NAME]
    Set the "enemy_name" variable to string to automatically generate names
    Example:
       enemy_name = "Enemy"
    
    Set the "enemy_name" variable to list or array to manually generate name
    Example:
      enemy_name = ["alpha", "beta", "charlie", "delta"]
    """
    enemy_name = "Enemy"
    enemies.range_enemy_name(enemy_name, "Name", auto="yes")

    # [RANGE ENEMIES LEVELS]
    min_level = 1
    levels_class = ["Easy", "Medium", "High"]
    graph_title = "Player Level Distribution"

    enemies.range_levels(min_level, levels_class, 'Levels', scale=len(levels_class))
    enemies.show_range_levels(graph_title, title=False)

    # [RANGE ENEMIES HP]
    min_hp = 40
    max_hp = 520

    enemies.range_health_points(min_hp, max_hp, 'HP')

    # [RANGE ENEMIES MP]
    min_mp = 20
    max_mp = 490

    enemies.range_magic_points(min_mp, max_mp, 'MP')

    # [RANGE ENEMIES TYPE]
    enemy_type = ['Mixed', 'Hard Magic', 'Soft Magic', 'Hard Strength', 'Soft Strength']
    graph_title = "Enemy Level Distribution"

    # Distribution percentage (distribute_percent) example:
    # distribute_percent = [40, 10, 20, 10, 20]
    distribute_percent = [34, 13, 20, 13, 20]

    enemies.range_enemy_type(enemy_type, distribute_percent, 'Type')
    enemies.show_range_enemy_type(graph_title, title=False)

    """
    [RANGE ENEMIES WEAKNESSES]
    CHARACTER ELEMENT DAMAGE IMPACT.
    0: Normal damage.
    1: Repel against (no damage).
    2: The damage weaknesses.
    """
    element_name = ['Phys', 'Water', 'Wind', 'Earth', 'Fire']
    damage_name = ['Normal', 'Repel', 'Weak']
    graph_title = "Enemy Element Distribution"

    # Override this function when have different weaknesses concept!
    enemies.range_element_weak(element_name, damage_name)
    enemies.show_element_weak(graph_title, title=False)

    # [RANGE ENEMIES STATS]
    stats_name = ['Strength', 'Magic', 'Endurance', 'Speed', 'Luck']
    basic_max_stats = [50, 60, 40, 55, 45]
    basic_min_stats = [2, 2, 2, 2, 2]
    graph_title = "Enemy Stats Distribution"

    enemies.range_stats(stats_name, basic_min_stats, basic_max_stats)
    enemies.show_range_stats(graph_title, title=False)

    # Parse All Data to The Tables
    enemies.generate_enemy()


if __name__ == "__main__":
    all_enemies()
