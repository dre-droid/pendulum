import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor pins
IN1_PIN = 12  # GPIO12 for IN1
IN2_PIN = 13  # GPIO13 for IN2
PWM_FREQ = 1000  # 1kHz PWM frequency
DUTY_CYCLE = 10  # 10% duty cycle for low power test

# Setup PWM pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
pwm_in1 = GPIO.PWM(IN1_PIN, PWM_FREQ)
pwm_in2 = GPIO.PWM(IN2_PIN, PWM_FREQ)

def test_motor():
    try:
        print("Starting motor test...")
        print(f"Running at {DUTY_CYCLE}% power")
        
        # Start PWM on both pins
        pwm_in1.start(DUTY_CYCLE)
        pwm_in2.start(0)  # Keep IN2 at 0% to test one direction
        
        # Run for 2 seconds
        time.sleep(2)
        
        # Stop motor
        pwm_in1.stop()
        pwm_in2.stop()
        print("Motor test complete")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Cleanup
        pwm_in1.stop()
        pwm_in2.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    test_motor() 