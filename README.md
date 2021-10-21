# Ventoy Updater

Official Ventoy Website:
https://www.ventoy.net/en/index.html

Ventoy on GitHub:
https://github.com/ventoy/Ventoy

# Table of Contents
- [Ventoy Updater](#ventoy-updater)
- [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [OS Support](#os-support)
  - [Install Ventoy Updater](#install-ventoy-updater)
  - [How to](#how-to)
    - [Install new images](#install-new-images)
    - [Add a new ISO download source](#add-a-new-iso-download-source)
    - [Get help](#get-help)

---

## Description

The Ventoy Updater can be used to install new, update or remove ISO files on the Ventoy device.

## OS Support

Currently supported images:

| Operating system | URL |
| ---------------- | --- |
| Debian (arm64) | https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/ |
| Debian (amd64) | https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/ |
| Grml | https://download.grml.org/" |
| Ubuntu (18.04, 20.04, 21.04) | https://ftp.halifax.rwth-aachen.de/ubuntu-releases/ |
| Manjaro (XFCE, KDE) | https://manjaro.org/downloads/official/ |
| Finnix 123 | https://www.finnix.org/releases/123/ |

With the option `add-url` you have the possibility to add new ISO sources.

## Install Ventoy Updater

```bash
$ pip3 install ventoy_updater
```

**Note:** You may want to install with option `--user`.

## How to

### Install new images

```bash
$ sudo ventoyu install
```

### Add a new ISO download source

**Tip:** Before add a new URL, check it with `check-url`.

```bash
$ sudo ventoyu add-url --url <URL>
```

### Get help

For more information type `ventoyu --help`.
