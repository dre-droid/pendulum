import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor driver pins
IN1_PIN = 25    # GPIO25 for IN1 (direction control)
IN2_PIN = 24    # GPIO24 for IN2 (direction control)
EN_PIN = 6      # GPIO6 for EN (Enable, active high)

# Setup pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

def test_motor_full_power():
    try:
        print("Starting full power motor test...")
        print("Applying 12V across motor terminals (OUT1 to OUT2)")
        
        # Enable the motor driver
        GPIO.output(EN_PIN, GPIO.HIGH)
        print("Motor driver enabled")
        
        # Set direction to create 12V potential (IN1 high, IN2 low)
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        print("Direction set - running at full power")
        
        # Run for 2 seconds
        time.sleep(2)
        
        print("Motor test complete")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Cleanup
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(EN_PIN, GPIO.LOW)   # Disable motor driver
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    test_motor_full_power() 