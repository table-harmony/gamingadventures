ScreenWidth, ScreenHeight = 1000, 500

FPS = 60

enemies = {
    'long_shooter': {'image': '../assets/enemy_1', 'enemy_speed': 2, 'enemy_health': 5, 'notice_range': ScreenWidth / 2, 'attack_range': ScreenWidth / 3, 'laser_cool_down': 3 * FPS},
    'shooter': {'image': '../assets/enemy_2', 'enemy_speed': 3, 'enemy_health': 3, 'notice_range': 300, 'attack_range': 200, 'laser_cool_down': FPS},
    'suicidal': {'image': '../assets/enemy_3', 'enemy_speed': 4.5, 'enemy_health': 1, 'notice_range': 50, 'attack_range': 15, 'laser_cool_down': FPS / 2}
}
