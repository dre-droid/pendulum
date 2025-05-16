import time
import RPi.GPIO as GPIO
import spidev

# LS7366R Commands
CLR_CNTR = 0x20  # Clear counter
RD_CNTR = 0x60   # Read counter
WR_MDR0 = 0x88   # Write to MDR0
WR_MDR1 = 0x90   # Write to MDR1

# MDR0 config: 4X quadrature, free-running count, no index
MDR0_CONF = 0b00000011
# MDR1 config: 4-byte counter, enable counting
MDR1_CONF = 0b00000000

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
        self.spi0.mode = 0b00
        self.spi1.mode = 0b00
        
        # Initialize encoders
        self._setup_encoder(self.spi0)
        self._setup_encoder(self.spi1)

    def _setup_encoder(self, spi):
        """Configure LS7366R encoder"""
        spi.xfer2([WR_MDR0, MDR0_CONF])
        spi.xfer2([WR_MDR1, MDR1_CONF])
        spi.xfer2([CLR_CNTR])  # Clear counter

    def read_encoders(self):
        """Read both encoder values"""
        motor_angle = self._read_encoder(self.spi0)
        pendulum_angle = self._read_encoder(self.spi1)
        return motor_angle, pendulum_angle

    def _read_encoder(self, spi):
        """Read encoder value over SPI using LS7366R protocol"""
        resp = spi.xfer2([RD_CNTR, 0x00, 0x00, 0x00, 0x00])
        return (resp[1] << 24) | (resp[2] << 16) | (resp[3] << 8) | resp[4]

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
