"""
Gitago - TouchPortal Android ADB
"""
__version__ = "1.0"

### MOVED ALL IMPORTS TO adb_globals...
from adb_globals import *
commands=adb_commadns.commands


#### https://dev.to/larsonzhong/most-complete-adb-commands-4pcg#turn-on-off-the-screen  
### some shortcuts for calling n such



#print(device.shell("dumpsys battery | grep health"))
### Find all the ADB Stuff on the Device
#print(device.shell('dumpsys | grep "DUMP OF SERVICE"'))
#print(device.shell('/sys/class/power_supply/battery/'))


#### one line screenshot + save 'screencap -p | sed "s/\r$//"> sc.png'   - but read only file system on pc??
#device.shell('input keyevent 15')

""" OPEN WEBSITE / BROWSER """
#device.shell("am start -a android.intent.action.VIEW -d http://www.stackoverflow.com")
#device.shell("am start -n com.android.chrome/com.google.android.apps.chrome.Main \ -a android.intent.action.VIEW -d 'http://www.stackoverflow.com'")



def get_screen_info(device_choice)-> dict:
    """Get Device Screen Info"""
    density = device_choice.shell('wm density').split(":")[-1].split("\n")[0]
    size = device_choice.shell('wm size').split(":")[-1].split("\n")[0]
    model = device_choice.shell('getprop ro.product.model').split("\n")[0]
    manufac = device_choice.shell('getprop ro.product.manufacturer').split("\n")[0]
    board  = device_choice.shell('getprop ro.product.board').split("\n")[0]
    hardware = device_choice.shell('getprop ro.hardware').split("\n")[0]
    android_version = device_choice.shell('getprop ro.build.version.release').split("\n")[0]
    return {"Version": android_version, "Hardware": hardware, "Board": board, "Manufacturer": manufac.capitalize(), "Model": model, "Screen Size": size, "Screen Density":density}
    

"""            GETTING BATTERY INFO / SAVING TO DICT                """
def battery_state_update(device, format = "Celcius")-> dict:
    """ Returns Dictionary with Full Battery Details """
    #global battery_states
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
                        print("changed: state={} old={} new={}".format(state, value, m.group(1)))
                        battery_states[state] = m.group(1)
                        

    
        # Taking Battery Health/Status and Turning into "result"""
        #  Extracting the NUMBER, it will be converted to a string result on update/create states
        ### NEED TO MAKE INDEPENDENT DICTIONARIES FOR EACH DEVICE...
        if "vendor.samsung.hardware" in battery_states['health']:
            extract_health= (battery_states['health'].split("::")[0].replace("vendor.samsung.hardware.health@",""))
            battery_states['health'] = str(round(float(extract_health)))
    
    # Converting Battery Status Number to String
    try:
        battery_states['status'] = bat_state_conver(choice='status',num=int(battery_states['status']))
    except:
        print("Unable to Convert Status, Check Results")
        ### NEED TO MAKE INDEPENDENT DICTIONARIES FOR EACH DEVICE...
        
    if changes > 0:
        print("---- {} changes".format(changes))
       # print(battery_states)
        pass
        
    return battery_states



def create_states():
    """ Creates and or Updates States as Needed """
    count2=1
    
    for adict in device_list:
       # battery_info= get_battery_level_and_temperature(adict['Device'], format = "Celcius")
        battery_info = battery_state_update(adict['Device'])
        mem_info = get_mem_info(adict['Device'])
        
        
        """ THIS SHOULD PULL FROM PLUGIN SETTINGS TO DECIDE IF C OR F"""
        aformat="Fahrenheit"
        temp = float(battery_info['temperature']) /10.0  

        if aformat == "Celcius":
            temp_formatted = f"{float(battery_info['temperature']) /10.0} °C"
        elif aformat == "Fahrenheit":
            temp_formatted = f'{(temp * 9/5) + 32} °F'
    
        
        TPClient.createStateMany([
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.Version',
        "desc": f"{adict['Model']} Android Version",
        "value": str(adict['Version'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.Hardware',
        "desc": f"{adict['Model']} Hardware ",
        "value": str(adict['Hardware'])
        },
            {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.Manufacturer',
        "desc": f"{adict['Model']} Manufacturer",
        "value": str(adict['Manufacturer'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.Model',
        "desc": f"{adict['Model']} Model",
        "value": f"{adict['Model']}"
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.ScreenSize',
        "desc": f"{adict['Model']} Screen Size",
        "value": str(adict['Screen Size'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.BatteryStatus',
        "desc": f"{adict['Model']} Battery Status",
        "value": str(battery_info['status'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.BatteryLevel',
        "desc": f"{adict['Model']} Battery Level",
        "value": str(battery_info['level'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.BatteryTemperature',
        "desc": f"{adict['Model']} Battery Temperature",
        "value": str(temp_formatted)
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.BatteryVoltage',
        "desc": f"{adict['Model']} Battery Voltage",
        "value": str(battery_info['voltage']+" mV")
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.BatteryHealth',
        "desc": f"{adict['Model']} Battery Health",
        "value": bat_state_conver(choice='health',num=int(battery_info['health']))
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.MemoryTotal',
        "desc": f"{adict['Model']} Memory Total",
        "value": str(mem_info['MemTotal'])
        },
        {
        "id": f'Gitago-ADB.TP.Plugins.device{count2}.MemoryAvailable',
        "desc": f"{adict['Model']} Memory Available",
        "value": f"{str(mem_info['MemAvailable'])} {mem_info['MemAvailable']} // {mem_info['MemTotal']} "
        }, 
        ])
        count2 = count2+1
    


### Swipe to Unlock
def swipe_to_unlock(device, x1=None, x2=None, y1= None, y2=None):
    """ Basic Swipe to Unlock"""
    "Turn on screen"
    try:
        #device.shell('input keyevent 224')
       # time.sleep(0.2)
        "swipe to unlock"
        device.shell(f'input swipe {x1} {x2} {y1} {y2}')
    except:
        print("error swiping")
   # device.shell("input keyevent 15")
   # device.shell("input keyevent 13")
   # device.shell("input keyevent 15")
   # device.shell("input keyevent 14")



def get_mem_info(device)-> dict:
    """ Returns Dictionary with Memory Details"""
    mem_list = ['MemTotal', 'MemAvailable']
    mem_check = device.shell("cat /proc/meminfo")
    split = mem_check.splitlines(-1)
    memdict ={}
    for line in split:
        if 'MemTotal:' in line:
            size = kb2mb(int(line.split(" ")[-2]))
            memdict['MemTotal'] = f"{size}"
            memtotal = memdict['MemTotal']
        if 'MemAvailable:' in line:
            size = kb2mb(line.split(" ")[-2])
            memdict['MemAvailable'] = f"{size}"
            memavail = memdict['MemAvailable']
            
        """Had to do this to get it to round?"""
    perce= int(memavail) / int(memtotal) * 100
    memdict['Percentage']= round(perce)

    return memdict


def adjust_volume(device, volume, speaker):
    """ Adjust Device Volume
    - Speaker = Phone": 1, "Notification": 2, "Speaker": 3, "Alarm": 4, "Bluetooth": 6
    """
    speaker_choices ={
        "Phone": 1,
        "Notification": 2,
        "Speaker": 3, 
        "Alarm": 4,
        "Bluetooth": 6}
    volume = int(volume) // 4
    device['Device'].shell(f'service call audio 7 i32 {speaker_choices[speaker]} i32 {int(volume)} i32 1')
    time.sleep(0.10)


def adjust_brightness(device, level):
    """Adjust Device Brightness"""
    level = level * 2.6
    if level <6:
        print("too low")
        pass
    elif level >5:
        print("going up?")
        if level >255:
            level = 255
        device['Device'].shell(f'settings put system screen_brightness {int(level)}')
        print(level)



""" Formatting + Dictionary """
def check_sleep():
    ok=(device.shell('dumpsys power | grep mHolding'))
    buf = StringIO(ok)
    changes = 0
    for line2 in buf.readlines():
        line = line2.strip()
        for state, value in sleep_states.items():
            m = re.search(r'{}=(.*)'.format(state), line)
            if m:
                if value != m.group(1):
                    changes += 1
                    print("changed: state={} old={} new={}".format(state, value, m.group(1)))
                    sleep_states[state] = m.group(1)
        if changes > 0:
            print("---- {} changes".format(changes))
            return sleep_states
        

##################################################################################################
#________________________________ TOUCH PORTAL CONNECTION _______________________________________#

### Removed device_list=[] here and moved to globals...
def connect():
    global device_list
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    #client.remote_connect("192.168.0.106", 5555)
    devices = client.devices() 
    if len(devices) == 0:
        print('No devices')
        quit()
        
    count = 0
    a={}
    for x in devices:
        key = f"device{count}"
        value = x
        a[key] = value
        
        ### Pulling Device Details
        device_info = get_screen_info(value)
        
        device_dict = {f"Device": value}
        device_dict.update(device_info)
        device_list.append(device_dict)
        count=count+1
    return device_list


try:
    TPClient = TP.Client(
        pluginId = "Gitago-ADB", 
        sleepPeriod = 0.05,    
        autoClose = True,      
        checkPluginId = True,  
        maxWorkers = 4,        
        updateStatesOnBroadcast = False,  
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")


g_log = getLogger()

old_devices=[]
def handleSettings(settings, on_connect=False):
    global old_devices
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    
    """ Updating Choice Selection on Startup"""
    choice_list = []
    for x in device_list:
        choice_list.append(f"{x['Manufacturer'].capitalize()} {x['Model']}")
    if old_devices != choice_list:
            TPClient.choiceUpdate('Gitago-ADB.TP.Plugins.device_select', choice_list)
    old_devices = choice_list
    
    """ Creating States for Connected Devices"""
    create_states()


#_________________ ON CONNECT _______________#
# Initial connection handler
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    device, client = connect()
    if settings := data.get('settings'):
        handleSettings(settings, True)
        
    #th = threading.Thread(target=battery_state_update, daemon=True)
    #th.start()


#__________ON SETTINGS UPDATE ___________#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)


#________ ON LIST CHANGE _______#
@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data):
    global old_devices
    if data['actionId'] == "Gitago-ADB.TP.Plugins.device_commands":
        c_list = []
        for x in device_list:
            c_list.append(f"{x['Manufacturer']} {x['Model']}")
        if old_devices != c_list:
            TPClient.choiceUpdate('Gitago-ADB.TP.Plugins.device_select', c_list)
        old_devices = c_list


#________ ON BUTTON HELD DOWN _______#
@TPClient.on(TP.TYPES.onHold_down)
def heldingButton(data):
    print(data)
    while True:
        """ Can make this smoother by using onhold_up and down and then go from 0-100 scale while holding.. just need to find a way to get current volume level"""
        if TPClient.isActionBeingHeld('Gitago-ADB.TP.Plugins.screenbrightness'):
            if data['data'][1]['value'] == "Down":
               match_device(data['data'][0]['value'])['Device'].shell('input keyevent 220')
               time.sleep(0.2)
               
            elif data['data'][1]['value'] == "Up":
                match_device(data['data'][0]['value'])['Device'].shell('input keyevent 221')
                time.sleep(0.2)
                
        else:
            break



#_________ ON CONNECTOR CHANGE  _________#
@TPClient.on(TP.TYPES.onConnectorChange)
def connectors(data):
    print(data)
    if data['connectorId'] == "Gitago-ADB.TP.Plugins.VolumeMixer.connectors":
        adjust_volume(device=match_device(data['data'][0]['value']), volume=data['value'], speaker= data['data'][1]['value'])
    
    if data['connectorId'] == "Gitago-ADB.TP.Plugins.device.brightness.slider":
        adjust_brightness(device=match_device(data['data'][0]['value']), level=data['value'])



#_________________ ON ACTIONS _______________#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    print(data)
    if data['actionId'] == "Gitago-ADB.TP.Plugins.device_commands":
        if data['data'][1]['value'] == "Camera":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 27')
        if data['data'][1]['value'] == "Browser":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 64')
        if data['data'][1]['value'] == "Contacts":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 207')
        if data['data'][1]['value'] == "Open Call Button":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 5')
        if data['data'][1]['value'] == "Close Call Button":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 6')
        if data['data'][1]['value'] == "Back Button":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 4')
        if data['data'][1]['value'] == "Home Button / Return":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 3')
        if data['data'][1]['value'] == "Toggle Device On / Off":
          #check_dreaming(data['data'][0]['value'])
          #print("YELLO?")  ### does not appear to do anything ?
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 2')
        if data['data'][1]['value'] == "Toggle Power Menu":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent KEYCODE_POWER')
        if data['data'][1]['value'] == "Toggle Mute":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 164')
        if data['data'][1]['value'] == "Voice Assistant":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 231')
        if data['data'][1]['value'] == "Calendar":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 208')
        if data['data'][1]['value'] == "Menu Button":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 82')
            
    if data['actionId'] == "Gitago-ADB.TP.Plugins.device_swipeunlock":
        swipe_to_unlock(device=match_device(data['data'][0]['value'])['Device'], x1=data['data'][1]['value'], x2=data['data'][2]['value'], y1=data['data'][3]['value'], y2=data['data'][4]['value'])
        
        
        
    if data['actionId'] == "Gitago-ADB.TP.Plugins.device.display":
        if data['data'][1]['value'] == "On":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 224')
        elif data['data'][1]['value'] == "Off":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 223')
      #print("eh?")
      #match_device(data['data'][0]['value'])['Device'].shell('input keyevent KEYCODE_POWER')

        
    if data['actionId'] == "Gitago-ADB.TP.Plugins.volume":
        if data['data'][1]['value'] == "Up":
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 24')
        else:
            match_device(data['data'][0]['value'])['Device'].shell('input keyevent 25')

    if data['actionId'] == "Gitago-ADB.TP.Plugins.device.screenshot":
        filename = data['data'][1]['value']
        """ Screenshot Device"""
        print(match_device(data['data'][0]['value'])['Device'].shell(f'screencap -p /sdcard/{filename}'))
        
        """ Pull Screenshot to PC"""
        print(match_device(data['data'][0]['value'])['Device'].pull(f"/sdcard/{filename}", f"C:/Users/dbcoo/Downloads/tmp/{filename}"))

    
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return

  #  else:
  #      g_log.warning("Got unknown action ID: " + aid)

#_______ ON SHUTDOWN ______#"""
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')


## Error handler
#@TPClient.on(TP.TYPES.onError)
#def onError(exc):
#    g_log.error(f'Error in TP Client event handler: {repr(exc)}')



def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    # handle CLI arguments
    parser = ArgumentParser()
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help="Log to this file (default is stdout).")
    parser.add_argument("-s", action='store_true',
                        help="If logging to file, also output to stdout.")

    opts = parser.parse_args()
    del parser

    # set up logging
    if opts.q:
        # no logging at all
        g_log.addHandler(NullHandler())
    else:
        # set up pretty log formatting (similar to TP format)
        fmt = Formatter(
            fmt="{asctime:s}.{msecs:03.0f} [{levelname:.1s}] [{filename:s}:{lineno:d}] {message:s}",
            datefmt="%H:%M:%S", style="{"
        )

        if   opts.d: g_log.setLevel(DEBUG)
        elif opts.w: g_log.setLevel(WARNING)
        else:        g_log.setLevel(INFO)
        if opts.l:
            try:
                fh = FileHandler(str(opts.l))
                fh.setFormatter(fmt)
                g_log.addHandler(fh)
            except Exception as e:
                opts.s = True
                print(f"Error while creating file logger, falling back to stdout. {repr(e)}")
        if not opts.l or opts.s:
            sh = StreamHandler(sys.stdout)
            sh.setFormatter(fmt)
            g_log.addHandler(sh)



    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    # TP disconnected, clean up.
    del TPClient
    
    return ret


if __name__ == "__main__":
    sys.exit(main())