# Author: Marcel-Brian Wilkowsky (mawigh)

import json;
import subprocess;
import shutil;
import re;
import sys;
import tempfile;
import sh;
import os;
import logging;

class ventoyl:

    def __init__ (self, ventoy_device=None, debug=False):
        self.device_mounted = False;
        self.iso_images = [];
        self.ventoy_device = ventoy_device;
        self.__easysearch = True;
        self.device_mounted = False;

        if not self.ventoy_device:
            self.find_ventoy_device();
            if self.ventoy_device:
                ttr = self.check_ventoy_mount();
                self.mount_ventoy_device();

        if debug:
            logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

        # check url json file

    def find_ventoy_device (self):

        ls_blkd = shutil.which("lsblk");
        fdevice = "";
        if ls_blkd:
            lsblk_out = subprocess.check_output([ls_blkd, "-Jnpo", "label,name"]);
            json_parse = json.loads(lsblk_out);
            search_pattern = "[V,v]entoy";
            if isinstance(json_parse, dict):
                for key in json_parse["blockdevices"]:
                    if key["children"]:
                        for child in key["children"]:
                            if re.search(search_pattern, str(child["label"])):
                                fdevice = child;
                                logging.debug("Found Ventoy device: " + str(child));
            else:
                return False;

            if isinstance(fdevice, dict):
                self.ventoy_device = fdevice["name"];
                return fdevice;
            else:
                return False;
        else:
            return False;

    def check_ventoy_mount (self):
        if not self.ventoy_device:
            self.find_ventoy_device();

        lsblk_out = subprocess.check_output(["lsblk","-Jnpo","name,mountpoint"]);
        json_parse = json.loads(lsblk_out);
        if isinstance(json_parse, dict):
            for key in json_parse["blockdevices"]:
                for child in key["children"]:
                    if re.search(str(self.ventoy_device), str(child["name"])):
                        if not child["mountpoint"] == None:
                            self.device_mounted = True;
                            self.temp_dir = child["mountpoint"];
                            return child["mountpoint"];
                        else:
                            return False;
                    else:
                        return False;
        else:
            return False;

    def mount_ventoy_device (self):
        if not self.ventoy_device:
            return False;
        
        if not self.is_ventoy_mounted():
            self.temp_dir = tempfile.mkdtemp();
            try: 
                mrc = sh.mount(str(self.ventoy_device),str(self.temp_dir));
                self.device_mounted = True;
            except sh.ErrorReturnCode_32:
                sys.exit("You must be root to mount a device");

    def umount_ventoy_device (self):
        if not self.is_ventoy_mounted():
            return False;

        try:
            mrc = sh.umount(str(self.ventoy_device));
            self.device_mounted = False;
            return True;
        except:
            return False;

    def is_ventoy_mounted (self):
        if self.device_mounted:
            return True;
        else:
            return False;

    def get_ventoy_mount_dir (self):
        if self.temp_dir:
            return self.temp_dir;

    def get_iso_files (self, scan=False):

        if not self.ventoy_device:
            return False;
        if not self.device_mounted:
            return False;
    
        if self.temp_dir:
            for f in os.listdir(self.temp_dir):
                if f.endswith(".iso"):
                    self.iso_images.append(os.path.join(self.temp_dir, f));

        if len(self.iso_images) >= 1:
                return self.iso_images;
        else:
                return False;

    def delete_iso (self,iso_filename:str):
        if not self.ventoy_device:
            return False;
        if not self.device_mounted:
            return False;

        try:
            remove_iso = os.remove(iso_filename);
            return True;
        except FileNotFoundError:
            return False;

