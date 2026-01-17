import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    exit(1)

js = pygame.joystick.Joystick(0)
js.init()

print("Joystick name:", js.get_name())
print("Axes:", js.get_numaxes())
print("Buttons:", js.get_numbuttons())
print("Move ONLY the throttle stick\n")

while True:
    pygame.event.pump()

    axes = [js.get_axis(i) for i in range(js.get_numaxes())]
    print("Axes:", ["{:+.3f}".format(a) for a in axes])

    time.sleep(0.1)

