import os
import RPi.GPIO as GPIO

fan = 13           # Pin to which the fan is connected.
threshold = 39     # Temperature in Celsius that, if reached, will trigger the fan.

GPIO.setmode(GPIO.BOARD)
GPIO.setup(fan, GPIO.OUT)

def get_gpu_temp():
    gpu = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
    return gpu


def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    cpu = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
           line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            cpu = float(line) / 1000
    # Give the result back to the caller.
    return cpu


def rule_fan():
    if get_cpu_temp() > threshold:
        GPIO.output(fan, GPIO.HIGH)
    else:
        GPIO.output(fan, GPIO.LOW)
    print("Status = ", GPIO.input(fan))

print("GPU:", get_gpu_temp())
print("CPU:", get_cpu_temp())

rule_fan()
GPIO.cleanup()

