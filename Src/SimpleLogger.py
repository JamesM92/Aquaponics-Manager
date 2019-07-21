import time
import board
import adafruit_lps35hw
     
import busio
import adafruit_sgp30    

import adafruit_veml6075

from datetime import datetime

now = datetime.now() 
  
   
#setup barometric pressure sensor
#lps35hw
LPS35HW = True 
if LPS35HW:
     i2c = board.I2C()
     lps = adafruit_lps35hw.LPS35HW(i2c)
     
#setup air quality sensor
#sgp30    
SGP30 = True
if SGP30:
     i2c2 = busio.I2C(board.SCL, board.SDA, frequency=100000)
     sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c2)
     sgp30.iaq_init()
     sgp30.set_iaq_baseline(0x8987, 0x8d39)

#setup UV index sensor
VEML6075 = True
if VEML6075:
     i2c3 = busio.I2C(board.SCL, board.SDA)
     veml6075 = adafruit_veml6075.VEML6075(i2c3, integration_time=800)


#create data backup text file
date_time = now.strftime("%Y%m%d%H%M%S.txt")
print(date_time)	
elapsed_sec = 0

for i in range(20):
     if LPS35HW:
          Press = lps.pressure
          Temp = lps.temperature
     if SGP30:
          CO2 = sgp30.eCO2
          VOC = sgp30.TVOC
     if VEML6075:
          UVA = veml6075.uva
          UVB = veml6075.uvb
          UVI = veml6075.uv_index
     print("Pressure:%.2f \t TempC: %.2f \t eCO2: %.2f \t VOC: %.2f \t UVA: %.2f \t UVB: %.2f \t UVI: %.2f" %(Press, Temp, CO2, VOC, UVA,UVB,UVI))
     time.sleep(1)
     elapsed_sec += 1
     
with open(date_time, 'a') as out:
     while True:
          now = datetime.now()
          date_time = now.strftime("%Y%m%d%H%M%S")
          if LPS35HW:
               Press = lps.pressure
               Temp = lps.temperature
          if SGP30:
               CO2 = sgp30.eCO2
               VOC = sgp30.TVOC
          if VEML6075:
               UVA = veml6075.uva
               UVB = veml6075.uvb
               UVI = veml6075.uv_index
          print("Pressure:%.2f \t TempC: %.2f \t eCO2: %.2f \t VOC: %.2f \t UVA: %.2f \t UVB: %.2f \t UVI: %.2f" %(Press, Temp, CO2, VOC, UVA,UVB,UVI))
 
          out.write("%s \t %.6f \t %.3f \t %.3f \t %.3f \t %.3f \t %.3f \t %.3f \n" %(date_time, Press, Temp, CO2, VOC,UVA,UVB,UVI))

          if elapsed_sec > 10:
               elapsed_sec = 0
               base_co2 = sgp30.baseline_eCO2
               base_voc = sgp30.baseline_TVOC
               print("**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
			% (base_co2, base_voc))
               out.write("%x \t %x \n" %(base_co2, base_voc))
               
          elapsed_sec += 1
          print("")
          #if datetime.time.hour() == 8 and datetime..minute() == 57:
          #     break
          time.sleep(60)
   
   

 

   


     

     

     
