import cv2
import numpy as np
import math
import serial
import datetime

ser = serial.Serial('/dev/ttyUSB1', 9600)
ser.flush()

# Ignore initial lines
for _ in range(7):
    ser.readline()

# Initialize variables
width, height = 800, 600
center = (width // 2, height // 2)
radius = 200
color_top = (255, 0, 0)  # Red for top half
color_bottom = (0, 0, 255)  # Blue for bottom half

# Initialize position and rotation angle
x_pos, y_pos = center
angle = 0
rotation_step = 5
step_size = 5

# Create a black image
image = np.zeros((height, width, 3), dtype=np.uint8)

# Function to update position and rotation based on roll and pitch values
def update_position(roll, pitch):
    global x_pos, y_pos, angle

    # Convert the values from radians to degrees
    roll_degrees = math.degrees(roll)
    pitch_degrees = math.degrees(pitch)

    # Update angle based on roll (left-right movement)
    angle -= roll_degrees

    # Update y_pos based on pitch (up-down movement)
    y_pos += int(pitch_degrees)

# Precompute rotation matrix
def compute_rotation_matrix(angle):
    return np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                     [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

# Main loop
while True:
    # Reset image
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Create a meshgrid of coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Convert to polar coordinates
    x_c = x - center[0]
    y_c = y - center[1]

    # Calculate rotated coordinates
    rotated_coords = np.dot(compute_rotation_matrix(angle), np.vstack((x_c.flatten(), y_c.flatten())))
    rotated_x = rotated_coords[0, :].reshape((height, width)) + center[0]
    rotated_y = rotated_coords[1, :].reshape((height, width)) + center[1]

    # Calculate distances and mask for top and bottom halves
    distances = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    top_half_mask = rotated_y < y_pos

    # Draw top and bottom halves using NumPy operations
    image[(distances <= radius) & top_half_mask] = color_top
    image[(distances <= radius) & ~top_half_mask] = color_bottom

    # Draw crosshair at the center
    crosshair_size = 40
    cv2.line(image, (center[0] - crosshair_size, center[1]), (center[0] + crosshair_size, center[1]), (255, 255, 255), 2)
    cv2.line(image, (center[0], center[1] - crosshair_size), (center[0], center[1] + crosshair_size), (255, 255, 255), 2)

    cv2.line(image, (center[0] - 80 - crosshair_size, center[1] - 15), (center[0] - 120 + crosshair_size, center[1] - 15), (0, 0, 0), 2)
    cv2.line(image, (center[0] + 120 - crosshair_size, center[1] - 15), (center[0] + 80 + crosshair_size, center[1] - 15), (0, 0, 0), 2)

    cv2.line(image, (center[0] - 100 - crosshair_size, center[1]), (center[0] - 100 + crosshair_size, center[1]), (0, 0, 0), 2)
    cv2.line(image, (center[0] + 100 - crosshair_size, center[1]), (center[0] + 100 + crosshair_size, center[1]), (0, 0, 0), 2)

    cv2.line(image, (center[0] - 80 - crosshair_size, center[1] + 15), (center[0] - 120 + crosshair_size, center[1] + 15), (0, 0, 0), 2)
    cv2.line(image, (center[0] + 120 - crosshair_size, center[1] + 15), (center[0] + 80 + crosshair_size, center[1] + 15), (0, 0, 0), 2)

    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        axis_data = line.split(" - ")
        axis_values = {}

        for axis in axis_data:
            key, value = axis.split(": ")
            axis_values[key] = int(value)

        # Add current datetime to the axis_values dictionary
        axis_values['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



        ## calibrate or reset to 0 if reuired
        axis_values = {'AxisX': axis_values['AxisX'] - 151, 'AxisY': axis_values['AxisY'] - 125, 'AxisZ': axis_values['AxisZ'] - 230}
        print(axis_values)



        # Extracting values from the data
        axis_x = axis_values['AxisX']
        axis_y = axis_values['AxisY']
        axis_z = axis_values['AxisZ']

        # Calculating roll (φ) and pitch (θ)
        roll = math.atan2(axis_y, math.sqrt(axis_x**2 + axis_z**2))
        pitch = math.atan2(-axis_x, math.sqrt(axis_y**2 + axis_z**2))

        update_position(roll, pitch)

    # Display the image
    cv2.imshow('Inclinometer', image)

    # Wait for key press and update position
    key = cv2.waitKey(1)
    if key == 27:  # Break the loop if Esc key is pressed
        break

# Release resources
cv2.destroyAllWindows()
