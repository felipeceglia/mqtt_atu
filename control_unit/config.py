SSID = "ssid"
PASSWORD = "wifipassword"

DEVICE_NAME = 'atu' 

MQTT_SERVER = "mqtt-radio"
MQTT_CLI_ID = "xpto"
MQTT_TOPIC_PUB = b'MQTT_ATU/' + DEVICE_NAME + '/cmd'
MQTT_TOPIC_SUB = b'MQTT_ATU/' + DEVICE_NAME + '/info'

MSG_LEVEL = 'debug'

BUTTONS = [
    {'name':'L_up1',  'action':'L',  'pin': 10, 'val':1},
    {'name':'L_up2',  'action':'L',  'pin': 11, 'val':2},
    {'name':'L_dwn1', 'action':'L', 'pin': 12, 'val':-1},
    {'name':'L_dwn2', 'action':'L', 'pin': 13, 'val':-2},

    {'name':'L_xtr1', 'action':'L_xtr1', 'pin': 9, 'val':2},

    {'name':'C_up1',  'action':'C_up',  'pin': 2, 'val':1},
    {'name':'C_up2',  'action':'C_up',  'pin': 3, 'val':2},
    {'name':'C_dwn1', 'action':'C_dwn', 'pin': 4, 'val':1},
    {'name':'C_dwn2', 'action':'C_dwn', 'pin': 5, 'val':2},
    
    {'name':'C_xtr1', 'action':'C_xtr1', 'pin': 8, 'val':2},

#    {'name':'L_up',   'pin': 13, 'val':1},
]
