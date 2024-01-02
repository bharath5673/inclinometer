# Inclinometer Project

<div align="center">
<p>
<img src="demo/Screenshot from 2024-01-02 21-58-01.png" width="600"/>  <img src="demo/Screenshot from 2024-01-02 21-58-26.png" width="600"/> 
</p>
<br>
</div>


## Overview
The Inclinometer project is a simple Python application using OpenCV to simulate an inclinometer or pitch and roll indicator. It provides a visual representation of the orientation of an object in two dimensions.

## Features
- Simulates pitch and roll movements based on user input.
- Interactive controls for adjusting orientation.
- Visual representation with a compass-style display.

## MPU6050 Integration
The project includes integration with the MPU6050 accelerometer and gyroscope sensor through Arduino and Python.

### Arduino Code
The Arduino code (`imu.ino`) reads data from the MPU6050 sensor and communicates the pitch and roll values to the Python script via serial communication.

### Python Code
The Python code (`test_digi_inclinometer_mpu6050`) receives data from the Arduino, processes it, and updates the inclinometer display accordingly.

## Dependencies
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Math
- Arduino IDE (for uploading the Arduino code)
- MPU6050 Library for Arduino
- pyserial


