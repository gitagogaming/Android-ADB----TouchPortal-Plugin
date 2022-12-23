from adb_globals import *




"""
-------------------------------------------------
----------------- BATTERY USAGE -----------------
-------------------------------------------------
"""

battery_states_final={}
def battery_state_update(device, format = "Celcius"):
    """ Returns Dictionary with Full Battery Details """
    battery_states = {"temperature": "", "level": "", "voltage":"", "status":"", "health": "",
                      "AC powered": "", "USB powered": "", "Wireless powered":"",  "present": ""}
    
    ok=(device.shell('dumpsys battery'))
    buf = StringIO(ok)
    changes = 0
    for line2 in buf.readlines():
        line = line2.strip()
        if "Max charging voltage" in line:
            pass
        else:
            for state, value in battery_states.items():
                m = re.search(r'{}:(.*)'.format(state), line)
                if m:
                    if value != m.group(1):
                        changes += 1
                       # print("changed: state={} old={} new={}".format(state, value, m.group(1)))

                        battery_states[state] = m.group(1).lstrip()

        # Taking Battery Health/Status and Turning into "result"""
        if "vendor.samsung.hardware" in battery_states['health']:
            extract_health= (battery_states['health'].split("::")[0].replace("vendor.samsung.hardware.health@",""))
            battery_states['health'] = str(round(float(extract_health)))

    # Converting Battery Status Number to String
    try:
        battery_states['status'] = bat_state_conver(choice='status',num=int(battery_states['status']))
    except:
        print("Unable to Convert Status, Check Results")
        
    if changes > 0:
        print("---- {} changes".format(changes))
        pass
    
    return battery_states







"""
-------------------------------------------------
------------------ SCREEN INFO ------------------
-------------------------------------------------
"""

dupe_device_count=1
def get_screen_info(device_choice):
    """Get Device Screen Info
    - This is where the device details are started
    """
    global dupe_device_count
    density = device_choice.shell('wm density').split(":")[-1].split("\n")[0]
    size = device_choice.shell('wm size').split(":")[-1].split("\n")[0]
    model = device_choice.shell('getprop ro.product.model').split("\n")[0]
    manufac = device_choice.shell('getprop ro.product.manufacturer').split("\n")[0]
    board  = device_choice.shell('getprop ro.product.board').split("\n")[0]
    hardware = device_choice.shell('getprop ro.hardware').split("\n")[0]
    android_version = device_choice.shell('getprop ro.build.version.release').split("\n")[0]
    
    
    ### Incase of duplicate devices lets add 1 number...
    if model in device_names:
        model = f"{model}({dupe_device_count})"
        dupe_device_count = dupe_device_count +1
    device_names.append(model)
    return {"Version": android_version, "Hardware": hardware, "Board": board, "Manufacturer": manufac.capitalize(), "Model": model, "Screen Size": size, "Screen Density":density}
    
    






"""
-------------------------------------------------
------------------- MEM USAGE -------------------
-------------------------------------------------
"""


import re

def get_mem_info(device):
    """ Returns Dictionary with Memory Details"""
    memdict = {}
    
    # Use regular expressions to extract the relevant values from the output of the "cat /proc/meminfo" command
    output = device.shell("cat /proc/meminfo")
    match = re.search(r'MemTotal:\s+(\d+)\skB\nMemFree:\s+(\d+)\skB\nMemAvailable:\s+(\d+)\skB', output)
    if match:
        memtotal, memfree, memavail = map(int, match.groups())
    else:
        # If the MemAvailable value is not found, use the MemFree value as a fallback
        match = re.search(r'MemTotal:\s+(\d+)\skB\nMemFree:\s+(\d+)\skB', output)
        memtotal, memfree = map(int, match.groups())
        memavail = memfree
    
    # Convert the values from kB to MB
    memtotal_mb = kb2mb(memtotal)
    memfree_mb = kb2mb(memfree)
    memavail_mb = kb2mb(memavail)

    # Calculate the percentage of available memory
    percent = memavail_mb / memtotal_mb * 100

    # Update the dictionary with the calculated values
    memdict['MemTotal'] = int(memtotal_mb)
    memdict['MemFree'] = int(memfree_mb)
    memdict['MemAvailable'] = int(memavail_mb)
    memdict['Percentage'] = round(percent)

    # Update the device list with the calculated values
    for x in device_list:
        if device_list[x]['ID'] == device:
            device_list[x].update({'MemAvailable': memavail_mb})
            device_list[x].update({'MemFree': memfree_mb})
            device_list[x].update({'Percentage': percent})
            # print(f"{x} Dictionary Updated with Memory Usage")
    return memdict




"""
-------------------------------------------------
------------------- CPU USAGE -------------------
-------------------------------------------------
"""

def get_cpu_usge(device):
    """ 
    Get the CPU Usage of the Device(s) 
    - if cpuz doesnt calculate cpu then why should we???
    """
    
    output = device.shell("top -n1")
    
    match =  re.search(r'(\d+%)cpu\s+(\d+%)user\s+(\d+%)nice\s+(\d+%)sys\s+(\d+%)idle', output)
    
    if match:
        ## assigning the values to variables
        cpu, user, nice, sys, idle = match.groups()
        
        ## stripping the '%' and splitting the values
        cpu = int(cpu.strip('%').split()[0])
        user = int(user.strip('%').split()[0])
        sys = int(sys.strip('%').split()[0])
        
        ## calculating the Approximate CPU usage on Device
        result = (int(user) + int(sys)) / int(cpu) * 100
        result = str(result)[:2]
    
    return result
