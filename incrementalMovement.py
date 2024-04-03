from gpiozero import DigitalOutputDevice, Servo
from time import sleep
import pygame
import pygame.camera
from ultralytics import YOLO

# setup vision model
model = YOLO("yolov8m.pt")


# Stepper Motor Configuration
direction_pin_stepper = DigitalOutputDevice(21)
pulse_pin_stepper = DigitalOutputDevice(20)
cw_direction_stepper = 0
ccw_direction_stepper = 1

# Servo Motor Configuration
servo_pin1 = 14
servo_pin2 = 17
servo1 = Servo(servo_pin1, min_pulse_width=0.0001, max_pulse_width=0.00275)
servo2 = Servo(servo_pin2, min_pulse_width=0.0001, max_pulse_width=0.00275)
servo1.mid() # Set servo to middle
servo2.mid() # Set servo to middle

# Initialize pygame
pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)

# Set up the camera
pygame.camera.init()
camera_source = "/dev/video0"  # Adjust the camera source as needed
camera = pygame.camera.Camera(camera_source, (640, 480))
camera.start()

# Flag to track if 'w' or 's' key is currently pressed
stepper_key_up_pressed = False
stepper_key_down_pressed = False

# Set incremement
global_inc = 0.2

def move_stepper(direction):
    if direction == 'up':
        direction_pin_stepper.value = ccw_direction_stepper
    elif direction == 'down':
        direction_pin_stepper.value = cw_direction_stepper
    else:
        direction_pin_stepper.value = cw_direction_stepper  # Default to up
    for _ in range(200):
        pulse_pin_stepper.on()
        sleep(0.001)
        pulse_pin_stepper.off()
        sleep(0.0005)

def move_servo1_right():
    inc = global_inc
    if servo1.value + inc <= 1:
        servo1.value += inc
    else:
        print("limit reached")

def move_servo1_left():
    inc = -global_inc
    if servo1.value + inc >= -1:
        servo1.value += inc
    else:
        print("limit reached")

def move_servo2_right():
    inc = global_inc
    if servo2.value + inc <= 1:
        servo2.value += inc
    else:
        print("limit reached")

def move_servo2_left():
    inc = -global_inc
    if servo2.value + inc >= -1:
        servo2.value += inc
    else:
        print("limit reached")

def return_servo1():
    servo1.value = 0
    
def return_servo2():
    servo2.value = 0

# Main loop
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    move_servo1_left()
                elif event.key == pygame.K_w:
                    move_servo1_right()
                elif event.key == pygame.K_a:
                    move_servo2_left()
                elif event.key == pygame.K_d:
                    move_servo2_right()
                elif event.key == pygame.K_e:
                    return_servo1()
                elif event.key == pygame.K_q:
                    return_servo2()
                elif event.key == pygame.K_UP:
                    stepper_key_up_pressed = True
                elif event.key == pygame.K_DOWN:
                    stepper_key_down_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    stepper_key_up_pressed = False
                elif event.key == pygame.K_DOWN:
                    stepper_key_down_pressed = False

        if stepper_key_up_pressed:
            move_stepper('up')
        elif stepper_key_down_pressed:
            move_stepper('down')

        # Capture frame-by-frame
        image = camera.get_image()




        # Display the frame on the screen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        sleep(0.1)  # Adjust the sleep time as needed
        
        print("Servo 1 value: " + str(servo1.value))
        print("Servo 2 value: " + str(servo2.value))
        
except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    direction_pin_stepper.close()
    pulse_pin_stepper.close()
    servo1.value = 0
    servo2.value = 0
    servo1.close()
    servo2.close()
    camera.stop()
