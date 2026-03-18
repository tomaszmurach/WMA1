# LAB1 – Red Object Detection and Tracking in Video

This project was created as part of a university computer vision lab using **Python**, **OpenCV**, and **NumPy**.

The program detects and tracks a **red bottle cap** in a video file. It uses **HSV color segmentation**, **morphological operations**, and **image moments** to estimate the position and size of the object.

## Features

- video loading from command line argument
- red color detection in **HSV**
- support for red hue wrap-around using **two HSV ranges**
- noise removal using **OPEN** and **CLOSE** morphology
- object center estimation using **image moments**
- circle visualization around detected object
- horizontal deviation bars showing left/right offset from image center
- two display windows:
  - original video with tracking overlay
  - processed binary mask

## Technologies

- Python 3
- OpenCV
- NumPy

## Project structure

```text
.
├── lab1_object_detection.py
└── F1.MOV
