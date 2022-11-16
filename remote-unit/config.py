SERVICE_NAME = 'atu' 
DEVICE_ID = "remote_unit"

MASTER_ID = "control_unit"
SLAVE_ID = "remote_unit"

MQTT_SERVER = "mqtt-radio"
MQTT_CLI_ID = SERVICE_NAME + '-' + DEVICE_ID

MQTT_TOPIC_PUB = b'/CT7ANO/' + SERVICE_NAME

MQTT_TOPIC_SUB = b'/CT7ANO/' + SERVICE_NAME + '/cmd/' + SLAVE_ID + '/#'


MQTT_PING_PERIOD = 5000 #ms

MSG_LEVEL = 'debug'



dc_motors = {
    #ok para motor de teste, tipo parabrisa solto
    'L': {
        'pin_up': 16, 'pin_dwn':17, 'pin_pwm':18, 'freq': 15, 'min_duty':1000, 'min_speed':10
        }
    }
