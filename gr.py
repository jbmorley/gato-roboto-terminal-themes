#!/usr/bin/env python3

import glob
import os
import random
import subprocess
import sys
import time

import click

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIRECTORY = os.path.join(ROOT_DIRECTORY, "profiles")


SCRIPT = """
tell application "Terminal"
    set current settings of window 1 to settings set "%s"
end tell
"""

PROFILES = {
    "bark": "GR Bark",
    "chewed-gum": "GR Chewed Gum",
    "coffee-stain": "GR Coffee Stain",
    "default": "GR Default",
    "goop": "GR Goop",
    "grape": "GR Grape",
    "gris": "GR Gris",
    "meowtrix": "GR Meowtrix",
    "nicotine": "GR Nicotine",
    "port": "GR Port",
    "soft": "GR Soft",
    "starboard": "GR Starboard",
    "swamp-matcha": "GR Swamp Matcha",
    "tamagato": "GR Tamagato",
    "urine": "GR Urine",
    "virtual-cat": "GR Virtual Cat",
}


class Chdir(object):
    
    def __init__(self, path):
        self.path = os.path.abspath(path)
    
    def __enter__(self):
        self.pwd = os.getcwd()
        os.chdir(self.path)
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.pwd)


def set_profile(profile):
    subprocess.check_call(["osascript", "-e", SCRIPT % PROFILES[profile]])


@click.group()
def cli():
    pass


@cli.command()
@click.option("--sleep", default=2, help="length of time to sleep")
def demo(sleep):
    while True:
        for profile in PROFILES.keys():
            set_profile(profile)
            columns = os.get_terminal_size().columns
            sys.stdout.write(f"\r".ljust(columns))
            sys.stdout.write(f"\rkiki % gr set {profile} ")
            time.sleep(sleep)


@cli.command()
@click.argument("theme")
def set(theme):
    set_profile(theme)
    
    
@cli.command("random")
def command_random():
    theme = random.choice(list(PROFILES.keys()))
    set_profile(theme)
    
    
@cli.command()
def install():
    with Chdir(PROFILES_DIRECTORY):
        profiles = glob.glob("*.terminal")
        subprocess.check_call(["open"] + profiles)


if __name__ == '__main__':
    cli()
