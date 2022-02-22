from asyncio.windows_events import NULL
from concurrent.futures import thread
import time
import re
import threading 
from ppadb.client import Client as AdbClient


#### https://dev.to/larsonzhong/most-complete-adb-commands-4pcg#turn-on-off-the-screen  
### some shortcuts for calling n such
commands = [{
    "Turn Off Screen": "input keyevent 223",
    "Turn On Screen": "input keyevent 224",
    "Power Button Toggle": "input keyevent 26",
    "Swipe to Unlock": "input swipe 300 1000 300 500",   ## start x, end x, start y, end y
    "Input Text": "input text (text here)",
    "Increase Volume": "input keyevent 24",
    "Decrease Volume": "input keyevent 25",
    "Take Picture": "input keyevent 27",  # input keyevent KEYCODE_CAMERA"
    "Toggle Mute Volume": "input keyevent 164",
    "Home Key": "input keyevent 3",
    "Return Key": "input keyevent 4",
    "Menu": "input keyevent 82",
    "Switch Applications": "input keyevent 187",
    "Calendar": "input keyevent 208" ,
    "Reduce Screen Brightness": "input keyevent 220",
    "Increase Screen Brightness": "input keyevent 221",
    "Voice Assistant": "input keyevent 231",
    "Device Model": "getprop ro.product.model",
    "Screen Size": "wm size",
    "Screen Density": "wm density",
    "Android Version": "getprop ro.build.version.release",
    "CPU INFO": "cat /proc/cpuinfo",   ### use func above to pull details needed like processor, 
    "MEM INFO": "cat /proc/meminfo",
    "Screenshot Device": "exec-out screencap -p> sc.png",
    "Pull Image to PC": "screencap -p /sdcard/sc.png",  ##  doesnt quite work?
    "Screen Record Phone": "screenrecord /sdcard/filename.mp4",   ## -- "--bit-rate 2000" "--time-limit 60" "--size 300x300"
    "Reboot Device": "reboot",

}]






""" OPEN WEBSITE / BROWSER """
#device.shell("am start -a android.intent.action.VIEW -d http://www.stackoverflow.com")
#device.shell("am start -n com.android.chrome/com.google.android.apps.chrome.Main \ -a android.intent.action.VIEW -d 'http://www.stackoverflow.com'")

def kb2mb(num):
    return int(num) // 1024



### MAIN FUNCTIONS ###
""" Gets Battery Level, Temp, Status, Health"""
        # get_battery_level_and_temperature()
        
""" Gets Total Memory, Free Memory"""        
        # mem_info()
        
""" Gets Overall Device Info / Screen Size / Manufac / Android Version etc """
      # get_device_info


def get_screen_info(device_choice):
    density = device_choice.shell('wm density').split(":")[-1].split("\n")[0]
    size = device_choice.shell('wm size').split(":")[-1].split("\n")[0]
    model = device_choice.shell('getprop ro.product.model').split("\n")[0]
    manufac = device_choice.shell('getprop ro.product.manufacturer').split("\n")[0]
    board  = device_choice.shell('getprop ro.product.board').split("\n")[0]
    hardware = device_choice.shell('getprop ro.hardware').split("\n")[0]
    android_version = device_choice.shell('getprop ro.build.version.release').split("\n")[0]
    
    return {"Version": android_version, "Hardware": hardware, "Board": board, "Manufacturer": manufac, "Model": model, "Screen Size": size, "Screen Density":density}
    

def get_battery_status(device):
      #  """
      #  获取电池充电状态
      #  BATTERY_STATUS_UNKNOWN：未知状态
      #  BATTERY_STATUS_CHARGING: 充电状态
      #  BATTERY_STATUS_DISCHARGING: 放电状态
      #  BATTERY_STATUS_NOT_CHARGING：未充电
      #  BATTERY_STATUS_FULL: 充电已满
      #  """
        health = device.shell("dumpsys battery | grep health")
        status = device.shell("dumpsys battery | grep status")
        statusDict = {1 : "UNKNOWN",
                      2 : "CHARGING",
                      3 : "DISCHARGING",
                      4 : "NOT_CHARGING",
                      5 : "FULL"}
        
        healthDict = {1 : "UNKNOWN",
                      2 : "GOOD",
                      3 : "OVERHEAT",
                      4 : "DEAD",
                      5 : "OVER VOLTAGE",
                      6 : "unspecified failure",
                      7: "COLD"}
        
        newhealth = re.match(r'.*health: (\d+).*', health, re.DOTALL)
        newhealth = int(newhealth.group(1))
        return {"Status":statusDict[int(status.split(":")[-1])], "Health": healthDict[newhealth]}



#print(device.shell("dumpsys battery | grep health"))
### Find all the ADB Stuff on the Device
#print(device.shell('dumpsys | grep "DUMP OF SERVICE"'))


#print(device.shell('/sys/class/power_supply/battery/'))


def get_battery_level_and_temperature(device, format = "Celcius"):
    print("we in ?")
    """Return device's battery and temperature levels."""
    output = device.shell('dumpsys battery')
    

    # Get battery level.
    m_battery_level = re.match(r'.*level: (\d+).*', output, re.DOTALL)
    if not m_battery_level:
        m_battery_level = "None"

    # Get battery temperature.
    m_battery_temperature = re.match(r'.*temperature: (\d+).*', output, re.DOTALL)
    if not m_battery_temperature:
        m_battery_temperature = "None"
    
    # Get Battery Voltage
    m_voltage_level = re.match(r'.*voltage: (\d+).*', output, re.DOTALL)
    if not m_voltage_level:
        m_voltage_level = "None"

    # Get Powered Status
    ac_powered_status = re.match(r'.*AC powered: (\d+).*', output, re.DOTALL)
    if not ac_powered_status:
            ac_powered_status= "None"

    # Get Powered Status
    usb_powered_status = re.match(r'.*USB powered: (\d+).*', output, re.DOTALL)
    if not usb_powered_status:
            usb_powered_status = "None"

    level = int(m_battery_level.group(1))
    temperature = float(m_battery_temperature.group(1)) / 10.0
    voltage = int(m_voltage_level.group(1))
    
    bat_status = get_battery_status(device) 
   # 
    Fahrenheit = (temperature * 9/5) + 32
   # #Celsius = (Fahrenheit - 32) * 5/9
    if format == "Celcius":
        return {'Level': level, 
                'Status': bat_status['Status'],
                'Temperature': f"{temperature} °C",
                "Voltage": f"{voltage} mV",
                'Health': bat_status['Health']
                } 
        
    if format == "Fahrenheit":
            return {'Level': level, 
                'Status': bat_status['Status'],
                'Temperature': f"{Fahrenheit} °F",
                "Voltage": f"{voltage} mV",
                'Health': bat_status['Health']
                } 
        
#print(get_battery_level_and_temperature())



"""" TEST WIRELESS ADB CONNECTION WITH LAPTOP """


#### one line screenshot + save 'screencap -p | sed "s/\r$//"> sc.png'   - but read only file system on pc??
#device.shell('input keyevent 15')


### Swipe to Unlock

def unlock_device(device):
    device.shell(commands[0]['Turn On Screen'])
    time.sleep(0.2)
    device.shell(commands[0]['Swipe to Unlock'])
    time.sleep(0.2)
    device.shell("input keyevent 15")
    device.shell("input keyevent 13")
    device.shell("input keyevent 15")
    device.shell("input keyevent 14")




def get_mem_info(device):
    mem_list = ['MemTotal', 'MemAvailable', ]
    mem_check = device.shell("cat /proc/meminfo")
    split = mem_check.splitlines()
    memdict={}
    
    #print(device.shell('top -m 10'))   ## keeps adb open?
    #print(device.shell(r'top -n 1 -o %MEM'))
    for line in split:
        for item in mem_list:
            if item in line:
                size = kb2mb(line.split(" ")[-2])
                memdict[item] = f"{size} MB"
    return memdict
from pprint import pprint
###   print(get_screen_info())
###   print(get_mem_info())
###   print(get_battery_level_and_temperature(format="Fahrenheit"))


def connect():
    device_list = []
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    #client.remote_connect("192.168.0.106", 5555)
    devices = client.devices() 
    if len(devices) == 0:
        print('No devices')
        quit()
        
    count = 0
    a={}
 

  # for x in devices:
  #     key = f"device{count}"
  #     value = x
  #     a[key] = value
  #     
  #     ### Pulling Device Details
  #     device_info = get_screen_info(value)
  #     
  #     device_dict = {f"Device": value}
  #     device_dict.update(device_info)
  #     device_list.append(device_dict)
  #     count=count+1
        
  # for x in device_list:
  #     print(f'Connected to {x["Device"]}')
  #     print(get_battery_level_and_temperature(device=x['Device']))
    
    pprint(device_list, sort_dicts=False)
    return device, client


if __name__ == '__main__':
    device, client =  connect()




















### messed up import    import argparse
### messed up import    import errno
### messed up import    import itertools
### messed up import    import os
### messed up import    import re
### messed up import    # import traceback
### messed up import    # import logging
### messed up import    import subprocess
### messed up import    import shutil
### messed up import    from subprocess import check_output
### messed up import    from time import strftime
### messed up import    
### messed up import    # openpyxl sample:
### messed up import    # https://github.com/theorchard/openpyxl/tree/master/openpyxl/sample
### messed up import    # https://github.com/ericgazoni/openpyxl/tree/master/openpyxl/sample
### messed up import    from openpyxl import Workbook
### messed up import    from openpyxl.utils import get_column_letter
### messed up import    #rom openpyxl.compat import range
### messed up import    from openpyxl.styles import Color, PatternFill, Font, Alignment, Border, Side
### messed up import    
### messed up import    # Add the PATH environment variable to your Run Configuration
### messed up import    # (Run->Edit Configurations) like this: PATH=/local/bin:$PATH
### messed up import    #
### messed up import    # cmd_meminfo = "/local/bin/adb shell dumpsys meminfo"
### messed up import    
### messed up import    # The shell argument (which defaults to False) specifies whether to use the shell as
### messed up import    # the program to execute. If shell is True, it is recommended to pass args as a string
### messed up import    # rather than as a sequence.
### messed up import    #
### messed up import    # cmd_meminfo = ["adb", "shell", "dumpsys", "meminfo", "|", "tee", "meminfo.txt"]
### messed up import    
### messed up import    # In practice it means you can pass the arguments as a string, instead of a list,
### messed up import    # as check_output() would normally expect.
### messed up import    #
### messed up import    # p = Popen(cmd_meminfo, stdout=PIPE, shell=True)
### messed up import    # output, err = p.communicate()
### messed up import    
### messed up import    CMD_PACKAGES = "adb shell pm list packages -f"
### messed up import    CMD_MEMINFO = "adb shell dumpsys meminfo"
### messed up import    # used for generating dir's name
### messed up import    CMD_DEVICE = "adb shell getprop ro.product.device"
### messed up import    CMD_VERSION = "adb shell getprop ro.build.version.incremental"
### messed up import    
### messed up import    SYSTEM_PROC_WHITE_LIST = ['system', 'android.process.media', 'android.process.acore']
### messed up import    GOOGLE_PROC_WHITE_LIST = ['com.google', 'com.android.facelock', 'com.android.vending', 'com.android.chrome']
### messed up import    
### messed up import    QCOM_TITLE = ['Memory', 'Total RAM', 'Free RAM', 'Kernel', 'Native',
### messed up import             'Module', 'GMS', 'Qcom', 'Third', 'System apps',
### messed up import             'Packages', 'installed', 'gms', 'qcom', 'third', 'system']
### messed up import    
### messed up import    MTK_TITLE = ['Memory', 'Total RAM', 'Free RAM', 'Kernel', 'Native',
### messed up import                 'Module', 'GMS', 'MTK', 'Third', 'System apps',
### messed up import                 'Packages', 'installed', 'gms', 'mtk', 'third', 'system']
### messed up import    
### messed up import    PLATFORM_PKGS = []
### messed up import    platform_flag = 0
### messed up import    
### messed up import    meminfo_file = 'meminfo.txt'
### messed up import    packages_file = 'packages.txt'
### messed up import    out_parse_table = 'parse_table.txt'
### messed up import    out_parse_xlsx = 'parse_diff_info.xlsx'
### messed up import    
### messed up import    original_dir = ""
### messed up import    diff_dir = ""
### messed up import    
### messed up import    
### messed up import    def main():
### messed up import        global original_dir, diff_dir, out_parse_table
### messed up import        global platform_flag, PLATFORM_PKGS
### messed up import    
### messed up import        # Print program usage example with argparse module
### messed up import        # http://stackoverflow.com/a/10930713/4710864
### messed up import        # https://docs.python.org/dev/library/argparse.html#argparse.RawDescriptionHelpFormatter
### messed up import        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog='''
### messed up import    Example of use:
### messed up import      platform: 0(Qualcomm)/1(MTK)
### messed up import      comparison mode: $ python parse_meminfo.py [-p platform:0/1] -f original_dir -d diff_dir
### messed up import      analysis mode:   $ python parse_meminfo.py [-p platform:0/1] [-o outdir]
### messed up import    ''')
### messed up import        parser.add_argument('-p', '--platform', nargs='?', default='0', help="0: Qualcomm; 1: MTK")
### messed up import        parser.add_argument('-f', '--file', nargs='*', help="the original directory's name")
### messed up import        parser.add_argument('-d', '--diff', nargs='*', help="the diff directory's name")
### messed up import        parser.add_argument('-o', '--outdir', nargs='?',  # default='parse_result.txt',
### messed up import                            help='For analysis mode, save result in the custom directory')
### messed up import        args = parser.parse_args()
### messed up import        # 0: qualcomm; 1: MTK
### messed up import        platform_flag = args.platform
### messed up import        if int(platform_flag):
### messed up import            PLATFORM_PKGS = ["com.mediatek", "com.mtk"]
### messed up import        else:
### messed up import            PLATFORM_PKGS = ["com.qti", "com.qualcomm"]
### messed up import    
### messed up import        if args.file is None:
### messed up import            # prepare output directory's name
### messed up import            try:
### messed up import                if args.outdir is None:
### messed up import                    device_name = check_output(CMD_DEVICE, shell=True)
### messed up import                    version_name = check_output(CMD_VERSION, shell=True)
### messed up import                    # http://stackoverflow.com/a/27866830/4710864
### messed up import                    cur_time = strftime("%m%d%H%M")
### messed up import                    outdir = "{}_{}_{}".format(device_name.strip(), version_name.strip(), cur_time.strip())
### messed up import                else:
### messed up import                    outdir = str(args.outdir)
### messed up import    
### messed up import                # Run command with arguments and return its output as a byte string.
### messed up import                file_meminfo = check_output(CMD_MEMINFO, shell=True)
### messed up import                write_to_file("{}/{}".format(outdir, meminfo_file), file_meminfo)
### messed up import                system_mem, filtered_procs_mem = get_file_meminfo(file_meminfo)
### messed up import    
### messed up import                installed_pkgs_str = check_output(CMD_PACKAGES, shell=True)
### messed up import                write_to_file("{}/{}".format(outdir, packages_file), installed_pkgs_str)
### messed up import                pkgs_dic = get_packages_dic(installed_pkgs_str)
### messed up import            except subprocess.CalledProcessError:
### messed up import                print ("*** Error: please check your device state.\n")
### messed up import                # Programatically stop execution of python script
### messed up import                raise SystemError(0)
### messed up import    
### messed up import            groups_mem_kb, groups_mem = get_procs_attr_group(filtered_procs_mem, pkgs_dic)
### messed up import            out_parse_table = "{}/{}".format(outdir, out_parse_table)
### messed up import            print_mem_table(out_parse_table, system_mem, groups_mem_kb, pkgs_dic)
### messed up import            print ("Finished: ##The output files is in: {}/".format(os.path.dirname(out_parse_table)))
### messed up import        else:
### messed up import            original_dir = args.file[0]
### messed up import            diff_dir = args.diff[0]
### messed up import            meminfo_1 = "{}/{}".format(original_dir, meminfo_file)
### messed up import            pm_list_1 = "{}/{}".format(original_dir, packages_file)
### messed up import            meminfo_2 = "{}/{}".format(diff_dir, meminfo_file)
### messed up import            pm_list_2 = "{}/{}".format(diff_dir, packages_file)
### messed up import    
### messed up import            # change output file to .xlsx
### messed up import            # base = ntpath.basename(outfile)
### messed up import            # outfile = "{}.xlsx".format(ntpath.splitext(base)[0])
### messed up import    
### messed up import            system_mem_1, filtered_procs_mem_1 = get_file_meminfo(read_file(meminfo_1))
### messed up import            system_mem_2, filtered_procs_mem_2 = get_file_meminfo(read_file(meminfo_2))
### messed up import            pkgs_dic_1 = get_packages_dic(read_file(pm_list_1))
### messed up import            pkgs_dic_2 = get_packages_dic(read_file(pm_list_2))
### messed up import            groups_mem_kb_1, groups_mem_1 = get_procs_attr_group(filtered_procs_mem_1, pkgs_dic_1)
### messed up import            groups_mem_kb_2, groups_mem_2 = get_procs_attr_group(filtered_procs_mem_2, pkgs_dic_2)
### messed up import            print_diff_table(system_mem_1, system_mem_2, pkgs_dic_1, pkgs_dic_2,
### messed up import                             groups_mem_kb_1, groups_mem_kb_2, groups_mem_1, groups_mem_2)
### messed up import    
### messed up import            print ("************* system meminfo*********************")
### messed up import            print (system_mem_1)
### messed up import            print ("\n**************************************************")
### messed up import            print (system_mem_2)
### messed up import            print ("\n\n************* process meminfo ********************")
### messed up import            print ("filtered_procs_mem_1:")
### messed up import            for k, v in sorted(filtered_procs_mem_1.items(), key=lambda x: (-int(x[1]), x[0])):
### messed up import                print (' {1}:  {0}'.format(k, v))
### messed up import    
### messed up import            print ("\n**************************************************")
### messed up import            print ("filtered_procs_mem_2:")
### messed up import            for k, v in sorted(filtered_procs_mem_2.items(), key=lambda x: (-int(x[1]), x[0])):
### messed up import                print (' {1}:  {0}'.format(k, v))
### messed up import    
### messed up import            print ("\n\n***************** packages ***********************")
### messed up import            print ("pkgs_dic_1:")
### messed up import            for key in pkgs_dic_1:
### messed up import                print (key, ":")
### messed up import                for pkg in sorted(pkgs_dic_1[key]):
### messed up import                    print ("** ", pkg)
### messed up import                print ('len=', len(pkgs_dic_1[key]))
### messed up import    
### messed up import            print ("\n**************************************************")
### messed up import            print ("pkgs_dic_2:")
### messed up import            for key in pkgs_dic_2:
### messed up import                print (key, ":")
### messed up import                for pkg in sorted(pkgs_dic_2[key]):
### messed up import                    print ("** ", pkg)
### messed up import                print ('len=', len(pkgs_dic_2[key]))
### messed up import    
### messed up import            print ("\n\n************** group meminfo kb ******************")
### messed up import            print (groups_mem_kb_1)
### messed up import            print ("\n**************************************************")
### messed up import            print (groups_mem_kb_2)
### messed up import            print ("\n\n**************group meminfo ***********************")
### messed up import            print ("groups_mem_1:")
### messed up import            for key in groups_mem_1:
### messed up import                print (key, ":")
### messed up import                for pkg in sorted(groups_mem_1[key]):
### messed up import                    print ("** ", pkg)
### messed up import                print ('len=', len(groups_mem_1[key]))
### messed up import            print ("\n**************************************************")
### messed up import            print ("groups_mem_2:")
### messed up import            for key in groups_mem_2:
### messed up import                print (key, ":")
### messed up import                for pkg in sorted(groups_mem_2[key]):
### messed up import                    print ("** ", pkg)
### messed up import                print ('len=', len(groups_mem_2[key]))
### messed up import    
### messed up import    
### messed up import    # Most pythonic way to delete a file which may not exist
### messed up import    # http://stackoverflow.com/a/10840586/4710864
### messed up import    def silent_remove(filename):
### messed up import        try:
### messed up import            if os.path.isdir(filename):
### messed up import                # How do I delete a file or folder in Python?
### messed up import                # http://stackoverflow.com/a/6996628/4710864
### messed up import                shutil.rmtree(filename)
### messed up import            else:
### messed up import                os.remove(filename)
### messed up import        except OSError as exc:  # this would be "except OSError, e:" before Python 2.6
### messed up import            if exc.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
### messed up import                raise  # re-raise exception if a different error occured
### messed up import    
### messed up import    
### messed up import    def read_file(filename):
### messed up import        with open(filename, 'r') as fp:
### messed up import            return fp.read()
### messed up import    
### messed up import    
### messed up import    def write_to_file(filename, file_meminfo):
### messed up import        # automatically creating directories with file output
### messed up import        # http://stackoverflow.com/a/12517490/4710864
### messed up import        if not os.path.exists(os.path.dirname(filename)):
### messed up import            try:
### messed up import                os.makedirs(os.path.dirname(filename))
### messed up import            except OSError as exc:  # Guard against race condition
### messed up import                if exc.errno != errno.EEXIST:
### messed up import                    raise
### messed up import        try:
### messed up import            with open(filename, 'w') as fp:
### messed up import                fp.write(file_meminfo)
### messed up import        except IOError:
### messed up import            print ('Oops! write file error.')
### messed up import            silent_remove(filename)
### messed up import    
### messed up import    
### messed up import    def get_procs_attr_group(filtered_procs_mem, pkgs_dic):
### messed up import        gms_kb = platform_kb = third_kb = sys_kb = 0
### messed up import        groups_mem_kb = {}
### messed up import        groups_mem = {}
### messed up import        gms_procs_mem = []
### messed up import        platform_procs_mem = []
### messed up import        third_procs_mem = []
### messed up import        sys_procs_mem = []
### messed up import    
### messed up import        for proc in filtered_procs_mem:
### messed up import            if any(item in proc for item in GOOGLE_PROC_WHITE_LIST):
### messed up import                gms_kb += int(filtered_procs_mem[proc])
### messed up import                gms_procs_mem.append(proc)
### messed up import            elif any(plat_pkg in proc for plat_pkg in PLATFORM_PKGS):
### messed up import                platform_kb += int(filtered_procs_mem[proc])
### messed up import                platform_procs_mem.append(proc)
### messed up import            else:
### messed up import                # prefix_third = re.search(r'\w+\.\w+', proc)
### messed up import                # Check if substring is in a list of strings
### messed up import                # http://stackoverflow.com/a/16380333/4710864
### messed up import                # if prefix_third is not None and any(prefix_third.group() in pkg for pkg in third_pkgs):
### messed up import                #
### messed up import                # If any item of list starts with string?
### messed up import                #
### messed up import                # if there is only one "com.tct" in the third packages, resulted in all the com.tct pkgs in the third
### messed up import                # if "com.jrdcom" not in proc and prefix_third is not None and any(
### messed up import                #         pkg.startswith(prefix_third.group()) for pkg in pkgs_dic['third']):
### messed up import                #
### messed up import                # Check if multiple strings exist in another string
### messed up import                # http://stackoverflow.com/a/3389611/4710864
### messed up import                if any(pkg in proc for pkg in pkgs_dic['system'] if pkg != 'android' and pkg != 'android.overlay')\
### messed up import                        or any(proc == item for item in SYSTEM_PROC_WHITE_LIST):
### messed up import                    sys_kb += int(filtered_procs_mem[proc])
### messed up import                    sys_procs_mem.append(proc)
### messed up import                else:
### messed up import                    third_kb += int(filtered_procs_mem[proc])
### messed up import                    third_procs_mem.append(proc)
### messed up import    
### messed up import        groups_mem_kb.update({'GMS': gms_kb})
### messed up import        groups_mem_kb.update({'Third': third_kb})
### messed up import        groups_mem_kb.update({'System apps': sys_kb})
### messed up import        if int(platform_flag):
### messed up import            groups_mem_kb.update({'MTK': platform_kb})
### messed up import        else:
### messed up import            groups_mem_kb.update({'Qcom': platform_kb})
### messed up import    
### messed up import        groups_mem.update({'GMS': gms_procs_mem})
### messed up import        groups_mem.update({'Third': third_procs_mem})
### messed up import        groups_mem.update({'System apps': sys_procs_mem})
### messed up import        if int(platform_flag):
### messed up import            groups_mem.update({'MTK': platform_procs_mem})
### messed up import        else:
### messed up import            groups_mem.update({'Qcom': platform_procs_mem})
### messed up import        return groups_mem_kb, groups_mem
### messed up import    
### messed up import    
### messed up import    def get_packages_dic(installed_pkgs_str):
### messed up import        pkgs_dic = {}
### messed up import        third_pkgs = []
### messed up import        installed_pkgs = []
### messed up import        for pkg in installed_pkgs_str.split('\n'):
### messed up import            pkg_mat = re.search(r'package:(/\w+/[\w\-]+)/[^=]+=(.+)', pkg)
### messed up import            if pkg_mat is not None:
### messed up import                installed_pkgs.append(pkg_mat.group(2).strip())
### messed up import                if "/data/app" == pkg_mat.group(1) and not any(item in pkg for item in GOOGLE_PROC_WHITE_LIST):
### messed up import                    third_pkgs.append(pkg_mat.group(2).strip())
### messed up import        pkgs_dic.update({'third': third_pkgs})
### messed up import        pkgs_dic.update({'installed': installed_pkgs})
### messed up import    
### messed up import        gms_pkgs = []
### messed up import        platform_pkgs = []
### messed up import        system_pkgs = []
### messed up import        for pkg in installed_pkgs:
### messed up import            if any(item in pkg for item in GOOGLE_PROC_WHITE_LIST):
### messed up import                gms_pkgs.append(pkg)
### messed up import            elif any(plat_pkg in pkg for plat_pkg in PLATFORM_PKGS):
### messed up import                platform_pkgs.append(pkg)
### messed up import            elif pkg not in third_pkgs:
### messed up import                system_pkgs.append(pkg)
### messed up import        pkgs_dic.update({'gms': gms_pkgs})
### messed up import        pkgs_dic.update({'system': system_pkgs})
### messed up import        if int(platform_flag):
### messed up import            pkgs_dic.update({'mtk': platform_pkgs})
### messed up import        else:
### messed up import            pkgs_dic.update({'qcom': platform_pkgs})
### messed up import        return pkgs_dic
### messed up import    
### messed up import    
### messed up import    def get_file_meminfo(file_meminfo_str):
### messed up import        pss_mem_flag = False
### messed up import        native_mem_flag = False
### messed up import        system_mem = {}
### messed up import        procs_mem = {}
### messed up import        # How can I add items to an empty set in python
### messed up import        # http://stackoverflow.com/a/17511281/4710864
### messed up import        native_mem = set()
### messed up import    
### messed up import        mem_item_regx = re.compile('(\d+) kB: ([\w\.:_\-]*) \(pid.*')
### messed up import        for line in file_meminfo_str.split('\n'):
### messed up import            # A string contains substring method
### messed up import            if "Total PSS by process:" in line:
### messed up import                pss_mem_flag = True
### messed up import            elif "Total PSS by OOM adjustment:" in line:
### messed up import                pss_mem_flag = False
### messed up import                native_mem_flag = True
### messed up import            elif pss_mem_flag:
### messed up import                proc = mem_item_regx.search(line)
### messed up import                if proc is not None:
### messed up import                    procs_mem.update({proc.group(2): proc.group(1)})
### messed up import            elif native_mem_flag:
### messed up import                # Check whether the string is empty
### messed up import                if not system_mem.get('Native', ""):
### messed up import                    native = re.search(r'(\d+) kB: Native', line)
### messed up import                    if native is not None:
### messed up import                        system_mem.update({'Native': native.group(1)})
### messed up import                # elif re.search(r'\d+ kB: Persistent', line) is not None:
### messed up import                elif re.search(r'\d+ kB: \w+?\s*[\r\n]+', line) is not None:
### messed up import                    native_mem_flag = False
### messed up import                elif native_mem_flag:
### messed up import                    na = mem_item_regx.search(line)
### messed up import                    if na is not None:
### messed up import                        native_mem.add(na.group(2))
### messed up import            elif not system_mem.get('Total RAM', ""):
### messed up import                total = re.search(r'Total RAM:\s+(\d+) kB', line)
### messed up import                if total is not None:
### messed up import                    system_mem.update({'Total RAM': total.group(1)})
### messed up import            elif not system_mem.get('Free RAM', ""):
### messed up import                free = re.search(r'Free RAM:\s+(\d+) kB', line)
### messed up import                if free is not None:
### messed up import                    system_mem.update({'Free RAM': free.group(1)})
### messed up import            elif not system_mem.get('Used RAM', ""):
### messed up import                used = re.search(r'Used RAM:\s+(\d+) kB\s+\((\d+) used pss\s+\+\s+(\d+) kernel', line)
### messed up import                if used is not None:
### messed up import                    system_mem.update({'Used RAM': used.group(1)})
### messed up import                    system_mem.update({'Used Pss': used.group(2)})
### messed up import                    system_mem.update({'Kernel': used.group(3)})
### messed up import    
### messed up import        if __debug__:
### messed up import            pss_kb = 0
### messed up import            # # Python Sorted: Sorting a dictionary by value (DESC) then by key (ASC)
### messed up import            # # http://stackoverflow.com/a/15371752/4710864
### messed up import            # for k, v in sorted(procs_mem.items(), key=lambda x: (-int(x[1]), x[0])):
### messed up import            #     print (' {1}:  {0}'.format(k, v))
### messed up import            #     pss_kb += int(v)
### messed up import            # print 'procs_mem size=', len(procs_mem), ', pss_kb=', pss_kb
### messed up import            # print '\n************\n'
### messed up import            # print 'system_mem=', system_mem
### messed up import            # print '\n************\n'
### messed up import    
### messed up import        filtered_procs_mem = filter_out_native_processes(procs_mem, native_mem)
### messed up import        return system_mem, filtered_procs_mem
### messed up import    
### messed up import    
### messed up import    def filter_out_native_processes(procs_mem, native_mem):
### messed up import        filtered_procs_mem = {}
### messed up import        for key in set(procs_mem.keys()) - native_mem:
### messed up import            filtered_procs_mem.update({key: procs_mem[key]})
### messed up import        return filtered_procs_mem
### messed up import    
### messed up import    
### messed up import    def print_mem_table(outfile, system_mem, groups_mem_kb, pkgs_dic):
### messed up import        row_format = "{:<20}{}\n"
### messed up import        if os.path.isfile(outfile):
### messed up import            os.remove(outfile)
### messed up import        with open(outfile, 'w') as fp:
### messed up import            # write system memory info
### messed up import            fp.write(row_format.format("*Memory*", "*Val(MB)*"))
### messed up import            fp.write(row_format.format('Total RAM', kb2mb(system_mem['Total RAM'])))
### messed up import            fp.write(row_format.format('Free RAM', kb2mb(system_mem['Free RAM'])))
### messed up import            fp.write(row_format.format('Kernel', kb2mb(system_mem['Kernel'])))
### messed up import            fp.write(row_format.format('Native', kb2mb(system_mem['Native'])))
### messed up import            fp.write("\n")
### messed up import            # write module memory info
### messed up import            fp.write(row_format.format("*Module*", "*Val(MB)*"))
### messed up import            fp.write(row_format.format('GMS', kb2mb(groups_mem_kb['GMS'])))
### messed up import            fp.write(row_format.format('Third', kb2mb(groups_mem_kb['Third'])))
### messed up import            fp.write(row_format.format('System apps', kb2mb(groups_mem_kb['System apps'])))
### messed up import            if int(platform_flag):
### messed up import                fp.write(row_format.format('MTK', kb2mb(groups_mem_kb['MTK'])))
### messed up import            else:
### messed up import                fp.write(row_format.format('Qcom', kb2mb(groups_mem_kb['Qcom'])))
### messed up import            fp.write("\n")
### messed up import            # write packages info
### messed up import            fp.write(row_format.format("*Packages*", "*Count*"))
### messed up import            fp.write(row_format.format('installed', len(pkgs_dic['installed'])))
### messed up import            fp.write(row_format.format('gms', len(pkgs_dic['gms'])))
### messed up import            fp.write(row_format.format('third', len(pkgs_dic['third'])))
### messed up import            fp.write(row_format.format('system', len(pkgs_dic['system'])))
### messed up import            if int(platform_flag):
### messed up import                fp.write(row_format.format('mtk', len(pkgs_dic['mtk'])))
### messed up import            else:
### messed up import                fp.write(row_format.format('qcom', len(pkgs_dic['qcom'])))
### messed up import    
### messed up import    
### messed up import    def kb2mb(num):
### messed up import        return int(num) // 1024
### messed up import    
### messed up import    
### messed up import    # border_style = Style(font=Font(name='Console', size=10, bold=False,
### messed up import    #                                color=Color(openpyxl.styles.colors.BLACK)),
### messed up import    #                      fill=PatternFill(patternType='solid', fgColor=Color(rgb='00C5D9F1')),
### messed up import    #                      border=Border(bottom=Side(border_style='medium', color=Color(rgb='FF000000'))))
### messed up import    def styled_title_cell(ws, data):
### messed up import        for c in data:
### messed up import            c = ws.cell(column=data.index(c) + 1, row=1, value=c)
### messed up import            c.fill = PatternFill(start_color='ff268bd2', end_color='ff268bd2', fill_type='solid')
### messed up import            c.font = Font(name='Console', size=14, bold=True)
### messed up import            c.alignment = Alignment(horizontal='left', vertical='center')
### messed up import            yield c
### messed up import    
### messed up import    
### messed up import    def styled_subtitle(val, c):
### messed up import        if val in ['Memory', 'Module', 'Packages']:
### messed up import            c.font = Font(name='Courrier', size=12, bold=True)
### messed up import        else:
### messed up import            c.font = Font(name='Courrier', size=12)
### messed up import        c.fill = PatternFill(patternType='solid', fgColor=Color(rgb='00C5D9F1'))
### messed up import        c.alignment = Alignment(horizontal='left', vertical='center')
### messed up import    
### messed up import    
### messed up import    def styled_cell(c):
### messed up import        c.font = Font(name='Courrier', size=12)
### messed up import        c.alignment = Alignment(horizontal='left', vertical='top')
### messed up import    
### messed up import    
### messed up import    def render_ws(ws):
### messed up import        # adjust width of the column
### messed up import        # http://stackoverflow.com/a/14450572/4710864
### messed up import        # http://stackoverflow.com/q/32855656/4710864
### messed up import        for i in range(ws.max_column):
### messed up import            ws.column_dimensions[get_column_letter(i + 1)].width = 20
### messed up import    
### messed up import        # adjust height of the row
### messed up import        # http://stackoverflow.com/q/32855656/4710864
### messed up import        for i in range(ws.max_row):
### messed up import            # Get value of specific cells with openpyxl
### messed up import            # http://stackoverflow.com/a/29157762/4710864
### messed up import            val = ws["{}{}".format(get_column_letter(5), i + 1)].value
### messed up import            if i == 0:
### messed up import                ws.row_dimensions[i + 1].height = 23
### messed up import            elif val is not None:
### messed up import                if len(val.split('\n')) <= 10:
### messed up import                    ws.row_dimensions[i + 1].height = 18 * len(val.split('\n'))
### messed up import                else:
### messed up import                    ws.row_dimensions[i + 1].height = 18 * 10
### messed up import            else:
### messed up import                ws.row_dimensions[i + 1].height = 18
### messed up import    
### messed up import        # set border, used "iter_rows"
### messed up import        # http://stackoverflow.com/a/34521257/4710864
### messed up import        for row in ws.iter_rows("A1:E17"):
### messed up import            for i in range(ws.max_column):
### messed up import                row[i].border = Border(left=Side(border_style='thin'),
### messed up import                              right=Side(border_style='thin'),
### messed up import                              top=Side(border_style='thin'),
### messed up import                              bottom=Side(border_style='thin'))
### messed up import    
### messed up import    
### messed up import    def print_diff_table(system_mem_1, system_mem_2, pkgs_dic_1, pkgs_dic_2,
### messed up import                         groups_mem_kb_1, groups_mem_kb_2, groups_mem_1, groups_mem_2):
### messed up import        ws_tile = ['Items', original_dir, diff_dir, 'Gap', 'Detail']
### messed up import        total_memory_items = ['Total RAM', 'Free RAM', 'Kernel', 'Native']
### messed up import        if int(platform_flag):
### messed up import            module_memory_items = ['GMS', 'MTK', 'Third', 'System apps']
### messed up import            package_items = ['installed', 'gms', 'mtk', 'third', 'system']
### messed up import        else:
### messed up import            module_memory_items = ['GMS', 'Qcom', 'Third', 'System apps']
### messed up import            package_items = ['installed', 'gms', 'qcom', 'third', 'system']
### messed up import        wb = Workbook()
### messed up import        ws = wb.active
### messed up import        ws.title = "Memory Diff Table"
### messed up import        # Coloring a tab in openpyxl
### messed up import        ws.sheet_properties.tabColor = 'FFFF9900'  # Orange
### messed up import        # add title at the top of the table
### messed up import        ws.append(styled_title_cell(ws, ws_tile))
### messed up import    
### messed up import        if int(platform_flag):
### messed up import            title = MTK_TITLE
### messed up import        else:
### messed up import            title = QCOM_TITLE
### messed up import        # How to write a list to xlsx
### messed up import        # http://stackoverflow.com/a/15004956/4710864
### messed up import        for col in title:
### messed up import            styled_subtitle(col, ws.cell(column=1, row=title.index(col) + 2, value=col))
### messed up import            if col in total_memory_items:
### messed up import                styled_cell(ws.cell(column=2, row=title.index(col) + 2, value="{}MB".format(kb2mb(system_mem_1[col]))))
### messed up import                styled_cell(ws.cell(column=3, row=title.index(col) + 2, value="{}MB".format(kb2mb(system_mem_2[col]))))
### messed up import                styled_cell(ws.cell(column=4, row=title.index(col) + 2,
### messed up import                                    value="{}MB".format(kb2mb(system_mem_1[col]) - kb2mb(system_mem_2[col]))))
### messed up import            if col in module_memory_items:
### messed up import                styled_cell(ws.cell(column=2, row=title.index(col) + 2, value="{}MB".format(kb2mb(groups_mem_kb_1[col]))))
### messed up import                styled_cell(ws.cell(column=3, row=title.index(col) + 2, value="{}MB".format(kb2mb(groups_mem_kb_2[col]))))
### messed up import                styled_cell(ws.cell(column=4, row=title.index(col) + 2,
### messed up import                                    value="{}MB".format(kb2mb(groups_mem_kb_1[col]) - kb2mb(groups_mem_kb_2[col]))))
### messed up import                # Writing multi-line strings into cells using openpyxl
### messed up import                # http://stackoverflow.com/questions/15370432/writing-multi-line-strings-into-cells-using-openpyxl
### messed up import                c = ws.cell(column=5, row=title.index(col) + 2)
### messed up import                c.style.alignment.wrap_text = True
### messed up import                c.value = "ADDED PROCESSES:\n{}\n\nREMOVED PROCESSES:\n{}".format(
### messed up import                    '\n'.join(set(groups_mem_1[col]) - set(groups_mem_2[col])),
### messed up import                    '\n'.join(set(groups_mem_2[col]) - set(groups_mem_1[col])))
### messed up import                styled_cell(c)
### messed up import            if col in package_items:
### messed up import                styled_cell(ws.cell(column=2, row=title.index(col) + 2, value=len(pkgs_dic_1[col])))
### messed up import                styled_cell(ws.cell(column=3, row=title.index(col) + 2, value=len(pkgs_dic_2[col])))
### messed up import                styled_cell(ws.cell(column=4, row=title.index(col) + 2,
### messed up import                                    value=len(pkgs_dic_1[col]) - len(pkgs_dic_2[col])))
### messed up import                c = ws.cell(column=5, row=title.index(col) + 2)
### messed up import                c.style.alignment.wrap_text = True
### messed up import                diff_pkgs = [['\nADDED PACKAGES:'], set(pkgs_dic_1[col]) - set(pkgs_dic_2[col]),
### messed up import                             ['\nREMOVED PACKAGES:'], set(pkgs_dic_2[col]) - set(pkgs_dic_1[col])]
### messed up import                # how to extract nested lists?
### messed up import                # http://stackoverflow.com/a/953097/4710864
### messed up import                merged = list(itertools.chain(*diff_pkgs))
### messed up import                if len(merged) != 0:
### messed up import                    c.value = '\n'.join(merged)
### messed up import                    styled_cell(c)
### messed up import    
### messed up import        render_ws(ws)
### messed up import        wb.save(filename=out_parse_xlsx)
### messed up import        print ("Finished: save xlsx at", out_parse_xlsx)
### messed up import    
### messed up import    
### messed up import    def filter_out_items(list1, list2):
### messed up import        set(list1) - set(list2)
### messed up import    
### messed up import    
### messed up import    if __name__ == '__main__':
### messed up import        # Python: about catching ANY exception
### messed up import        # http://stackoverflow.com/a/4992124/4710864
### messed up import        try:
### messed up import            main()
### messed up import        except Exception as e:
### messed up import            # print e.__doc__
### messed up import            # print e.message
### messed up import            # logging.error(traceback.format_exc().strip())  # seems like "raise"
### messed up import            # delete output files
### messed up import            silent_remove(os.path.dirname(out_parse_table))
### messed up import            silent_remove(out_parse_xlsx)
### messed up import            raise
