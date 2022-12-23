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
       # print(battery_states)
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

def get_mem_info(device):
    """ Returns Dictionary with Memory Details"""
    memavail = 0
    memfree = 0
    memtotal = 0
    
    try:
        mem_check = device.shell("cat /proc/meminfo")
        split = mem_check.splitlines(-1)
        memdict ={}
        for line in split:
            if 'MemTotal:' in line:
                size = kb2mb(int(line.split(" ")[-2]))
                memdict['MemTotal'] = f"{size}"
                memtotal = memdict['MemTotal']
                
            if 'MemFree:' in line:
                size = kb2mb(line.split(" ")[-2])
                memdict['MemFree'] = f"{size}"
                memfree = memdict['MemFree']

            if 'MemAvailable:' in line:
                size = kb2mb(line.split(" ")[-2])
                memdict['MemAvailable'] = f"{size}"
                memavail = memdict['MemAvailable']


           # print(memdict)
            """Had to do this to get it to round?"""
        perce= int(memavail) / int(memtotal) * 100
        memdict['Percentage']= round(perce)

        for x in device_list:
            if device_list[x]['ID'] == device:
                device_list[x].update({'MemAvailable':memavail})
                device_list[x].update({'MemFree':memfree})
                device_list[x].update({'Percentage':perce})
              #  print(f"{x} Dictionary Updated with Memory Usage")

        return memdict
    
    except Exception as e:
        print(f"Error Getting Memory Info: {e}")
        return None





"""
-------------------------------------------------
------------------- CPU USAGE -------------------
-------------------------------------------------
"""

def get_cpu_usge(device):
    """ 
    Get the CPU Usage of the Device(s) 
    """
    
    build = {}
    thelist = {"cpu", "user", "nice", "sys", "idle"}
    ok = device.shell("top -n1")
    split = ok.splitlines(-1)
    complete = False
    for line in split:
        if not complete:
            if "cpu" in line:
                newline = line.split(" ")
                complete = True
                for x in newline:
                    if x:
                        final_split = x.split("%")
                        if final_split[-1] in thelist:
                            build[final_split[-1]] = final_split[0]

                result= int(build['user']) + int(build['sys'])
                result = result / int(build['cpu'])
                result=result*100
                result = str(result)[0:2]
                
                if "." in result:
                    result = result.replace(".", "")

    """ Updating CPU Usage for Devices"""
    for x in device_list:
        if device_list[x]['ID'] == device:
            device_list[x].update({'CPU USAGE':result})
           # print(f"{x} Dictionary Updated with CPU Usage")
           
    return result
