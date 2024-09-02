

# Setup the PWM pin
pwm_output = gpiozero.PWMOutputDevice(18)  # Connect to GPIO18 (you can change to your pin)

try:
    while True:
        if is_pressed('1'):  # If key '1' is pressed
            pwm_output.value = 1.0  # Send 100% PWM signal (simulate 5V)
        else:
            pwm_output.value = 0.0  # Turn off the signal
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Program terminated")

finally:
    pwm_output.close()  # Cleanup
import gpiozero
from keyboard import is_pressed
import time