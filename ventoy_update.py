#!/usr/bin/python3
# Author: Marcel-Brian Wilkowsky
# Dependencies:
# 

import os
import sys
import tempfile
import shutil
import urllib.request

# ID, Name, URL
operating_systems = {

        "debian": [1, "Debian", "URLURLURLURL"]
}

def check_root ():
    uid = os.getuid();
    if not uid == 0:
        sys.exit("Are you dumb? How should I access your Ventoy drive without root access?");
    else:
        check_ventoy();

def check_ventoy ():
    print("Checking for Ventoy drive...");
    mount_device();

def mount_device ():
    # create temporary directory
    temp_dir = tempfile.mkdtemp();
    print("Using temporary directory: " + temp_dir);
    # mount ventoy partition to manage the .iso files

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

check_root();
