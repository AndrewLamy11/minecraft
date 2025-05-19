from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time

app = Ursina()

player = FirstPersonController()
Sky()

# ----- Settings -----
block_size = 1
selected_texture = 'dirt.png'
fly_mode = False
last_y_press = 0

# Speed control
normal_speed = 5
sprint_speed = 10
player.speed = normal_speed

# Block storage
boxes = []

# World generation
world_width = 20
world_depth = 20
world_height = 15  # Number of underground layers

for y in range(-world_height, 0):
    for x in range(world_width):
        for z in range(world_depth):
            texture = 'dirt.png' if y >= -3 else 'stone.png'
            box = Button(
                model='cube',
                color=color.white,
                texture=texture,
                position=(x, y, z),
                parent=scene,
                origin_y=0.5,
                scale=block_size
            )
            boxes.append(box)

# ----- Input Handling -----
def input(key):
    global selected_texture, fly_mode, last_y_press

    # Block type switching
    if key == '1':
        selected_texture = 'dirt.png'
        print("Selected: Dirt")
    if key == '2':
        selected_texture = 'stone.png'
        print("Selected: Stone")

    # Fly mode toggle on double-tap Y
    if key == 'y':
        current_time = time.time()
        if current_time - last_y_press < 0.4:
            fly_mode = not fly_mode
            player.gravity = 0 if fly_mode else 1
            print("Fly Mode:", "ON" if fly_mode else "OFF")
        last_y_press = current_time

    # Interact with hovered block only
    hovered = mouse.hovered_entity
    if hovered and isinstance(hovered, Button):
        if key == 'left mouse down':
            new = Button(
                model='cube',
                color=color.white,
                texture=selected_texture,
                position=hovered.position + mouse.normal * block_size,
                parent=scene,
                origin_y=0.5,
                scale=block_size
            )
            boxes.append(new)
        elif key == 'right mouse down':
            if hovered in boxes:
                boxes.remove(hovered)
            destroy(hovered)

# ----- Update Loop -----
def update():
    # Sprint toggle
    player.speed = sprint_speed if held_keys['shift'] else normal_speed

    # Fly up/down
    if fly_mode:
        if held_keys['space']:
            player.y += 5 * time.dt
        if held_keys['control']:
            player.y -= 5 * time.dt

app.run()
