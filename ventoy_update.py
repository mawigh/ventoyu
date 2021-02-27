#!/usr/bin/python3
# Author: Marcel-Brian Wilkowsky
# Dependencies:
# sh

# TODO:
# * Auto check for ventoy partition
# * Using lib ctypes to mount partition

import os
import sys
import tempfile
import shutil
import signal
import urllib.request
from subprocess import check_output
from sh import mount, umount

# Global variables
mounted=False;
partition="";
temp_dir="";

# Catch SIGINT
def sig_handler (signal, frame):
    print("You pressed Ctrl+C! Umount partition, if mounted");
    # UMOUNT
    sys.exit(1);

signal.signal(signal.SIGINT, sig_handler);

# ID, Name, URL
operating_systems = {
        "debian": [1, "Debian", "URLURLURLURL"],
        "grml": [2, "GRML", "URLURLURLURL"],
        "Win": [3, "Windows 10", "URLURLURLURL"]
}

def check_root ():
    uid = os.getuid();
    if not uid == 0:
        sys.exit("Are you dumb? How should I access your Ventoy drive without root access?");
    else:
        return 0;

def check_for_ventoy ():
    print("\nTry to find a partition with ventoy installed...");
    check_ventoy = check_output("lsblk -l -o NAME,LABEL | grep ventoy | cut -d ' ' -f1", shell=True);

    if not check_ventoy:
        print("\nNo partition found! You can try to enter a partition manually:\n");
        select_partition();
    else:
        # Partition with LABEL: ventoy found
        check_ventoy = check_ventoy.decode("utf-8");
        # delete new line 
        check_ventoy = check_ventoy.rstrip("\n");
        print("\nI found a partition with label 'ventoy': " + str(check_ventoy));
        qask = input("Is " + str(check_ventoy) + " the correct partition? [Y/n]: ");

        if qask == "y" or qask == "Y" or qask == "":
            print("\nOK. Using partition " + str(check_ventoy));
            mount_device(str(check_ventoy));
        else:
            select_partition();

def select_partition ():
    show_drives = check_output("lsblk -o NAME -n -l | xargs", shell=True);
    show_drives = show_drives.decode("utf-8").split(" ");

    print("Found Block Devices:");
    for i in range(len(show_drives)):
        print("-> " + str(show_drives[i]));
    while(True):
        print("\nOn which partition should I update Ventoy .iso images?")
        qpartition = input("Partition: ");
        if qpartition == "":
            print("Are you drunk? You should type something.");
            continue;
        else:
            if not str(qpartition) in show_drives:
                print("WTF? Type in a valid parititon!");
                continue;
            else:
                print("\nUsing partition: " + str(qpartition));
                mount_device(str(qpartition));
                break;

def mount_device (partition):
    # create temporary directory
    temp_dir = tempfile.mkdtemp();
    print("Using temporary directory: " + temp_dir);
    # mount ventoy partition to manage the .iso files

    if not "dev" in str(partition):
        partition = "/dev/" + str(partition);

    print("\nTry mounting it...");
    try: 
        mount(str(partition),str(temp_dir));
        print("Mounted " + str(partition) + " on " + str(temp_dir) + "...");
    except:
        sys.exit("Cannot mount " + str(partition) + " partition...");

    # show drive stats
    print("\nVentoy usage statistics:");
    print("Total: " + str(round(shutil.disk_usage(temp_dir).total/1024/1024/1024)) + "GB");
    print("Used: " + str(round(shutil.disk_usage(temp_dir).used/1024/1024/1024)) + "GB");
    print("Free: " + str(round(shutil.disk_usage(temp_dir).free/1024/1024/1024)) + "GB");
    ventoy_updater(temp_dir);

def ventoy_updater (mount_dir):
    # check for installed .iso images
    print("\n# Scanning for .iso files...");
    iso_files = 0;
    for isofile in os.listdir(str(mount_dir)):
        if isofile.endswith(".iso"):
            if any(os in isofile for os in operating_systems):
                iso_files += 1;
                print("Found ISO: " + str(isofile));

    if iso_files == 0:
        print("No .iso files found :-(")
        newq = input("Do you want to download new .iso images? [y/N] ")
        
        if newq == "y" or newq == "Y":
            print(operating_systems);
            qosa = input("Please select an Operating System (comma-seperated): ");

            if qosa == "":
                print("No Operating System selected. Aborting...");
                sys.exit(0);
        else:
            print("Aborting...")
            sys.exit(0);
    else:
        # try to update
        pass;

def start():
    check_root();
    check_for_ventoy();

start();
