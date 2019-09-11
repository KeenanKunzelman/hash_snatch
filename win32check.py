#!/usr/bin/env python3

# Author: Keenan Kunzelman
# Description: Meant to be run on a linux bootable usb. Program scans for all connected storage devices and looks for specific 
# file systems to mount and then exfils data. Only looks for NTFS and exfils the calc.exe program for now.

import subprocess
import os
import shutil

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
    subprocess.Popen(["sudo mount -t ntfs -o nls=utf8,umask=0222 {} /media/windows".format(drive.get_source()), "/etc/services"], shell=True)
    subprocess.call(["sudo", "cp", "/media/windows/Windows/System32/calc.exe", "~/Desktop"])

def find_winpayload():
#    source = os.listdir("/media/windows")
#    print(source)
    pass
    # shutil.copy('/media/windows/Windows/System32/calc.exe', "~/Desktop")


  
    # subprocess.Popen(["cp calc.exe ~/Desktop", "/etc/services"], shell=True)

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
    drives = grab_drives()
    raw_win_drives = locate_winfs(drives)
    win_drives = storewin_drives(raw_win_drives)
    mount_drive(win_drives[1])
    find_winpayload()


 

if __name__ == '__main__':
    main()
    


