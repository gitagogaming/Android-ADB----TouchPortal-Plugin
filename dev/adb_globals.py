
#from android_adb import *
from asyncio.windows_events import NULL
from concurrent.futures import thread
from ppadb.client import Client as AdbClient
from io import StringIO
import sys
import TouchPortalAPI as TP


from asyncio.windows_events import NULL
from concurrent.futures import thread
import time
import re
import threading 
import adb_commadns
from argparse import ArgumentParser
from logging import (getLogger, Formatter, NullHandler, FileHandler, StreamHandler, DEBUG, INFO, WARNING)



device_list = []


global battery_states
battery_states = {
"temperature": "",
"level": "",
"voltage":"",
"status":"",
"health": "",
"AC powered": "",
"USB powered": "",
"Wireless powered":"",
"present": ""}




sleep_states = {
    'mHoldingWakeLockSuspendBlocker': '',
    'mHoldingDisplaySuspendBlocker': ''}




def bat_state_conver(choice, num):
          #  """
      #  获取电池充电状态
      #  BATTERY_STATUS_UNKNOWN：未知状态
      #  BATTERY_STATUS_CHARGING: 充电状态
      #  BATTERY_STATUS_DISCHARGING: 放电状态
      #  BATTERY_STATUS_NOT_CHARGING：未充电
      #  BATTERY_STATUS_FULL: 充电已满
      #  """
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
    for x in device_list:
        if name in f"{x['Manufacturer']} {x['Model']}":
            return x


def kb2mb(num):
    return int(num) // 1024
