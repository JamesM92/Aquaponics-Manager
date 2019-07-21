import time
import board
import busio
import adafruit_veml6075
 
i2c3 = busio.I2C(board.SCL, board.SDA)
 
veml = adafruit_veml6075.VEML6075(i2c3, integration_time=800)
 
print("Integration time: %d ms" % veml.integration_time)
 
while True:
    print(veml.uv_index)
    time.sleep(1)
