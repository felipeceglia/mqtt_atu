SERVICE_NAME = 'atu' 
DEVICE_ID = "control_unit"

MASTER_ID = "control_unit"
SLAVE_ID = "remote_unit"

MQTT_SERVER = "mqtt-radio"
MQTT_CLI_ID = "xpto"

MQTT_TOPIC_PUB = b'/CT7ANO/' + SERVICE_NAME + '/cmd'
MQTT_TOPIC_SUB = b'/CT7ANO/' + SERVICE_NAME + '/info/' + MASTER_ID


MQTT_PING_PERIOD = 5000 #ms

MSG_LEVEL = 'debug'

BUTTONS = [
    {'name':'L_up1', 'dst':SLAVE_ID, 'action':'L', 'pin': 10, 'val': 1},
    {'name':'L_up2', 'dst':SLAVE_ID, 'action':'L', 'pin': 11, 'val': 2},
    {'name':'L_dwn1','dst':SLAVE_ID, 'action':'L', 'pin': 12, 'val':-1},
    {'name':'L_dwn2','dst':SLAVE_ID, 'action':'L', 'pin': 13, 'val':-2},

    {'name':'L_xtr1', 'dst':SLAVE_ID, 'action':'L_xtr1', 'pin': 9, 'val':2},

    {'name':'C_up1', 'dst':SLAVE_ID, 'action':'C',  'pin': 2, 'val': 1},
    {'name':'C_up2', 'dst':SLAVE_ID, 'action':'C',  'pin': 3, 'val': 2},
    {'name':'C_dwn1','dst':SLAVE_ID, 'action':'C', 'pin': 4, 'val':-1},
    {'name':'C_dwn2','dst':SLAVE_ID, 'action':'C', 'pin': 5, 'val':-2},
    
    {'name':'C_xtr1', 'action':'C_xtr1', 'pin': 8, 'val':2},

#    {'name':'L_up',   'pin': 13, 'val':1},
]
