import cv2
import numpy as np
import math

# Initialize variables
width, height = 800, 600
center = (width // 2, height // 2)
radius = 200
color_top = (255, 100, 50)  # Red for top half
color_bottom = (0, 25, 125)  # Blue for bottom half

# Initialize position and rotation angle
x_pos, y_pos = center
angle = 0
rotation_step = 5
step_size = 5

# Create a black image
image = np.zeros((height, width, 3), dtype=np.uint8)

# Function to update position and rotation based on key press
def update_position(key):
    global x_pos, y_pos, angle
    if key == ord('w'):
        y_pos = max(y_pos - step_size, center[1] - radius)
    elif key == ord('s'):
        y_pos = min(y_pos + step_size, center[1] + radius)
    elif key == ord('d'):
        angle -= rotation_step
    elif key == ord('a'):
        angle += rotation_step


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
    crosshair_size = 50
    cv2.line(image, (center[0] - crosshair_size, center[1]), (center[0] + crosshair_size, center[1]), (255, 255, 255), 2)
    cv2.line(image, (center[0], center[1] - crosshair_size), (center[0], center[1] + crosshair_size), (255, 255, 255), 2)

    cv2.line(image, (center[0]-80 - crosshair_size, center[1]-15), (center[0]-120 + crosshair_size, center[1]-15) , (0, 0, 0), 2)
    cv2.line(image, (center[0]+120 - crosshair_size, center[1]-15), (center[0]+80 + crosshair_size, center[1]-15) , (0, 0, 0), 2)

    cv2.line(image, (center[0]-100 - crosshair_size, center[1]), (center[0]-100 + crosshair_size, center[1]) , (0, 0, 0), 2)
    cv2.line(image, (center[0]+100 - crosshair_size, center[1]), (center[0]+100 + crosshair_size, center[1]) , (0, 0, 0), 2)

    cv2.line(image, (center[0]-80 - crosshair_size, center[1]+15), (center[0]-120 + crosshair_size, center[1]+15) , (0, 0, 0), 2)
    cv2.line(image, (center[0]+120 - crosshair_size, center[1]+15), (center[0]+80 + crosshair_size, center[1]+15) , (0, 0, 0), 2)


    # Draw additional crosshair for roll
    roll_crosshair_size = 30
    roll_crosshair_angle = -angle - 90  # Use the same angle as the inclination

    # Calculate rotated position for roll crosshair
    roll_crosshair_x = center[0] + int(roll_crosshair_size * np.cos(np.radians(roll_crosshair_angle)))
    roll_crosshair_y = center[1] + int(roll_crosshair_size * np.sin(np.radians(roll_crosshair_angle)))
    # Draw roll crosshair
    cv2.line(image, (center[0], center[1]), (roll_crosshair_x, roll_crosshair_y), (0, 100, 255), 2)

    # Draw arrow mark on top of the roll crosshair
    arrow_tip = (roll_crosshair_x, roll_crosshair_y)
    cv2.arrowedLine(image, (center[0], center[1]), arrow_tip, (0, 100, 255), 2, tipLength=0.3)

    # Display controls
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'Controls:', (20, 40), font, 0.5, (255, 255, 255), 1)
    cv2.putText(image, 'W: Pitch+', (20, 80), font, 0.4, (255, 255, 255), 1)
    cv2.putText(image, 'S: Pitch-', (20, 120), font, 0.4, (255, 255, 255), 1)
    cv2.putText(image, 'A: Roll+', (20, 160), font, 0.4, (255, 255, 255), 1)
    cv2.putText(image, 'D: Roll-', (20, 200), font, 0.4, (255, 255, 255), 1)

    # Display the image
    cv2.imshow('Inclinometer', image)

    # Wait for key press and update position
    key = cv2.waitKey(1)
    if key == 27:  # Break the loop if Esc key is pressed
        break
    update_position(key)

# Release resources
cv2.destroyAllWindows()
