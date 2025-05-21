import RPi.GPIO as GPIO
import time

# Pin definitions (BCM numbering)
IN1_PIN = 25    # GPIO25 for direction control
IN2_PIN = 24     # GPIO24 for direction control
D2_PIN = 12      # GPIO12 for PWM control (active low)
EN_PIN = 6       # GPIO6 for Enable
SF_PIN = 2      # GPIO2 for SF

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
#GPIO.setup(D2_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.setup(SF_PIN, GPIO.IN)
# Initialize PWM
#pwm = GPIO.PWM(D2_PIN, 1000)  # 1 kHz frequency
#pwm.start(0)

# Enable motor driver
GPIO.output(EN_PIN, GPIO.HIGH)

def motor_test():
    try:
        #read status flag
        print("SF: ", GPIO.input(SF_PIN))
        time.sleep(1)

        # Spin forward
        print("Spinning forward")
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        print("In1, In2: ", GPIO.input(IN1_PIN), GPIO.input(IN2_PIN))
        #pwm.ChangeDutyCycle(50)
        time.sleep(3)

        #read status flag
        print("SF: ", GPIO.input(SF_PIN))
        time.sleep(1)
        
        # Stop
        print("Stopping")
        pwm.ChangeDutyCycle(0)

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        pwm.stop()
        GPIO.output(EN_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("Test complete - GPIO cleaned up")

if __name__ == "__main__":
    motor_test()