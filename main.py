import random

# Constants
GRID_SIZE = 10
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # N, E, S, W, NW, NE, SW, SE

# Initialize grid and searched status
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
searched = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place player, object, and enemies randomly
player_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
object_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
while object_pos == player_pos:
    object_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

# Number of enemies
num_enemies = 5
enemy_pos = []
for _ in range(num_enemies):
    pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    while pos == player_pos or pos == object_pos or pos in enemy_pos:
        pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    enemy_pos.append(pos)

# Player hiding status
is_hiding = False

def print_grid():
    print("  N\nW + E\n  S")  # Compass
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == player_pos and not is_hiding:
                print('P', end=' ')
            elif searched[x][y]:
                print('o', end=' ')
            elif (x, y) in enemy_pos:
                print('E', end=' ')
            else:
                print('.', end=' ')
        print()
    print()

def move_player(direction):
    global player_pos, is_hiding
    is_hiding = False  # Player stops hiding when they move
    new_pos = (player_pos[0] + direction[0], player_pos[1] + direction[1])
    if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
        player_pos = new_pos
        check_game_status()
    else:
        print("Invalid move. Try again.")

def move_enemies():
    global enemy_pos
    for i, pos in enumerate(enemy_pos):
        direction = random.choice(DIRECTIONS)
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
            enemy_pos[i] = new_pos

def search_surroundings():
    global is_hiding
    is_hiding = False  # Player stops hiding when they search
    found_something = False
    print("Searching surrounding squares...")
    for direction in DIRECTIONS:
        search_pos = (player_pos[0] + direction[0], player_pos[1] + direction[1])
        if 0 <= search_pos[0] < GRID_SIZE and 0 <= search_pos[1] < GRID_SIZE:
            searched[search_pos[0]][search_pos[1]] = True
            if search_pos == object_pos:
                print("The treasure is near!")
                found_something = True
            elif search_pos in enemy_pos:
                print("Enemy spotted nearby!")
                found_something = True
    if not found_something:
        print("Nothing found.")

def hide():
    global is_hiding
    is_hiding = True
    print("You are hiding. Enemies can't see you this turn.")

def check_game_status():
    global is_hiding
    if player_pos == object_pos:
        print("You found the Treasure! You win!")
        exit()
    if player_pos in enemy_pos and not is_hiding:
        print("An enemy got you! Game over.")
        exit()

def player_turn():
    global is_hiding
    print_grid()
    action = input("Choose action (move [n, e, s, w], search, or hide): ")
    if action in ['n', 'e', 's', 'w']:
        direction = {'n': DIRECTIONS[0], 'e': DIRECTIONS[1], 's': DIRECTIONS[2], 'w': DIRECTIONS[3]}[action]
        move_player(direction)
    elif action == 'search':
        search_surroundings()
    elif action == 'hide':
        hide()
    else:
        print("Invalid action.")
    move_enemies()
    check_game_status()

# Game loop
while True:
    player_turn()
