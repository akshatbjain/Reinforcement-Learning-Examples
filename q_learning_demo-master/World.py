# Author = Akshat Jain
# Code based on philippe's code (https://github.com/llSourcell/q_learning_demo)

from Tkinter import *
from random import randint

master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 100
(x, y) = (10, 10)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
score = 1
restart = False
walk_reward = -0.04

walls = []
occupied = []
print("Adding Walls now...")
for i in range(10):
    temp_x = randint(0,9)
    temp_y = randint(0,9)
    walls.append((temp_x, temp_y))
    occupied.append((temp_x, temp_y))
print("Added Walls!")

add_green = False
add_red = False
specials = []
print("Adding Green and Red Cells now...")
while(not add_green or not add_red):
    if(not add_green):
        green_x = randint(0,9)
        green_y = randint(0,9)
        if((green_x, green_y) not in occupied):
            specials.append((green_x, green_y, "green", 1))
            occupied.append((green_x, green_y))
            add_green = True
            print("Added Green!")
    if(not add_red):
        red_x = randint(0,9)
        red_y = randint(0,9)
        if((red_x, red_y) not in occupied):
            specials.append((red_x, red_y, "red", -1))
            occupied.append((red_x, red_y))
            add_red = True
            print("Added Red!")

add_player = False
player_x = 0
player_y = 0
print("Adding Player now...")
while(not add_player):
    player_x = randint(0,9)
    player_y = randint(0,9)
    if((player_x, player_y) not in occupied):
        player = (player_x, player_y)
        add_player = True
        print("Added Player!")

cell_scores = {}

def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()

def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart

    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print "Success! score: ", score
            else:
                print "Fail! score: ", score
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (player_x, player_y)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
