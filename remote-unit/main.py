import config
import config_wifi

import network
import time
import urequests
import utime

from dcmotor import DCMotor
from machine import Pin, PWM

#from umqtt.simple import MQTTClient
from umqtt.robust2 import MQTTClient

def echo(msg, level='info'):
    print(level.upper(), msg)


led_mqtt = Pin(15, Pin.OUT)
led_mqtt.value(0)
    
echo('starting REMOTE UNIT...')

##############################################################

def wifi_connect(ssid, passwd):
    #global config

 #  connect to the internet
    sta_if = network.WLAN(network.STA_IF)
    count = 0

    #echo(f'wifi connecting to {ssid}')
    
    if not sta_if.isconnected():
        echo(f'connecting to wifi {ssid} ...')
        sta_if.active(True)
        #sta_if.ifconfig(('192.168.10.99', '255.255.255.0', '192.168.10.1', '8.8.8.8'))
        sta_if.connect(ssid, passwd)

        while (count < 5):
            count += 1

            status = sta_if.status()

            #try:
            #    with open('errors.txt', 'a') as outfile:
            #        outfile.write('connect status = ' + str(status) + '\n')
            #except OSError:
            #    print('oops')

            if (sta_if.isconnected()):
                count = 0
                break

            #print('.', end = '')
            utime.sleep(1)

    if (count == 5):
        count = 0

        echo(f'cannot connect to wifi {ssid}, resetting')
        utime.sleep(2)
        machine.reset()


    echo(f'wifi connected to {ssid}')
    echo(('network config:', sta_if.ifconfig()))

wifi_connect(config_wifi.SSID, config_wifi.PASSWORD)

##############################################################


# ##############################################################
# echo (f'connecting to wifi: {config_wifi.SSID}...')
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(config_wifi.SSID, config_wifi.PASSWORD)
# time.sleep(5)
# if wlan.isconnected():
#     echo (f'connected to wifi: {config_wifi.SSID}')
##############################################################    
    
sensor = Pin(16, Pin.IN)

#TODO

dc_motors = {}

def dc_motors_init():
    global dc_motors
    dc_motors = config.dc_motors
    
    for idx, m in config.dc_motors.items():
        echo(f'initializing dc_motor {idx}: {m}')
        dc_motors[idx]['m'] = DCMotor(m['pin_up'], m['pin_dwn'], m['pin_pwm'], m['freq'], m['min_duty'])

#dc_motor = LM298(16, 17, 18)

##############################################################
speed = 100
freq = 15000

def mqtt_sub_cb(topic, msg, retained, duplicate):
    #echo((topic, msg, retained, duplicate))
    #print(utime.ticks_ms())
#    global dc_motor
    global speed
    global freq
    global dc_motors
    
    msg = msg.decode()
    
    topic = topic.decode("utf-8").split('/')
    
    #a ping message, reply with pong
    if (topic[-1] == 'ping' and topic[-3] == config.DEVICE_ID):
        mqtt_client.publish(config.MQTT_TOPIC_PUB + '/info/' + topic[-2] + '/' + config.DEVICE_ID + '/pong', msg)
        
    ##############################################################    
    if ((topic[-1] == 'L' or topic[-1] == 'C') and topic[-3] == config.DEVICE_ID):

        name = topic[-1]

        action, speed = msg.split('|')
        speed = int(speed)

        echo (f'got command {msg}')

        if speed < dc_motors[name]['min_speed']:
            speed = dc_motors[name]['min_speed']
        elif speed > 100:
            speed = 100
        
        if action == 'up':
            dc_motors[name]['m'].up(speed)

        elif action == 'dwn':
            dc_motors[name]['m'].down(speed)

            
        elif action == 'stop':
            dc_motors[name]['m'].stop()
            
    ##############################################################

##############################################################

def mqtt_connect():
    global mqtt_client
    
    mqtt_client = MQTTClient(
            config.MQTT_CLI_ID,
            config.MQTT_SERVER,
            #keepalive=3600,
    )
    
    
    mqtt_client.DEBUG = True
    mqtt_client.KEEP_QOS0 = False
    # Option, limits the possibility of only one unique message being queued.
    mqtt_client.NO_QUEUE_DUPS = True
    # Limit the number of unsent messages in the queue.
    mqtt_client.MSG_QUEUE_MAX = 2

    mqtt_client.set_callback(mqtt_sub_cb)
    
    #mqtt_client.connect()
    
    if not mqtt_client.connect(clean_session=False):
        print("New session being set up")
    
    echo(f'Connected to mqtt server: {config.MQTT_SERVER}')

    sub = config.MQTT_TOPIC_SUB
    #sub = '/CT7ANO/atu/cmd/ping/remote_unit'
    #sub = str.encode(sub)
    echo(('mqtt subscribing to', sub))
    mqtt_client.subscribe(sub)
    
    
    led_mqtt.value(1)
    
    mqtt_client.publish(config.MQTT_TOPIC_PUB + '/' + config.DEVICE_ID + '/hello', 'hello')
    
    return mqtt_client

##############################################################  

def mqtt_reconnect():
    echo('Failed to connect to the MQTT Broker. Reconnecting...')
    led_mqtt.value(0)
    time.sleep(5)
    machine.reset()

##############################################################  

dc_motors_init()

try:
    mqtt_client = mqtt_connect()
except OSError as e:
    #mqtt_reconnect()
    echo('x')
##############################################################  


builtin_led = machine.Pin(15, Pin.OUT)


sleep_ms = 100
ping_interval = config.MQTT_PING_PERIOD / sleep_ms

i_ping = 0

while True:
    utime.sleep_ms(sleep_ms)
    
    ##############################################################

    i_ping += 1
    if i_ping == ping_interval:
        i_ping = 0

    ##############################################################

    if mqtt_client.is_conn_issue():
        while mqtt_client.is_conn_issue():
            # If the connection is successful, the is_conn_issue
            # method will not return a connection error.
            mqtt_client.reconnect()
        else:
            mqtt_client.resubscribe()
               
    mqtt_client.check_msg() # needed when publish(qos=1), ping(), subscribe()
    mqtt_client.send_queue()  # needed when using the caching capabilities for unsent messages

mqtt_client.disconnect()
led_mqtt.value(0)

