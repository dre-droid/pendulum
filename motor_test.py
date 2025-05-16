import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor pins
MOTOR_PIN = 12  # GPIO12 for both IN1 and IN2
PWM_FREQ = 1000  # 1kHz PWM frequency
DUTY_CYCLE = 10  # 10% duty cycle for low power test

# Setup PWM pin
GPIO.setup(MOTOR_PIN, GPIO.OUT)
pwm = GPIO.PWM(MOTOR_PIN, PWM_FREQ)

def test_motor():
    try:
        print("Starting motor test...")
        print(f"Running at {DUTY_CYCLE}% power")
        
        # Start PWM
        pwm.start(DUTY_CYCLE)
        
        # Run for 2 seconds
        time.sleep(2)
        
        # Stop motor
        pwm.stop()
        print("Motor test complete")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Cleanup
        pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    test_motor() 