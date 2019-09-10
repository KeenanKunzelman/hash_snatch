#!/usr/bin/env python3
import subprocess

#Run the command sudo blkid and then recieve its output as a bytes
#Decode using utf-8 and then split on \n
def grab_drives():
    proc = subprocess.Popen(["sudo blkid", "/etc/services"], stdout=subprocess.PIPE, shell=True)
    (drives, err) = proc.communicate()
    drives = drives.decode("utf-8").split("\n")
    return drives
    # Uncomment for debugging 
    # for drive in drives:
    #     print(drive)

# extracts the drives with ntfs types
# Modular for inclusion of *nix systems
def locate_winfs(drives):
    win_drives = []
    for drive in drives:
        if "ntfs" in drive:
            win_drives.append(drive)
    return win_drives

def mount_drive():
    pass

def find_payload():
    pass

def main():
    drives = grab_drives()
    win_drives = locate_winfs(drives)
    for drive in win_drives:
        print(drive)
if __name__ == '__main__':
    main()
    