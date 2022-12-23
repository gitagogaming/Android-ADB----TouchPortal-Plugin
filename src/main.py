"""
Gitago - TouchPortal Android ADB
"""

from adb_globals import *
import device_states
import logging

### TP PACKAGE ANDROID NAME = package:com.sec.android.RilServiceModeApp
# https://adbinstaller.com/commands/adb-shell-pm-5b672ff6e7958178a295553a


#### https://dev.to/larsonzhong/most-complete-adb-commands-4pcg#turn-on-off-the-screen  
### some shortcuts for calling n such
### Find all the ADB Stuff on the Device
#print(device.shell('dumpsys | grep "DUMP OF SERVICE"'))


""" OPEN WEBSITE / BROWSER """
#device.shell("am start -a android.intent.action.VIEW -d http://www.stackoverflow.com")
#device.shell("am start -n com.android.chrome/com.google.android.apps.chrome.Main \ -a android.intent.action.VIEW -d 'http://www.stackoverflow.com'")
###  Compare Custom Uninstall against the actual packages on device.

### calculator = 210
### System settings = 176
### resume playback = 126/127 
### move cursor to top/bottom list = 122/123



## Getting current devie volume ? 

#      output = match_device(data['data'][0]['value']).shell("""content query --uri content://settings/system --where 'name="volume_music"'""")
#   #   output = get_volume()
#      value = re.search(r"value=(\d+)", output).group(1)
#      print(value)

PLUGIN_ID = "Gitago-ADB.TP.Plugins"

COMMANDS = {
    "Turn Off Screen": "input keyevent 223",
    "Turn On Screen": "input keyevent 224",
    "Toggle Power Menu": 'input keyevent KEYCODE_POWER', #"input keyevent 26",
    "Toggle Device On / Off": 'input keyevent 2',
    "Increase Volume": "input keyevent 24",
    "Decrease Volume": "input keyevent 25",
    "Toggle Mute": "input keyevent 164",
    "Home Button": "input keyevent KEYCODE_HOME",             # "input keyevent 3",
    "Back Button": "input keyevent 4",
    "Menu Button": "input keyevent KEYCODE_MENU",                 #"input keyevent 82",
    "Calendar": "input keyevent 208" ,
    "Reduce Screen Brightness": "input keyevent 220",
    "Increase Screen Brightness": "input keyevent 221",
    "Voice Assistant": "input keyevent 231",
    "Browser": 'input keyevent 64',
    "Contacts": "input keyevent 207",
    "Open Call Button": 'input keyevent KEYCODE_CALL',
    "Close Call Button": 'input keyevent KEYCODE_ENDCALL',
    "Delete / Backspace": 'input keyevent KEYCODE_DEL',
    "Enter Button": "input keyevent KEYCODE_ENTER",
    "Reboot Device": "reboot",
    "Focus Camera": "input keyevent KEYCODE_FOCUS", #"input keyevent 80",
    "Take Picture": "input keyevent KEYCODE_CAMERA" #"input keyevent 27"
    
    
    # "CPU INFO": "cat /proc/cpuinfo",                        # use func above to pull details needed like processor, 
    # "MEM INFO": "cat /proc/meminfo",
    # "Screenshot Device": "exec-out screencap -p> sc.png",
    ##@ do we need this ??  
    # "Take Picture": "input keyevent 27",  # input keyevent KEYCODE_CAMERA"
    
    ##@ dont see a need  "Input Text": "input text (text here)",
    # "Switch Applications": "input keyevent 187",
    # "Device Model": "getprop ro.product.model",
    # "Screen Size": "wm size",
    # "Screen Density": "wm density",
    #  "Android Version": "getprop ro.build.version.release",
    # "Pull Image to PC": "screencap -p /sdcard/sc.png",    doesnt quite work?
    # "Screen Record Phone": "screenrecord /sdcard/filename.mp4",  #  -- "--bit-rate 2000" "--time-limit 60" "--size 300x300"
}


### Swipe to Unlock
def swipe_to_unlock(device, x1=None, x2=None, y1= None, y2=None):
    "Swipe to unlock function"
    try:
        device.shell(f'input swipe {x1} {x2} {y1} {y2}')
    except:
        g_log.error("error swiping")


def format_temperature(device, aformat):
    """
    THIS SHOULD PULL FROM PLUGIN SETTINGS TO DECIDE IF C OR F
    """
    temp = float(device['temperature']) / 10.0
    if aformat == "Celcius":
        return f"{temp} °C"
    else:
        return f'{(temp * 9/5) + 32} °F'



def create_states():
    """ Creates and or Updates States as Needed """
    count2=1
    for adevice in device_list:
        device = (device_list[adevice])  ### The Device Info Saved
        
        sleep = check_sleep(device['ID'])  ## Checking Sleep States
        
        
        temp_formatted = format_temperature(device, "Fahrenheit")
        
        cpu_usage = device.get('CPU USAGE')
      # memfree=""
      # first_math = (int(device['MemTotal']) / int(device['MemFree']))
      # memfree = first_math*10
        
        
        TPClient.createStateMany([
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.Version',
        "desc": f"{device['Model']} Android Version",
        "value": str(device['Version']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.Hardware',
        "desc": f"{device['Model']} Hardware ",
        "value": str(device['Hardware']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.Manufacturer',
        "desc": f"{device['Model']} Manufacturer",
        "value": str(device['Manufacturer']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.Model',
        "desc": f"{device['Model']} Model",
        "value": f"{device['Model']}",
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.ScreenSize',
        "desc": f"{device['Model']} Screen Size",
        "value": str(device['Screen Size']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.BatteryStatus',
        "desc": f"{device['Model']} Battery Status",
        "value": str(device['status']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.BatteryLevel',
        "desc": f"{device['Model']} Battery Level",
        "value": str(device['level']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.BatteryTemperature',
        "desc": f"{device['Model']} Battery Temperature",
        "value": str(temp_formatted)[0:4]+ "°",
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.BatteryVoltage',
        "desc": f"{device['Model']} Battery Voltage",
        "value": str(device['voltage']+" mV"),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.BatteryHealth',
        "desc": f"{device['Model']} Battery Health",
        "value": bat_state_conver(choice='health',num=int(device['health'])),
        'parentGroup': device['Model']
        },
        ## add "AC powered", "USB powered", "Wireless powered"
        
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.cpu_usage',
        "desc": f"{device['Model']} CPU Usage",
        "value": "0" if cpu_usage == None else str(device['CPU USAGE']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.MemoryTotal',
        "desc": f"{device['Model']} Memory Total",
        "value": str(device['MemTotal']),
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.MemoryAvailable',
        "desc": f"{device['Model']} Memory Available",
        "value": device['MemAvailable'],
        'parentGroup': device['Model']
        },
        {
        "id": PLUGIN_ID + f'.device.{device["Model"]}.screen_on',
        "desc": f"{device['Model']} Sleep State",
        "value": "" if sleep == None else (str(sleep)),
        'parentGroup': device['Model']
        }
        ])
        count2 = count2+1





def get_current_app_loop(device: object, name:str)-> None:
    """ 
    Retrieves the current app every 2 Seconds and updates the state
    - This is a threaded loop
    """
    while True:
        current_app = get_current_app(device)
        
        if current_app:
            TPClient.createState(stateId=PLUGIN_ID + f".device.{name}.current_open_app",
                                 description= f"{name} Current App",
                                 value=current_app,
                                 parentGroup= name
                                 )
        time.sleep(2.0)



def get_current_app(device: object)-> str:
    """ find most recent opened app """
    result = (device.shell("dumpsys activity  activities | grep mResumedActivity"))
    if result:
        last_opened_app = result.split("/")[-2].split(".")[-1]
    else:
        last_opened_app= "None"
        
    return last_opened_app





""" 
NOT IMPLEMENTED YET - 
Now that ParentGroups are available we can add it! 


//This would be a mess if added now due to not
//being able to create states inside a category
"""
def most_recent_5(device: object)-> dict:
    """ 
    check the last 5 apps opened
    """
    
    #-------------------------------------------#
    #---------------NOT IMPLEMENTED-------------#
    #-------------------------------------------#
    result_dict = {}
    last_5_opened={}
    """ This shows last 5 for sure.. maybe use it instead? """
    ### (device.shell("dumpsys activity  activities | grep 'Hist #'"))
    result = device.shell("dumpsys activity  activities | grep mLastPausedActivity")
    for x in result.splitlines():
        first_split = x.split("/")
        activity = first_split[-1]
        previous_app = first_split[-2].split(".")[-1]
        base = first_split[-2].split(" ")[-1]

        if "{" or "}" in activity or base:
            activity = activity.strip("}").strip("{")
            base = base.strip("}").strip("{")

        last_5_opened[previous_app] = {"Activity": activity, "Base": base}
        return last_5_opened






def state_loop_update():
    """ 
    
    Keeps the phones states updated every 5 seconds
    - We could allow users to set this in the settings if requested
    
    """
    while True:
        for x in device_list:
            device_states.get_cpu_usge(device_list[x]['ID'])
            device_states.get_mem_info(device_list[x]['ID'])
            ## have not decided to loop for battery % yet.. until someone notices?? 
            device_states.battery_state_update(device_list[x]['ID'])
        create_states()
        time.sleep(5)
        


def adjust_volume(device:object, volume:str, speaker:str)-> None:
    """ 
    Adjust Device Volume
    - Speaker = Phone": 1, "Notification": 2, "Speaker": 3, "Alarm": 4, "Bluetooth": 6
    """
    # The key that is used to determine what speaker to adjust
    SPEAKER_CHOICES ={"Phone": 1, "Notification": 2, "Speaker": 3, "Alarm": 4, "Bluetooth": 6}
    # Determining what Version of Android and what method to run in shell
    SET_STREAM_VOLUME = {"Android 5": 3, "Android 6": 3, "Android 7": 3,"Android 8": 3, "Android 9": 7, "Android 10": 10,  "Android 11": 10, "Android 12": 11}
    
    set_volume = int(volume) // 4
    
    version = DEVICE_VERSIONS[device]
    android_version = "Android "+ version
    
    if android_version in SET_STREAM_VOLUME:
        if speaker == "Phone":
            set_volume = int(volume) // 10
        device.shell(f'service call audio {SET_STREAM_VOLUME[android_version]} i32 {SPEAKER_CHOICES[speaker]} i32 {int(set_volume)} i32 1')

    time.sleep(0.10)


def adjust_brightness(device:object, level)-> None:
    level = max(6, min(level * 2.6, 255))
    device.shell(f'settings put system screen_brightness {int(level)}')
    


""" Check Sleep State """

def check_sleep(device:object):
    #output = device.shell('dumpsys power | grep -e "mWakefulness=" -e "Display Power"')
    output = device.shell('dumpsys power | grep -e "mWakefulness="')
    output = output.split("=")[-1]
    return output

# def check_sleep2(device:object):
#     try:
#        # ok=(device.shell('dumpsys power | grep "mHolding"'))
#        ### we could find out phone boot time here also.... so if phone has been on more than X hours they can reboot maybe?
#        
#         sleep_state =(device.shell("dumpsys nfc | grep 'mScreenState='"))
#         print(sleep_state)
#         if not sleep_state:
#             
#             sleep_state = device.shell("dumpsys nfc | grep 'Screen State'")
#             sleep_state = sleep_state.split(":")[-1]
#         buf = StringIO(sleep_state)
#         changes = 0
#         
#         """ This was used when grep mHolding"""
#      ###  for line2 in buf.readlines():
#      ###      line = line2.strip()
#      ###      for state, value in sleep_states.items():
#      ###          m = re.search(r'{}=(.*)'.format(state), line)
#      ###          if m:
#      ###              if value != m.group(1):
#      ###                  changes += 1
#      ###                  # print("SLEEP STATE CHANGED: state={} old={} new={}".format(state, value, m.group(1)))
#      ###                  sleep_states[state] = m.group(1)
#      ###       if changes > 0:
#                #pass
#      ###          print("---- {} Sleepstate changes".format(changes))
#      ###       return sleep_states
#         return sleep_state
#     except RuntimeError as err:
#         print(" error on check_sleep... ", err)
        




def install_apk(device:object, apkpath:str)-> bool:
    """
    Returns True/False depending on success
    """
    ## perhaps have a install state?
    if apkpath.endswith(".apk"):
        result = device.install(f"{apkpath}")
        
    return result


def uninstall_apk(device:object, package:str)-> bool:
    """ Returns True/False depending on success"""
    result = device.uninstall(f"{package}")
    return result

def sort_app_list(apps):
    """ Sorts the app list by name """
    applist = [x.split(":")[-1] for x in apps.splitlines()]
    return applist

def get_app_list_choices():
    try:
        for x in device_list:
            ## Get List of Apps on Each Device, then sort them
            apps = device_list[x]['ID'].shell('pm list packages -3')
            applist = sort_app_list(apps)
    except:
        g_log.error("Error or list change")
    try:
        TPClient.choiceUpdate(PLUGIN_ID + '.device.app_list', applist)
    except:
        pass



def build_dicts(devices):
    global device_list
    
    global DEVICE_VERSIONS
    DEVICE_VERSIONS = {} ## Used for volume adjusment when finding version of android
    
    device_dict = {}
    try:
        for value in devices:
            # Pulling Device Details
            device_info = device_states.get_screen_info(value)
            battery_info = device_states.battery_state_update(value)
            mem_info = device_states.get_mem_info(value)

            device_dict = {
                "ID": value,
            }
            device_dict.update(device_info)
            device_dict.update(battery_info)
            device_dict.update(mem_info)

            ## Storing each devices version so we dont have to loop thru it later to adjust volume
            DEVICE_VERSIONS[value] = device_info['Version']
 


            device_list[device_info['Model']] = device_dict
            # Starting Threads for Current App, 1 sec loop
            name = threading.Thread(target=get_current_app_loop, args=(value, device_dict['Model']),daemon=True)
            name.start()
            
    except RuntimeError as err:
        g_log.error("[SNAG HIT] ->  A Device is Offline... We are Skipping it ")
       # print("[SNAG HIT] ->  A Device is Offline... We are Skipping it ")
        print(err)
        
   
    return device_list







############################################################################# ADVANCED LOGGGING THINGS #####################################################################################################
####      THIS IS GOOD FOR FOLKS WHO WANT TO KNOW WHEN AN APP CLOSES AND OR OPENS       ####
APPROVED_LIST = ["SM-A326U", "KFTRWI"]

### SPECIAL PARSING NEEDING PER DEVICE
def check_for_logging(device:object, name:str)->None:
    """ If Device is Compatible with logging then it will start 
    - See Compatible.py (need to make this... :|)
    """
    model = name       
        
    if model in APPROVED_LIST:
        model = threading.Thread(target=log_thread_start, args=(name,device), daemon=True)
        if not model.is_alive():
            model.start()
            g_log.debug(f"Starting Logging Thread for {name}")
            #print("* "*30+" LOGGING STARTED FOR"+model+" *"*30)




#--------------------------------------------------------------------
#------------------- LOGCAT TO FILE ACTIONS -------------------------
#--------------------------------------------------------------------

logging_on=False
def logcat_set(device, logcat_filepath=""):
    ### Starting Logging Thread for Device
    th = threading.Thread(target=logcat_shell_start,args=(device, logcat_filepath),daemon=True)
    th.start()

def logcat_shell_start(device, logcat_filepath=""):
    device.shell("logcat", handler=dump_logcat_by_line_TOFILE)

def dump_logcat_by_line_TOFILE(connect):
    global logging_on
    logging_on=True
    
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=logcat_filepath, level=logging.INFO)
    
    while logging_on:
        file_obj = connect.socket.makefile()
        for index in range(0, 10):
            pre_parse = (file_obj.readline().strip())
            logging.info(pre_parse)
    else:
        g_log.info("Logging Stopped")
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
            handler.close()






#--------------------------------------------------------------------
#--------------------- LOGCAT EXTRA STUFF ---------------------------
#--------------------------------------------------------------------

### SHELL COMMAND TO START LOGGING FOR SET DEVICE
def log_thread_start(name, device):
    if name in APPROVED_LIST:
        if name == "SM-A326U":
            device.shell("logcat ActivityTaskManager:I *:S | grep -E 'START|Removing'", handler=dump_logcat_by_line)
        elif name == "KFTRWI":
            device.shell("logcat ActivityManager:I *:S | grep -E 'Displayed|remove task'", handler=dump_logcat_by_line)


### The Logger - Where States should be updated or queued for update
def dump_logcat_by_line(connect):
    """ The Dump Log by Line - We can Update States Here"""
    while True:
        file_obj = connect.socket.makefile()
        for index in range(0, 10):
            """ Parsing out ActivityManager for app change events """
            pre_parse = (file_obj.readline().strip())
            
            
            ### HOW TO INTRODUCE PER DEVICE PARSING THAT WAY IT DOESNT END UP MESSING UP OTHERS?
            
            #--------------------------------------------------------------------------#
            #--------------------- Samsung SMA326U Parsing ----------------------------#
            #--------------------------------------------------------------------------#
            if "screen_off" in pre_parse:
                g_log.info(f"SCREEN SWITCHED OFF")
            elif "screen_on" in pre_parse:
                g_log.info(f"SCREEN SWITCHED ON")
      
            if "START" in pre_parse:
                if "SCREEN_OFF" in pre_parse:
                    g_log.info(f"SCREEN SWITCHED OFF")
                    
                displayed_app = pre_parse.split("u0")[-1].split("cmp=")[-1].split("/")[0]
                
                g_log.debug(f"DISPLAYED: {displayed_app}")
            if "Removing" in pre_parse:
                ## maybe check if (appDied) in preparse? or 'activityDestroyed'?
                killed_app = (pre_parse.split("u0")[-1].split("/")[0])
                g_log.debug(f"KILLED: {killed_app}")
            
            
            
            #--------------------------------------------------------------------------#
            #----------------- Amazon Fire HD 10 Tablet Parsin ------------------------#
            #--------------------------------------------------------------------------#
            if "Killing" in pre_parse:
                killed_app = pre_parse.split(":")[-2].split(" ")[0].split("/")[0]
                g_log.debug(f"KILLED: {killed_app}")
                
            elif "Displayed" in pre_parse:
               displayed_app = pre_parse.split(":")[-2].split(" ")[-1].split("/")[0]
               g_log.debug(f"DISPLAYED: {displayed_app}")


#############################################################################     END OF LOGGGING THINGS     #####################################################################################################







##################################################################################################
#_________________________________ ANDROID ADB CONNECTION _______________________________________#
device_list_final = []
### Removed device_list=[] here and moved to globals...
def connect(remote_connect_new=False, ip=None, theport=None):
    """ 
    - Initiate Connection to Devices
    
    If Remote Connect
    - IP = Tablet IP
    - Port - Desired Port to Run (5555)
     ------------------------
    - Assume you saved adb path into your Windows environment path
    - Activate debug mode in Android
    - Connect to PC via USB
    - Open command prompt type: adb tcpip 5555
    - Disconnect your tablet or smartphone from pc
    - Open command prompt type: adb connect IPADDRESS (IPADDRESS is the DHCP/IP address of your tablet or smartphone, which you can find by Wi-Fi -> current connected network)
    """
    devices=""          # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037) 
    new_connection=""
                         ### RFC = Device serial
    ### may need 'adb -s RFCRB1D7XFP tcpip 5555'  to restart the server, then do the normal connection.. probably kill-server first?
    if remote_connect_new:    #PORT 5555 RECOMMENDED
        
        g_log.info('attempting a remote connection')
        try:
            g_log.info("Client disconnect?", client.remote_disconnect(ip, int(theport)))
           # print(client.features())
        except:
            pass
        time.sleep(0.2)
        new_connection = client.remote_connect(ip, int(theport))
    
    if not remote_connect_new: 
        notconnected=True
        try:
            devices = client.devices() 
            
            if len(devices) == 0:
                while notconnected:
                    devices = client.devices() 
                    print('No devices')
                    time.sleep(5)
                    if len(devices) >0:
                        notconnected=False
            
        except RuntimeError as err:
            g_log.error(err)
            print(out('adb start-server'))
            time.sleep(2)
            connect()

            
    build_dicts(devices)
    return new_connection



def plugin_update_check(data):
    #-----------------------------#
    #---- Plugin Update Check ----#
    #-----------------------------#
    try:
        github_check = TP.Tools.updateCheck("GitagoGaming", "Android-ADB----TouchPortal-Plugin")
        plugin_version = str(data['pluginVersion'])
        
        if github_check.replace('v','').replace(".","") != plugin_version:
         ### Pulling Patch Notes for Notification
            r = requests.get("https://api.github.com/repos/GitagoGaming/Android-ADB----TouchPortal-Plugin/contents/patchnotes.txt")
            base64_bytes = r.json()['content'].encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')


        TPClient.showNotification(
                notificationId="Gitago_ADB.TP.Plugins.Update_Check",
                title=f"ADB-Android {github_check} is available",
                msg="A new version of ADB-Android is available and ready to Download. This may include Bug Fixes and or New Features",
                options= [{
                "id":"Download Update",
                "title":f"Patch Notes\n{message}\n Click to Update!"
                }])
    except Exception as e:
        g_log.error("Something went wrong checking update")
     #   print("Something went wrong checking update")
        #pass
    

##################################################################################################
#________________________________ TOUCH PORTAL CONNECTION _______________________________________#

old_devices=[]
def handleSettings(settings, on_connect=False):
    global old_devices
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    
    """ Updating Choice Selection on Startup"""
    choice_list = []
    for x in device_list:
        choice_list.append(f"{x}")

    if old_devices != choice_list:
            TPClient.choiceUpdate(PLUGIN_ID + '.device_select', choice_list)
            

    old_devices = choice_list
    



g_log = getLogger()
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



@TPClient.on(TP.TYPES.onNotificationOptionClicked)
def check_noti(data):
    print(data)
    if data['optionId'] == 'Download Update':
        github_check = TP.Tools.updateCheck("GitagoGaming", "Android-ADB----TouchPortal-Plugin")
        out(f"Start https://github.com/gitagogaming/Android-ADB----TouchPortal-Plugin/releases/tag/{github_check}")


#_________________ ON CONNECT _______________#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    
    plugin_update_check(data)
    connect() 
    
    if settings := data.get('settings'):
        handleSettings(settings, True)
    
    
    get_app_list_choices()
        
    th = threading.Thread(target=state_loop_update, daemon=True)
    th.start()
    
    



#__________ON SETTINGS UPDATE ___________#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)



#________ ON LIST CHANGE _______#
@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data):
    print(data)
    if data['actionId'] == PLUGIN_ID + '.device.open_application':
        try:
            ## Get the List of Packages on Device
            apps = match_device(data['value']).shell('pm list packages -3')
            applist = sort_app_list(apps)
        except:
            print("mmmhmm.. error or list change")
        try:
            TPClient.choiceUpdate(PLUGIN_ID + '.device.app_list', applist)
        except:
            pass


    if data['actionId'] == PLUGIN_ID + '.device.remote_connect':
        if data['value']:
            try:
                ip_parse = match_device(data['value']).shell('ip -f inet addr show wlan0')
                device_ip=(ip_parse.split("/")[0].split(" ")[-1])
                TPClient.choiceUpdate(PLUGIN_ID + '.device_remote_connect.ip.choice', ["Custom IP",str(device_ip)])
            except AttributeError as err:
                print("Error...", err)


    if data['actionId'] == PLUGIN_ID + '.device.uninstallAPK':
        try:
            # Get the List of Apps/Packages on Device
            apps = match_device(data['value']).shell('pm list packages -3')
            applist = sort_app_list(apps)
        except:
            print("mmmhmm.. error or list change")
        try:
            TPClient.choiceUpdate(PLUGIN_ID + '.device.app_list', applist)
        except:
            pass





### NEED PUSH TO HOLD VOLUME CONTROLS STILL
### NEED PUSH TO HOLD VOLUME CONTROLS STILL
#________ ON BUTTON HELD DOWN _______#
@TPClient.on(TP.TYPES.onHold_down)
def heldingButton(data):
    print(data)
    while True:
        """ Can make this smoother by using onhold_up and down and then go from 0-100 scale while holding.. just need to find a way to get current volume level"""
        ### ON HOLD SCREEN BRIGHTNESS
        if TPClient.isActionBeingHeld(PLUGIN_ID + '.screenbrightness'):
            if data['data'][1]['value'] == "Down":
               match_device(data['data'][0]['value']).shell(COMMANDS['Reduce Screen Brightness'])
               print("down")
               time.sleep(0.15)    
            elif data['data'][1]['value'] == "Up":
                match_device(data['data'][0]['value']).shell(COMMANDS['Increase Screen Brightness'])
                time.sleep(0.15)
        
        elif TPClient.isActionBeingHeld(PLUGIN_ID + '.volume'):
            if data['data'][1]['value'] == "Down":
                
          #     the_states = TPClient.getStatelist()
          #     the_states[f'{PLUGIN_ID}.device.{model}.volume'] 
          #  #  adjust_volume(device=match_device(data['data'][0]['value']),
          #  #                volume=data['value'],
          #  #                speaker= 1)
                ## we have no way to get the current volume of the device 
                ## we could use the 0-100 we would set ourselves..

                match_device(data['data'][0]['value']).shell(COMMANDS['Decrease Volume'])
                time.sleep(0.15)
            elif data['data'][1]['value'] == "Up":
                match_device(data['data'][0]['value']).shell(COMMANDS['Increase Volume'])
                time.sleep(0.15)
        else:
            break



#_________ ON CONNECTOR CHANGE  _________#
@TPClient.on(TP.TYPES.onConnectorChange)
def connectors(data):
    g_log.debug(f"Connector: {data}")
    if data['connectorId'] == PLUGIN_ID + ".VolumeMixer.connectors":
        adjust_volume(device=match_device(data['data'][0]['value']), volume=data['value'], speaker= data['data'][1]['value'])
    
    if data['connectorId'] == PLUGIN_ID + ".device.brightness.slider":
        adjust_brightness(device=match_device(data['data'][0]['value']), level=data['value'])



#_________________ ON ACTIONS _______________#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    g_log.info(f"Action: {data}")
    if data['actionId'] == PLUGIN_ID + ".device_commands":
        ## all command choices should match the key in COMMANDS dict so no need for all the extra ifs anylonger
        match_device(data['data'][0]['value']).shell(COMMANDS[data['data'][0]['value']])

    
    if data['actionId'] == PLUGIN_ID + ".device.open_application":
        if data['data'][2]['value'] == "Open":
            match_device(data['data'][0]['value']).shell(f"monkey -p {data['data'][1]['value']} -c android.intent.category.LAUNCHER 1")
        if data['data'][2]['value'] == "Close":
            match_device(data['data'][0]['value']).shell(f"am force-stop {data['data'][1]['value']}")
        
    if data['actionId'] == PLUGIN_ID + ".device.key_input":
        match_device(data['data'][0]['value']).shell(f"input keyevent {data['data'][1]['value']}")
        
    ### SWIPE TO UNLOCK
    if data['actionId'] == PLUGIN_ID + ".device_swipeunlock":
        swipe_to_unlock(device=match_device(data['data'][0]['value']), x1=data['data'][1]['value'], x2=data['data'][2]['value'], y1=data['data'][3]['value'], y2=data['data'][4]['value'])
        
        
    ### POWER CONTROLS
    if data['actionId'] == PLUGIN_ID + ".device.display":
        if data['data'][1]['value'] == "On":
            match_device(data['data'][0]['value']).shell(COMMANDS['Turn On Screen'])
        elif data['data'][1]['value'] == "Off":
            match_device(data['data'][0]['value']).shell(COMMANDS['Turn Off Screen'])


    ### VOLUME CONTROL
    if data['actionId'] == PLUGIN_ID + ".volume":
        if data['data'][1]['value'] == "Up":
            match_device(data['data'][0]['value']).shell(COMMANDS['Increase Volume'])
        else:
            match_device(data['data'][0]['value']).shell(COMMANDS['Decrease Volume'])
            

    ### DEVICE SCREENSHOT 
    if data['actionId'] == PLUGIN_ID + ".device.screenshot":
        filename = data['data'][1]['value']
        save_directory = data['data'][2]['value']
        if filename.endswith(".png") or filename.endswith(".jpg"):
            """ Screenshot Device"""
            match_device(data['data'][0]['value']).shell(f'screencap -p /sdcard/{filename}')
            if save_directory:
                """ Pull Screenshot to PC"""
                match_device(data['data'][0]['value']).pull(f"/sdcard/{filename}", f"{save_directory}/{filename}")

    ### TEXT INPUT
    if data['actionId'] == PLUGIN_ID + ".device.commands.text_input":
        match_device(data['data'][0]['value']).shell(f"input text {data['data'][1]['value']}")


    ### CAMERA CONTROLS
    if data['actionId'] == PLUGIN_ID + ".device.commands_camera":
        if data['data'][1]['value'] == "Open Camera":
                match_device(data['data'][0]['value']).shell('am start -a android.media.action.STILL_IMAGE_CAMERA')  ## Open Camera
        if data['data'][1]['value'] == "Focus Camera":
                match_device(data['data'][0]['value']).shell(COMMANDS['Focus Camera'])  ## Focus Camera
        if data['data'][1]['value'] == "Take Photo":
                match_device(data['data'][0]['value']).shell(COMMANDS['Take Picture'])  ## Take Photo  or 27

    if data['actionId'] == PLUGIN_ID + ".device.commands.tap_input":
        match_device(data['data'][0]['value']).shell(f"input tap {data['data'][1]['value']} {data['data'][2]['value']}")
    
    if data['actionId'] == PLUGIN_ID + ".device.connectnew":
        """ This should disconnect/reconnect and create new states again"""
        connect()
        time.sleep(3)
        
    if data['actionId'] == PLUGIN_ID + ".device.remote_connect":
        """ This should disconnect/reconnect and create new states again"""
        response = (connect(remote_connect_new=True, ip=(data['data'][1]['value']), theport=5555))
        
        
    if data['actionId'] == PLUGIN_ID + ".device.logcat":
        """
        0 = Device
        1 = Start / Stop / Clear
        2 = File Path
        """
        global logcat_filepath
        logcat_filepath = data['data'][2]['value']
        if data['data'][1]['value'] == "Start":
            logcat_set(device=match_device(data['data'][0]['value']), logcat_filepath=logcat_filepath)
            
        if data['data'][1]['value'] == "Stop":
            global logging_on
            logging_on=False
            
        if data['data'][1]['value'] == "Clear":
            match_device(data['data'][0]['value']).shell('logcat -c')




    if data['actionId'] == PLUGIN_ID + ".device.installAPK":
        g_log.info("Installing", data['data'][1]['value'], "on to", data['data'][0]['value'])
      #  print("Installing", data['data'][1]['value'], "on to", data['data'][0]['value'])
        TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "INSTALL RUNNING")
        apk_install = install_apk(match_device(data['data'][0]['value']), data['data'][1]['value'])
        
        if apk_install:
            TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "APK INSTALLED")
        if not apk_install:
            TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "INSTALL FAILED")
        
        
    if data['actionId'] == PLUGIN_ID + ".device.uninstallAPK":
        g_log.info("Uninstalling", data['data'][1]['value'], " from ", data['data'][0]['value'])
     #   print("Uninstalling", data['data'][1]['value'], " from ", data['data'][0]['value'])
        TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "UNINSTALL STARTED")
        
        """ If Custom is None, Then use the other field"""
        if not data['data'][2]['value']:
            apk_uninstall = uninstall_apk(match_device(data['data'][0]['value']), data['data'][1]['value'])
        elif data['data'][2]['value']:
            apk_uninstall = uninstall_apk(match_device(data['data'][0]['value']), data['data'][2]['value'])
            
        if apk_uninstall:
            TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "APK UNINSTALLED")
        if not apk_uninstall:
            TPClient.stateUpdate(PLUGIN_ID + '.apk_installresults', "UNINSTALL FAILED")
            
            
        
        
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return





  #  else:
  #      g_log.warning("Got unknown action ID: " + aid)

#_______ ON SHUTDOWN ______#"""
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')
    quit()


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
                g_log.error(f"Error while creating file logger, falling back to stdout. {repr(e)}")
             #   print(f"Error while creating file logger, falling back to stdout. {repr(e)}")
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
    
    
    



""" Do people want to actually record X seconds of footage on their device.. then transfer it to PC ? ..."""
## Screen record up to 180secs - adb shell screenrecord /sdcard/filename.mp4
#       --size WIDTHxHEIGHT	The size of the video, such as 1280x720, the default is the screen resolution.
#       --bit-rate RATE	The bit rate of the video, the default is 4Mbps.
#       --time-limit TIME	Recording duration, in seconds.
#       --verbose	Output more information.
#Video capture mode: adb shell "am start -a android.media.action.VIDEO_CAPTURE"

### need a GO TO WEBSITE ACTIONS
