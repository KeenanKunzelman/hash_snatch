# Calc Stealer

## Description

> A simple poc to test if I can mount a drive and exfil data off of it using python

## Installation

> Clone this repo and then cd into the directory you cloned. You can then run the script using `python3 win32check.py` or `./win32check.py`

## Usage

> The script supports two modes of execution. If you provide no command line args it will just dump connected storage devices to the screen. If you pass it **-w** like `./win32check.py -w` it will list drives using the NTFS file system and prompt you to select one. After selecting a drive the program will copy the calc.exe file onto your desktop. 
