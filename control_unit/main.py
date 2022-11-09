import network
import config
import time
import urequests
import utime


from machine import Pin
#from umqtt.simple import MQTTClient
from umqtt.robust2 import MQTTClient

def echo(msg, level='info'):
    print(level.upper(), msg)


led_mqtt = Pin(15, Pin.OUT)
led_mqtt.value(0)
    
echo('starting...')

##############################################################
echo (f'connecting to wifi: {config.SSID}...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.SSID, config.PASSWORD)
time.sleep(5)
if wlan.isconnected():
    echo (f'connected to wifi: {config.SSID}')
##############################################################    
    
sensor = Pin(16, Pin.IN)

#TODO

state = 0

##############################################################
def mqtt_sub_cb(topic, msg, retained, duplicate):
    echo((topic, msg, retained, duplicate))
    #print(utime.ticks_ms())

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
        mqtt_client.subscribe(b"/CT7ANO/atu/remote/pong/#")
    
    echo(f'Connected to mqtt server: {config.MQTT_SERVER}')
    
    led_mqtt.value(1)
    
    mqtt_client.publish(config.MQTT_TOPIC_PUB + '/hello', 'hello')
    
    return mqtt_client

##############################################################  
def mqtt_reconnect():
    echo('Failed to connect to the MQTT Broker. Reconnecting...')
    led_mqtt.value(0)
    time.sleep(5)
    machine.reset()


##############################################################  
# This function gets called every time the button is pressed.  The parameter "pin" is not used.
def btn_handler(p):

    #ugly hack, but kind of works
    pin = int(str(p)[4:6].rstrip(','))
    
    global btn_last_time
    #global btn_presses
    global btn_map

    new_time = utime.ticks_ms()
    elapsed_time = new_time - btn_last_time[pin]
    
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if elapsed_time > 75:
        b = btn_map[pin]
        
        if elapsed_time < 500:
            print('meio')
            if b['val'] != b['last_val']:
                echo('let it coast', 'debug')
        
        echo(('pressed pin', pin, btn_map[pin]['name'], 'state', state, 'elapsed', elapsed_time, 'value', p.value()), 'debug')
        #btn_presses[pin] +=1
        btn_last_time[pin] = new_time

        mqtt_topic = config.MQTT_TOPIC_PUB + '/' + b['action']
    
        if p.value() == 0:
             mqtt_msg = 0
        else:
            mqtt_msg = b['val']

        echo((mqtt_topic, mqtt_msg, b['last_val']))
        
        mqtt_client.publish(mqtt_topic, str(mqtt_msg))
        
        b['last_val'] = mqtt_msg
        
        return

##############################################################  


buttons = config.BUTTONS

btn_map 		= {}
btn_last_time 	= {}
btn_last_state 	= {}
#btn_presses 	= {}
pins_in 		= {}


##############################################################  
for d in buttons:
    print(('setting pin', d['pin'], d['name']), 'debug')
    btn_map[d['pin']] 		= d
    btn_map[d['pin']]['last_val'] = 0
    btn_last_time[d['pin']] = 0
    btn_last_state[d['pin']]= False
    #btn_presses[d['pin']] 	= 0
        
    pins_in[d['pin']] = machine.Pin(d['pin'], machine.Pin.IN, machine.Pin.PULL_DOWN)
    pins_in[d['pin']].irq(trigger=machine.Pin.IRQ_FALLING, handler=btn_handler)

##############################################################  

try:
    mqtt_client = mqtt_connect()
except OSError as e:
    mqtt_reconnect()

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
        mqtt_client.publish(config.MQTT_TOPIC_PUB + '/ping', str(utime.ticks_ms()))
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

