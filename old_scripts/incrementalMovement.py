from gpiozero import DigitalOutputDevice, Servo
from time import sleep
import pygame
import pygame.camera
from adafruit_servokit import ServoKit
import board
from adafruit_pca9685 import PCA9685


# Stepper Motor Configuration
direction_pin_stepper = DigitalOutputDevice(21)
pulse_pin_stepper = DigitalOutputDevice(20)
cw_direction_stepper = 0
ccw_direction_stepper = 1

# Servo Motor Configuration
#servo_pin1 = 14
#servo_pin2 = 17
#servo1 = Servo(servo_pin1, min_pulse_width=0.0001, max_pulse_width=0.00275)
#servo2 = Servo(servo_pin2, min_pulse_width=0.0001, max_pulse_width=0.00275)
#servo1.mid() # Set servo to middle
#servo2.mid() # Set servo to middle

kit = ServoKit(channels=16)
servo1 = kit.servo[0]
servo2 = kit.servo[1]
global_step = 5.0

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

def move_servo_right(servo):
    target = servo.angle + global_step
    if target >= 180:
        target = 180
    elif target <= 0:
        target = 0

    servo.angle = target
    
def move_servo_left(servo):
    target = servo.angle - global_step
    if target >= 180:
        target = 180
    elif target <= 0:
        target = 0

    servo.angle = target

def return_servo1():
    servo1.angle = 0
    
def return_servo2():
    servo2.angle = 0

# Main loop
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    move_servo_left(servo1)
                elif event.key == pygame.K_w:
                    move_servo_right(servo1)
                elif event.key == pygame.K_a:
                    move_servo_left(servo2)
                elif event.key == pygame.K_d:
                    move_servo_right(servo2)
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
        
        print("Servo 1 value: " + str(servo1.angle))
        print("Servo 2 value: " + str(servo2.angle))
        
except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    direction_pin_stepper.close()
    pulse_pin_stepper.close()
    servo1.angle = 90
    servo2.angle = 90
    camera.stop()
