#!/usr/bin/env python3
import subprocess
import ctypes
import ctypes.util
import os
libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p)


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







# use and unpack drive object here
def mount_drive(source, target, fs, options=''):
  ret = libc.mount(source, target, fs, 0, options)
  if ret < 0:
    errno = ctypes.get_errno()
    raise OSError(errno, "Error mounting {} ({}) on {} with options '{}': {}".
    format(source, fs, target, options, os.strerror(errno)))












def find_payload():
    pass


class Drive:
    # make getters and setters you stupid incel
    # so you can have partially populated obj at run time
    def __init__(self):
        self.source = ""
        self.target = "/mnt"
        self.fs = ""
        self.options = ""

    def set_source(self, source):
        self.source = source

    def set_fs(self, fs):
        self.fs = fs
    def set_options(self, options):
        self.options = options

    def get_source(self):
        return self.source
    def get_target(self):
        return self.target
    def get_fs(self):
        return self.fs
    def get_options(self):
        return self.options

def main():
    drives = grab_drives()
    raw_win_drives = locate_winfs(drives)
    print(len(raw_win_drives))

    win_drives = []
    #THIS SHIT IS ASS BACKWARDS AND YOURA A FUCKING INCEL
    # IF YOU DONT REFACTIOR IT IN THE MORINING

    for i in range(len(raw_win_drives)):
        temp_drive = Drive()
        temp_raw_drive = raw_win_drives[i].split()
        for attribute in temp_raw_drive:
            if "/dev" in attribute:
                #gotta trim the last character here
                temp_drive.set_source = attribute
            elif "TYPE" in attribute:
                temp_drive.set_fs = attribute

        temp_drive.set_source = raw_win_drives[i]
        temp_drive.set_target = raw_win_drives[i]
        temp_drive.set_fs = raw_win_drives[i]
        temp_drive.set_options = raw_win_drives[i]

        win_drives.append(temp_drive)





    # instantiate_drive = new Der


    

    # for drive in win_drives:
    #     print(drive)
    # for drive in win_drives:

    # create a drive object to store these attributes and then feed it to the mount_drive method   
    
    # mount_drive()
    # mount_drive('/dev/sdb1', '/mnt', 'ext4', 'rw')    

if __name__ == '__main__':
    main()
    

# OHHH fuck if you are reading this you forgott everyting and fell asleep
# I need to extract key drive info from the string first and store it in obj
# well good luck but here were my ideas at 10pm. Make drive object that holds
# string values about a drive. Then feed that to mount_drive method. I have to 
# unpack the object here though and modify the method to accept the object as input.
# it got way worse its 1030 and I fucked a lot of shit up probably
# this is my farewell 

# ➜ ./win32check.py
# 3
# ['/dev/sdb1:', 'LABEL="System', 'Reserved"', 'UUID="1C44DC8244DC5FD6"', 'TYPE="ntfs"', 'PARTUUID="23923449-01"']
# ['/dev/sdb2:', 'UUID="122ADE022ADDE2B1"', 'TYPE="ntfs"', 'PARTUUID="23923449-02"']
# ['/dev/sdb3:', 'UUID="266EA9266EA8F02B"', 'TYPE="ntfs"', 'PARTUUID="23923449-03"']

#THATS what was last spit out. Still hung up on populating the file obj
# There should maybe be some clues above lol. Next gotta rewrite stack overflow
# method so that it accepts my dope ass object.