import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor driver pins
IN1_PIN = 25    # GPIO25 for IN1 (direction control)
IN2_PIN = 24    # GPIO24 for IN2 (direction control)
D2_PIN = 12     # GPIO12 for !D2 (PWM control, active low)
EN_PIN = 6      # GPIO6 for EN (Enable, active high)
PWM_FREQ = 1000 # 1kHz PWM frequency
DUTY_CYCLE = 70 # 70% duty cycle (this will give 70% motor power due to D2 being active low)

# Setup pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(D2_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
pwm_d2 = GPIO.PWM(D2_PIN, PWM_FREQ)

def test_motor():
    try:
        print("Starting motor test...")
        print(f"Running at {DUTY_CYCLE}% power")
        
        # Enable the motor driver
        GPIO.output(EN_PIN, GPIO.HIGH)
        print("Motor driver enabled")
        
        # Set direction (IN1 high, IN2 low for one direction)
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        print("Direction set")
        
        # Start PWM on D2 (active low, so 70% duty cycle means 70% motor power)
        pwm_d2.start(DUTY_CYCLE)
        print("PWM started")
        
        # Run for 2 seconds
        time.sleep(2)
        
        # Stop motor by setting D2 high (active low disable)
        pwm_d2.stop()
        GPIO.output(D2_PIN, GPIO.HIGH)
        print("Motor test complete")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Cleanup
        pwm_d2.stop()
        GPIO.output(D2_PIN, GPIO.HIGH)  # Ensure motor is disabled
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(EN_PIN, GPIO.LOW)   # Disable motor driver
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    test_motor() 