from microbit import pin0,pin1,pin2,pin8, pin12,pin16,button_a,button_b
class GamerBit:
 def __init__(self,callback,scans=1):
  self.pins=[pin0,pin1,pin2,pin8,pin12,pin16,button_a,button_b]
  self.callback=callback
  self.number_of_scans=scans
  for pin in self.pins[:-2]:
   pin.set_pull(pin.PULL_UP)
  self.previous_readings=[0]*8
  self.current_readings=[0]*8
  self._scanner()
 def scan(self):
  readings=[int(not pin.read_digital())for pin in self.pins[:-2]]
  readings.append(int(button_a.is_pressed()))
  readings.append(int(button_b.is_pressed()))
  self.current_readings=[int(self.current_readings[pin]or readings[pin])for pin in range(0,len(readings))]
 def _scanner(self):
  pin_ids=['pin0','pin1','pin2','pin8','pin12','pin16','button_a','button_b']
  while True:
   for scans in range(0,self.number_of_scans):
    self.scan()
   report={}
   for x in range(0,8):
    if self.current_readings[x]!=self.previous_readings[x]:
     report[pin_ids[x]]=self.current_readings[x]
   self.previous_readings=self.current_readings
   self.current_readings=[0]*8
   if report:
    if self.callback:
     self.callback(report)


def my_callback(report):
    print('number of elements', len(report))
    for key in report:
        print(key, report[key])


gb = GamerBit(my_callback, 5)