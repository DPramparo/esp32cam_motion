# Motion Detection with ESP32-CAM using Python and Telegram

This repository contains the code and resources for a project that utilizes an ESP32-CAM module to stream images, process them for motion detection, and send notifications through Telegram when motion is detected.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributions](#contributions)
- [License](#license)

## Introduction

In this project, I have developed a system that utilizes an ESP32-CAM to capture and stream images. The images are then processed using Python to detect motion. When motion is detected, a notification is sent through Telegram to alert the user. This project can be used for security applications, monitoring, or any scenario where motion detection is required.

## Features

- Live video streaming from ESP32-CAM module.
- Motion detection algorithm to identify changes in consecutive frames.
- Integration with Telegram for instant notifications upon motion detection.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/dpramparo/esp32cam_motion.git
   cd esp32cam_motion
   ```

2. Install the required Python packages:
    
    ```bash
    pip install -r requirements.txt
    ```
3. Configure your Telegram bot and obtain the bot token.
## Usage

Connect your ESP32-CAM module to your network and obtain its IP address.

Run the Python script:
    ```bash
    python motion_sensor.py
    ```
The script will continuously monitor the camera stream for motion. When motion is detected, a notification will be sent to your Telegram account.

## Configuration
Before running the project, you need to configure the following:

· Set up your ESP32-CAM to stream video.
· Create a Telegram bot and obtain the bot token.
· Update the motion_sensor.py file with your ESP32-CAM's IP address and Telegram bot token.
