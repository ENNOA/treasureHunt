import random

# Constants
GRID_SIZE = 10
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # N, E, S, W, NW, NE, SW, SE

# Initialize grid and searched status
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
searched = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place player, object, and enemies randomly
player_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
object_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
while object_pos == player_pos:
    object_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

# Number of enemies
num_enemies = 5
enemy_pos = []
for _ in range(num_enemies):
    pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while pos == player_pos or pos == object_pos or pos in enemy_pos:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    enemy_pos.append(pos)

# Player hiding status
is_hiding = False
turn_count = 0


def print_grid():
    print("  N\nW + E\n  S")  # Compass
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == player_pos and not is_hiding:
                print('P', end=' ')
            elif (x, y) in enemy_pos:
                print('E', end=' ')
            elif searched[x][y]:
                print('o', end=' ')
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


import random


def move_enemies():
    global enemy_pos, turn_count
    turn_count += 1
    new_positions = []
    for i, pos in enumerate(enemy_pos):
        if i == 0:  # First enemy moves towards player on the x-axis with 70% chance
            if random.random() < 0.45:  # 45% chance to move towards player
                x_move = 1 if pos[0] < player_pos[0] else -1 if pos[0] > player_pos[0] else 0
            else:  # 30% chance to move randomly on the x-axis
                x_move = random.choice([-1, 0, 1])
            y_move = random.choice([-1, 0, 1])  # Random move in y
            new_pos = (pos[0] + x_move, pos[1] + y_move)

        elif i == 1:  # Second enemy moves towards player on the y-axis with 70% chance
            if random.random() < 0.45:  # 45% chance to move towards player
                y_move = 1 if pos[1] < player_pos[1] else -1 if pos[1] > player_pos[1] else 0
            else:  # 30% chance to move randomly on the y-axis
                y_move = random.choice([-1, 0, 1])
            x_move = random.choice([-1, 0, 1])  # Random move in x
            new_pos = (pos[0] + x_move, pos[1] + y_move)

        elif i == 2:  # Third enemy moves directly towards player every other turn
            if turn_count % 2 == 0:
                x_move = 1 if pos[0] < player_pos[0] else -1 if pos[0] > player_pos[0] else 0
                y_move = 1 if pos[1] < player_pos[1] else -1 if pos[1] > player_pos[1] else 0
                new_pos = (pos[0] + x_move, pos[1] + y_move)
            else:
                new_pos = pos

        else:  # Remaining enemies move randomly
            direction = random.choice(DIRECTIONS)
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])

        # Ensure new position is within grid and not occupied by another enemy
        if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE and new_pos not in new_positions:
            new_positions.append(new_pos)
        else:
            new_positions.append(pos)  # If move is invalid, stay in the same position

    # Update all enemy positions after checks
    enemy_pos[:] = new_positions


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
