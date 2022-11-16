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
    {'name':'L_up_slow',  'dst':SLAVE_ID, 'action':'L', 'pin': 10, 'msg': 'up|', 'speed':50, 'adc_pin': 28},
    {'name':'L_up2_fast', 'dst':SLAVE_ID, 'action':'L', 'pin': 11, 'msg': 'up|', 'speed':100},
    {'name':'L_dwn_slow', 'dst':SLAVE_ID, 'action':'L', 'pin': 12, 'msg': 'dwn|','speed':50, 'adc_pin': 28},
    {'name':'L_dwn_fast', 'dst':SLAVE_ID, 'action':'L', 'pin': 13, 'msg': 'dwn|','speed':100},

    {'name':'L_xtr1', 'dst':SLAVE_ID, 'action':'L_xtr1', 'pin': 9, 'msg':2},

    {'name':'C_up1', 'dst':SLAVE_ID, 'action':'C',  'pin': 2, 'msg': 1},
    {'name':'C_up2', 'dst':SLAVE_ID, 'action':'C',  'pin': 3, 'msg': 2},
    {'name':'C_dwn1','dst':SLAVE_ID, 'action':'C', 'pin': 4, 'msg':-1},
    {'name':'C_dwn2','dst':SLAVE_ID, 'action':'C', 'pin': 5, 'msg':-2},
    
    {'name':'C_xtr1', 'action':'C_xtr1', 'pin': 8, 'msg':2},

#    {'name':'L_up',   'pin': 13, 'msg':1},
]

ADC_SPEED = {
    'L': { 'pin': 28, 'pct_step':2, 'pct_min':10, 'adc_max':65100, 'dst':SLAVE_ID },
    }


    