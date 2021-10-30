# Author: Marcel-Brian Wilkowsky (mawigh)

import json;
import subprocess;
import shutil;
import re;
import sys;
import tempfile;
import os;
import logging;
import ctypes;
import ctypes.util;
import requests;
import tarfile;

class debug:
    COLOR = '\033[93m';

class ventoyl:

    _Ventoy_git_releases = "https://api.github.com/repos/ventoy/Ventoy/releases/latest";
    _Ventoy_download_URL = "https://github.com/ventoy/Ventoy/releases/download/vRELEASE/ventoy-RELEASE-linux.tar.gz";

    def __init__ (self, ventoy_device=None, debug=False):
        self.device_mounted = False;
        self.iso_images = [];
        self.ventoy_device = ventoy_device;
        self.__easysearch = True;
        self.device_mounted = False;
        self.debug = debug;

        if not self.ventoy_device:
            self.find_ventoy_device();
            if self.ventoy_device:
                ttr = self.check_ventoy_mount();
                self.mount_ventoy_device();

    def find_ventoy_device (self):

        ls_blkd = shutil.which("lsblk");
        fdevice = "";
        if ls_blkd:
            lsblk_out = subprocess.check_output([ls_blkd, "-Jnpo", "label,name,fstype"]);
            json_parse = json.loads(lsblk_out);
            search_pattern = "[V,v]entoy";
            if isinstance(json_parse, dict):
                for key in json_parse["blockdevices"]:
                    try:

                        if key["children"]:
                            for child in key["children"]:
                                if re.search(search_pattern, str(child["label"])):
                                    fdevice = child;
                                    logging.debug("Found Ventoy device: " + str(child));
                    except KeyError:
                        pass;
            else:
                return False;

            if isinstance(fdevice, dict):
                self.ventoy_device = fdevice["name"];
                self.ventoy_devicefs = fdevice["fstype"];
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
            libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True);
            libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p);

            return_val = libc.mount(str(self.ventoy_device).encode(), str(self.temp_dir).encode(), str(self.ventoy_devicefs).encode(), 0, "rw".encode());
            if return_val < 0:
                error = ctypes.get_errno();
                raise OSError(error, "Error mounting Ventoy device "+ str(self.ventoy_device) +" on "+ str(self.temp_dir) +": " + os.strerror(error));
            else:
                self.device_mounted = True;

    def umount_ventoy_device (self):
        if not self.is_ventoy_mounted():
            return False;

        umount_cmd = shutil.which("umount");
        rc = os.system(umount_cmd + " " + self.ventoy_device);
        if rc == 0:
            return True;
        else:
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

    def install_latest_Ventoy (self, gui=False):

        import platform;

        if not self.ventoy_device:
            return False;

        latest_release = requests.get(self._Ventoy_git_releases);
        latest_release = latest_release.json();
        latest_release = latest_release["tag_name"];
        latest_release = latest_release.replace("v", "");
        download_url = self._Ventoy_download_URL.replace("RELEASE", latest_release);
        file_name = download_url.split("/")[-1];

        download_dir = tempfile.mkdtemp();
        if self.debug:
            print(debug.COLOR + "Debug: Download URL: " + download_url);
            print(debug.COLOR + "Debug: Using download directory " + download_dir);

        download_file = requests.get(download_url);
        file_path = download_dir + "/" + file_name;
        if self.debug:
            print(debug.COLOR + "Debug: Trying to download file: " + file_path);
        with open(file_path, "wb") as tar_file:
            tar_file.write(download_file.content);

        if not os.path.isfile(file_path):
            sys.exit("Error: Cannot find "+ file_path +"!");
        else:
            if self.debug:
                print(debug.COLOR + "Latest Ventoy release v"+ latest_release +" successfully downloaded");

        if file_name.endswith(".tar.gz"):
            etar = tarfile.open(file_path, "r:gz");
            etar.extractall(download_dir);
            etar.close();
        elif file_name.endswiith(".tar"):
            etar = tarfile.open(file_path, "r:");
            etar.extractall(download_dir);
            etar.close();

        if gui == True:
            gui_installer_path = download_dir + "/ventoy-" + latest_release + "/VentoyGUI." + platform.uname().machine;
            if os.path.isfile(gui_installer_path):
                os.system(gui_installer_path);
            else:
                sys.exit("Error: Cannot find GUI installer " + gui_installer_path);
        else:
            shell_installer = download_dir + "/ventoy-" + latest_release + "/Ventoy2Disk.sh";
            if os.path.isfile(shell_installer):
                if self.debug:
                    print( debug.COLOR + "Debug: Launch Ventoy Installer...");
                os.system(shell_installer + " -i " + self.ventoy_device);
            else:
                sys.exit("Error: Cannot find Ventoy shell installer " + shell_installer);




