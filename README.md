# Blob Detector

![Demo](public/demo.gif)

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
- [To-Do](#to-do)

## Introduction
This project is a blob detector that processes video files to detect and highlight blobs.

## Setup

### Creating a Virtual Environment
To create a Python virtual environment, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the project directory:
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

### Installing Dependencies
To install all dependencies from [requirements.txt](http://_vscodecontentref_/1), run the following command:
```sh
pip install -r requirements.txt
```
### Usage
To execute the blob detector program, use the following command:
```sh
python blob_detector.py "path\to\the\video"
```
### Controls
- e: Press the key e to export video.
- p: Press the key p to pause video.
- q: Press the key q to quit the program.
- (+ / -): Press the plus or minus buttons to increase or decrease delay of processing (slows the playback).
### 💀 To-Do
- improve controls and customization