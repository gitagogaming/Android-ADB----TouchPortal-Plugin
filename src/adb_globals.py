

from asyncio.windows_events import NULL
from concurrent.futures import thread
from ppadb.client import Client as AdbClient
from io import StringIO
import TouchPortalAPI as TP
from asyncio.windows_events import NULL
from concurrent.futures import thread
from argparse import ArgumentParser
from logging import (getLogger, Formatter, NullHandler, FileHandler, StreamHandler, DEBUG, INFO, WARNING)


### FROM MAIN IMPORTS
from asyncio.windows_events import NULL
from concurrent.futures import thread
import TouchPortalAPI as TP
import time
import threading
import re
import sys
from ctypes import windll
import subprocess

### These were needed for Update check
import requests
import base64
import json


""" Moved other variables to device_states.py where they are used, device list is used globally"""
battery_states = {}
device_names = []
device_list = {}


sleep_states = {
    'mHoldingWakeLockSuspendBlocker': '',
    'mHoldingDisplaySuspendBlocker': ''}



def bat_state_conver(choice, num):
    
    ## This converts the numbers given by ADB into a string thats readable
    if choice == "status":
        statusDict = {1 : "UNKNOWN",
                        2 : "CHARGING",
                        3 : "DISCHARGING",
                        4 : "NOT_CHARGING",
                        5 : "FULL"}
        result = statusDict[int(num)]
        
    if choice == "health":
        healthDict = {1 : "UNKNOWN",
                        2 : "GOOD",
                        3 : "OVERHEAT",
                        4 : "DEAD",
                        5 : "OVER VOLTAGE",
                        6 : "unspecified failure",
                        7: "COLD"}
        result = healthDict[int(num)]
        
    return result


def match_device(name):
    """ Returns the device ID associated with the device name"""
    return device_list[name]['ID']


def kb2mb(num):
    return int(num) // 1024




def out(command):
    """Power Shell Func
    - Checking Devices Test
    """
    systemencoding = windll.kernel32.GetConsoleOutputCP()
    systemencoding= f"cp{systemencoding}"
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    result = str(output.stdout.decode(systemencoding))
    for device in result.splitlines():
        if device.endswith('\tdevice'):
            result= device.split('\t')[0]
        return result

