from machine import Pin, PWM

class DCMotor:      
  def __init__(self, pin1, pin2, pin_enable, freq=100, min_duty=0, max_duty=65535):
#      min_duty=750, max_duty=1023):
      
        self.pin1 = Pin(pin1, Pin.OUT) 
        self.pin2 = Pin(pin2, Pin.OUT)
        
        self.min_duty = min_duty
        self.max_duty = max_duty
        
        if hasattr(self, 'enable_pin'):
            print ('deinit pwm')
            self.enable_pin.deinit()
        
        self.enable_pin = PWM(Pin(pin_enable))
        self.enable_pin.freq(freq)
        
##############################################################                                          
        
  def up(self,speed=100):

    self.speed = speed
        
    self.duty_cycle = self.get_duty_cycle(speed)
   
    print('up....',speed, self.duty_cycle)
#    self.enable_pin.duty_ns(self.duty_cycle(self.speed))

#    self.enable_pin.duty_ns(self.duty_cycle)
    self.enable_pin.duty_u16(self.duty_cycle)                            
    self.pin1.value(0)
    self.pin2.value(1)
    
##############################################################    
  
  def down(self, speed=100):
      
    self.speed = speed
        
    self.duty_cycle = self.get_duty_cycle(speed)

    print('dwn....',speed, self.duty_cycle)

    self.enable_pin.duty_u16(self.duty_cycle)   
    self.pin1.value(1)
    self.pin2.value(0)

##############################################################
    
  def stop(self):
    self.enable_pin.duty_ns(0)
    self.pin1.value(0)
    self.pin2.value(0)
    
##############################################################
    
  def get_duty_cycle(self, speed):
   if self.speed <= 0 or self.speed > 100:
        duty_cycle = 0
   else:
    duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed-1)/(100-1)))
    return duty_cycle