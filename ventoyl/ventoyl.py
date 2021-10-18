import json;
import shutil;
import re;
import sys;

class ventoyl:

    def __init__ (self, ventoy_device=None):
        self.device_mounted = False;
        self.iso_images = [];
        self.__easysearch = True;

        if not ventoy_device is None:
            device = find_ventoy_device();
            mount_ventoy_device(device);

        # check url json file

    def find_ventoy_device (self):
        import subprocess;
        
        ls_blkd = shutil.which("lsblk");
        fdevice = "";
        if ls_blkd:
            lsblk_out = subprocess.check_output([ls_blkd, "-Jnpo", "label,name"]);
            json_parse = json.loads(lsblk_out);
            search_pattern = "[V,v]entoy";
            if isinstance(json_parse, dict):
                for key in json_parse["blockdevices"]:
                    for child in key["children"]:
                        if re.search(search_pattern, str(child["label"])):
                            fdevice = child;
            else:
                return False;

            if isinstance(fdevice, dict):
                self.ventoy_device = fdevice["name"];
                return fdevice;
            else:
                return False;
        else:
            return False;

    def mount_ventoy_device (self):
        if not self.ventoy_device:
            return False;

    def list_iso_files (self, scan=False):

        if self.ventoy_device is None:
            return False;
        if not self.device_mounted:
            return False;

        # scan for new iso files
        # SCAN HERE
        if scan == True:
            pass;

        print("Found following ISO images:");
        for i in iso_images:
            print("+ " + i);
        print("###########################");

    def downloadIso (self, url):
        pass;

    def deleteIso (self):
        pass;

test = ventoyl();
tt = test.find_ventoy_device();
if tt:
    print(tt);
else:
    print("Nicht gefunden :-(");
