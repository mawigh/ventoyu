# Ventoy ISO Updater

Official Ventoy Website:
https://www.ventoy.net/en/index.html

Ventoy GitHub:
https://github.com/ventoy/Ventoy

## Description

The script looks whether a partition with the label "ventoy" exists in the system and updates the ISO images on the partition if necessary.

If there is no partition with the label "ventoy", then the user can select a partition from a list.

The partition will be mounted into a temporarily created directory.

## OS Support

Currently supported images:

* grml: https://grml.org/
* Debian: https://www.debian.org/

## Dependencies

To install the dependencies system-wide, you can use the file requirements.txt

```bash
sudo python3 -m pip install -r requirements.txt
```

## How to use

You need to run this program as user root. Otherwise it cannot mount your ventoy drive.

```bash
sudo ./ventoy_update.py
```

## Update

To update the program, just pull this repository.

```bash
git pull https://github.com/mawigh/ventoy_updater.git

```
