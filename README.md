# Ventoy Updater

Official Ventoy Website:
https://www.ventoy.net/en/index.html

Ventoy GitHub:
https://github.com/ventoy/Ventoy

## Description

https://www.crummy.com/software/BeautifulSoup/

## OS Support

Currently supported:

* grml: https://grml.org/
* Debian: https://www.debian.org/

## Dependencies

To install the dependencies, you can use the file requirements.txt

```bash
python3 -m pip install -r requirements.txt
```

## How to use

You need to run this program as user root. Otherwise it cannot mount your ventoy drive.

```bash
sudo ./ventoy_update.py
```
