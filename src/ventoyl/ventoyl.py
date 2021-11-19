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

class debugp:
    COLOR = '\033[93m';
    ENDC = '\033[0m';

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

        self.log_file = os.path.dirname(__file__) + "/ventoyl.log";
        if self.debug == True:
            loglevel = logging.DEBUG;
        else:
            loglevel = logging.INFO;

        logging.basicConfig(filename=self.log_file, format="[%(levelname)s - %(asctime)s] %(filename)s - %(funcName)s: %(message)s", encoding="utf-8", level=loglevel);

        if not isinstance(ventoy_device, str):
            rc = self.findVentoyDevice();
            if not rc == False:
                logging.info("Found the Ventoy device: " + str(rc["name"]));
            
        rc = self.checkVentoyMount();
        if rc == -1:
            if isinstance(ventoy_device, str):
                logging.error("The specified Ventoy device ("+str(ventoy_device)+") could not be found on your system.");
                raise OSError("The specified Ventoy device could not be found on your system.");

        try:
            self.mountVentoyDevice();
        except:
            if isinstance(self.ventoy_device, str):
                logging.debug("The specified device ("+str(self.ventoy_device)+") could not be found.");
            
    def findVentoyDevice (self):

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

    def checkVentoyMount (self):
        if not self.ventoy_device:
            self.findVentoyDevice();

        lsblk_out = subprocess.check_output(["lsblk","-Jnpo","name,mountpoint"]);
        json_parse = json.loads(lsblk_out);
        if isinstance(json_parse, dict):
            for key in json_parse["blockdevices"]:
                try:
                    test = key["children"];
                except KeyError:
                    return False;
                for child in key["children"]:
                    if re.search(str(self.ventoy_device), str(child["name"])):
                        if not child["mountpoint"] == None:
                            self.device_mounted = True;
                            self.temp_dir = child["mountpoint"];
                            self.ventoy_config_dir = self.temp_dir + "/ventoy/";
                            return child["mountpoint"];
                        else:
                            return False;
                    else:
                        return -1;
        else:
            return False;

    def getVentoyConfig (self):

        if not self.isVentoyMounted():
            self.mountVentoyDevice();

        if not os.path.isdir(self.ventoy_config_dir):
            return False;
        
        config_file = open(self.ventoy_config_dir + "/ventoy.json", "r");
        if config_file:
            return json.load(config_file);

    def getVentoylLogFile (self):
        
        if self.log_file:
            return str(self.log_file);
        else:
            return False;

    def mountVentoyDevice (self):
        if not self.ventoy_device:
            return False;
        
        if not self.isVentoyMounted():
            self.temp_dir = tempfile.mkdtemp();
            libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True);
            libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p);

            return_val = libc.mount(str(self.ventoy_device).encode(), str(self.temp_dir).encode(), str(self.ventoy_devicefs).encode(), 0, "rw".encode());
            if return_val < 0:
                logging.error("Could not mount your Ventoy device "+str(self.ventoy_device)+"!");
                return False;
            else:
                logging.info("Successfully mounted Ventoy device "+str(self.ventoy_device)+" on " + str(self.temp_dir));
                self.device_mounted = True;
                return True;

    def umountVentoyDevice (self):
        if not self.isVentoyMounted():
            return False;

        umount_cmd = shutil.which("umount");
        rc = os.system(umount_cmd + " " + self.ventoy_device);
        if rc == 0:
            logging.info("Successfully umounted Ventoy device "+str(self.ventoy_device)+"!");
            return True;
        else:
            logging.error("Error trying to umount your Ventoy device "+str(self.ventoy_device)+"!");
            return False;

    def isVentoyMounted (self):
        if self.device_mounted:
            return True;
        else:
            return False;

    def getVentoyMountDir (self):
        if self.temp_dir:
            return self.temp_dir;

    def getISOFiles (self, scan=False):

        if not self.ventoy_device:
            return [];
        if not self.device_mounted:
            return [];
    
        if self.temp_dir:
            for f in os.listdir(self.temp_dir):
                if f.endswith(".iso"):
                    self.iso_images.append(os.path.join(self.temp_dir, f));

        if len(self.iso_images) >= 1:
                return self.iso_images;
        else:
                return [];

    def deleteISO (self,iso_filename:str):
        if not self.ventoy_device:
            return False;
        if not self.device_mounted:
            return False;

        try:
            remove_iso = os.remove(iso_filename);
            logging.info("Successfully deleted ISO file "+str(iso_filename));
            return True;
        except FileNotFoundError:
            return False;

    def installLatestVentoy (self, gui=False, force=False):

        import platform;

        latest_release = requests.get(self._Ventoy_git_releases);
        latest_release = latest_release.json();
        latest_release = latest_release["tag_name"];
        latest_release = latest_release.replace("v", "");
        download_url = self._Ventoy_download_URL.replace("RELEASE", latest_release);
        file_name = download_url.split("/")[-1];

        download_dir = tempfile.mkdtemp();
        logging.debug("Download "+download_url+" to directory "+download_dir);

        download_file = requests.get(download_url);
        file_path = download_dir + "/" + file_name;
        with open(file_path, "wb") as tar_file:
            tar_file.write(download_file.content);

        if not os.path.isfile(file_path):
            logging.error("Cannot find file "+file_path+"!");
            sys.exit("Error: Cannot find "+ file_path +"!");
        else:
            logging.debug("Latest Ventoy release v"+ latest_release +" successfully downloaded");

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
                logging.error("Cannot find the GUI installer ("+gui_installer_path+"). You may want to creat an issue on https://github.com/mawigh/ventoyu/issues");
                return False;
        else:
            shell_installer = download_dir + "/ventoy-" + latest_release + "/Ventoy2Disk.sh";
            if os.path.isfile(shell_installer):
                logging.debug("Launching the Ventoy Shell Installer "+shell_installer+"...");
                    
                cmd = shell_installer + " -i " + self.ventoy_device;
                if force == True:
                    cmd = shell_installer + " -I " + self.ventoy_device;
                os.system(cmd);
            else:
                logging.error("Cannot find the Ventoy shell installer " + shell_installer);
                return False;

    def configureVentoyPlugin (self, plugintype=None):
        
        if not self.ventoy_device:
            return False;
        if not self.isVentoyMounted():
            rc = self.mountVentoyDevice();
            if rc == False:
                return False;

        test = self.getVentoyConfig();

        if not os.path.isdir(self.ventoy_config_dir):
            os.mkdir(self.ventoy_config_dir);
            logging.debug("Created Ventoy config directory: " + self.ventoy_config_dir);

        available_types = ["theme"];

        if not plugintype in available_types:
            logging.error("Plugintype "+str(plugintype)+" is not available!");
            return False;

        if plugintype == "theme":
            #if not os.path.isfile(self.ventoy_config_dir + "/ventoy.json"):
            passed_arguments = {"theme": {"file": "", "gfxmode": ""}};
            
            for argument, value in passed_arguments[str(plugintype)].items():
                print("Needed value for: " + str(argument));
                qarg = input(str(argument) + ": ");
                passed_arguments.update({"theme": { str(argument): str(qarg)}});
                print(passed_arguments);

