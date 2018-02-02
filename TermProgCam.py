import RPi.GPIO as GPIO
import time
import picamera

GPIO.setmode(GPIO.BCM)

camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds = 3)
trigger = 23
echo = 24

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, False)

def getDistance():
  GPIO.output(trigger, True)
  time.sleep(0.00001)
  GPIO.output(trigger, False)

  while GPIO.input(echo) == 0:
    pulse_start = time.time()

  while GPIO.input(echo) == 1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  return distance

def control():
  # distance in cm
  zone = 100
  curr = 999
  camera.start_recording(stream, format = 'h264')
  try:
    while(True):
      curr = getDistance()
      camera.wait_recording(1)
      if(curr <= zone):
        print curr
        camera.wait_recording(10)
        stream.copy_to('motion.h264')

  finally:
    camera.stop_recording()

control()
GPIO.cleanup()

