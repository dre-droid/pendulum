import time
import RPi.GPIO as GPIO
import spidev

class FurutaHardware:
    def __init__(self):
        # Motor control setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)  # IN1
        GPIO.setup(13, GPIO.OUT)  # IN2
        self.motor_pwm1 = GPIO.PWM(12, 1000)
        self.motor_pwm2 = GPIO.PWM(13, 1000)
        self.motor_pwm1.start(0)
        self.motor_pwm2.start(0)
        
        # SPI setup for encoders
        self.spi0 = spidev.SpiDev()
        self.spi1 = spidev.SpiDev()
        self.spi0.open(0, 0)  # Bus 0, Device 0
        self.spi1.open(1, 0)  # Bus 1, Device 0
        self.spi0.max_speed_hz = 1000000
        self.spi1.max_speed_hz = 1000000

    def read_encoders(self):
        """Read both encoder values"""
        # You'll need to adjust this based on your encoder protocol
        motor_angle = self._read_spi(self.spi0)
        pendulum_angle = self._read_spi(self.spi1)
        return motor_angle, pendulum_angle

    def set_motor(self, power, direction):
        """Set motor power (-1 to 1) and direction"""
        power = max(-1, min(1, power))  # Clamp between -1 and 1
        duty_cycle = abs(power) * 100
        
        if direction:
            self.motor_pwm1.ChangeDutyCycle(duty_cycle)
            self.motor_pwm2.ChangeDutyCycle(0)
        else:
            self.motor_pwm1.ChangeDutyCycle(0)
            self.motor_pwm2.ChangeDutyCycle(duty_cycle)

    def _read_spi(self, spi):
        """Read encoder value over SPI"""
        # Placeholder - implement based on your encoder protocol
        resp = spi.xfer([0x00, 0x00, 0x00, 0x00])
        return (resp[0] << 24) | (resp[1] << 16) | (resp[2] << 8) | resp[3]

    def close(self):
        """Cleanup"""
        self.motor_pwm1.stop()
        self.motor_pwm2.stop()
        self.spi0.close()
        self.spi1.close()
        GPIO.cleanup()

# Test script
if __name__ == "__main__":
    robot = FurutaHardware()
    try:
        print("Testing hardware...")
        print("Reading encoders...")
        motor_angle, pendulum_angle = robot.read_encoders()
        print(f"Motor angle: {motor_angle}, Pendulum angle: {pendulum_angle}")
        
        print("\nTesting motor...")
        print("Moving forward at 50% power")
        robot.set_motor(0.5, True)
        time.sleep(1)
        
        print("Moving backward at 50% power")
        robot.set_motor(0.5, False)
        time.sleep(1)
        
        print("Stopping motor")
        robot.set_motor(0, True)
        
    finally:
        robot.close()
