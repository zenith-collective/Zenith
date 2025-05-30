import os.path
from configparser import NoOptionError, RawConfigParser
from pathlib import Path
from sys import platform

import distro

from zenith.__version__ import __version__

CURRENT_PLATFORM = platform
if platform in ["win32", "cygwin"]:
    CURRENT_PLATFORM = "windows"
elif platform.startswith("darwin"):
    CURRENT_PLATFORM = "macos"
elif platform.startswith("linux") or platform.startswith("freebsd"):
    CURRENT_PLATFORM = distro.like()

INSTALL_DIR = os.path.join(str(Path.home()), ".zenith")
CONFIG_FILE = os.path.join(INSTALL_DIR, "zenith.cfg")
GITHUB_PATH = "xShadyy/zenith"

DEFAULT_CONFIG = {
    "version": __version__,
    "agreement": "false",
    "ssh_clone": "false",
    "os": CURRENT_PLATFORM,
    "host_file": "hosts.txt",
    "usernames_file": "usernames.txt",
}


def get_config() -> RawConfigParser:
    config = RawConfigParser()
    if not os.path.exists(INSTALL_DIR):
        os.mkdir(INSTALL_DIR)
    if not os.path.exists(CONFIG_FILE):
        config["zenith"] = DEFAULT_CONFIG
        with open(CONFIG_FILE, "w", encoding="utf-8") as configfile:
            config.write(configfile)
    config.read(CONFIG_FILE)
    check_config(config)
    if config.get("zenith", "version") != __version__:
        config.set("zenith", "version", __version__)
        write_config(config)
    return config


def write_config(config: RawConfigParser) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def check_config(config: RawConfigParser) -> None:
    for key in DEFAULT_CONFIG:
        try:
            config.get("zenith", key)
        except NoOptionError:
            config.set("zenith", key, DEFAULT_CONFIG.get(key))
    write_config(config)
