#!/usr/bin/python3
# Author: Marcel-Brian Wilkowsky
# Dependencies:
# sh

# TODO:
# * Using lib ctypes to mount partition
# * scan and compare with iso files on web

import os
import sys
import tempfile
import shutil
import signal
import requests
from bs4 import BeautifulSoup
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

operating_systems = {

    0: {"short_name": "debian", "name": "Debian", "url": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/"},
    1: {"short_name": "grml", "name": "grml", "url": "https://download.grml.org/"}
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
    iso_files = [];
    iterator = 0;
    for isofile in os.listdir(str(mount_dir)):
        if isofile.endswith(".iso"):
            if any(os in isofile for os in str(operating_systems.values())):
                iso_files.append(str(isofile));
                print("Found ISO: " + str(isofile));

    if len(iso_files) == 0:
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
        # try to update iso images
        for i in range(len(iso_files)):
            url = operating_systems[i]["url"];
            extension = "iso";
            request = requests.get(url).text;
            html_soup = BeautifulSoup(request, "html.parser");
            iso_images = [url + '/' + node.get('href') for node in html_soup.find_all('a') if node.get('href').endswith(extension)];
            iso_images = list(dict.fromkeys(iso_images));
            for image in iso_images:
                print(image);


def start():
    check_root();
    check_for_ventoy();

start();
