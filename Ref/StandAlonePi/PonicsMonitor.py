#!/usr/bin/env python3

### code for monitoring system sensors such as temeprature and water level
### code is built around using the Pi-Plates DAQ2 Plate 
### https://pi-plates.com/daqc2r1/


import piplates.DAQC2plate as daq
import time
import math
import sys

import mysql.connector

ThermistorNominal = 10000
ThermistorTempNom = 25
BCoefficent = 3950
SeriesResistor = 10000

def CalcGallons(Signal,Ref):
	read = Signal / Ref
	read = read * 12
	read = read * 6.6 #converts reading to gallons
	return read

def CalcTemp(Signal,Ref):
	read = Ref / Signal -1
	read = SeriesResistor / read
	read = read / ThermistorNominal
	read = math.log(read)
	read /= BCoefficent
	read += 1/ (ThermistorTempNom + 273.15)
	read = 1 / read
	read -= 273.15
	return read


class rollAvg:
	def __init__(self, valsize):
		self.size = valsize
		self.vals = [0]*valsize

	def AddVal(self,x):
		if(x != 0):
			self.vals.append(x)
			del self.vals[0]

	def GetAvg(self):
		avg = float(sum(self.vals))/self.size
		return avg


def main():
	Time = time.time()
	print ("Wait 15 seconds to allow network connection")
	time.sleep(15)
   	
	conn = mysql.connector.connect(
		user='PonicsMonitor',
		password='raspberry',
		host='xx.xx.xxx.xxx',
		database='aquaponics')

	cursor = conn.cursor()

	TempTankAvg = rollAvg(5)
	TempBedAvg = rollAvg(5)
	TempSumpAvg = rollAvg(5)
	LvlSumpAvg = rollAvg(5)


	try:
		while True:
			TempTank = daq.getADC(0,0)
			TempBed = daq.getADC(0,1)
			TempSump = daq.getADC(0,2)
			AnalogV = daq.getADC(0,8)

			TempTank = CalcTemp(TempTank,AnalogV)
			TempBed = CalcTemp(TempBed,AnalogV)
			TempSump = CalcTemp(TempSump,AnalogV)

			LvlSump = daq.getADC(0,3)
			LvlSump = CalcGallons(LvlSump,AnalogV)
			print (TempTank,TempBed,TempSump,LvlSump)
	
			TempTankAvg.AddVal(TempTank)
			TempBedAvg.AddVal(TempBed)
			TempSumpAvg.AddVal(TempSump)
			LvlSumpAvg.AddVal(LvlSump)


			ts = time.time()
			if ((ts-Time) > 60):
				Time = time.time()
				query = "INSERT INTO Monitor (time,TempTank,TempBed,TempSump,LvlSump) VALUES ('%f','%f','%f','%f','%f')" %(Time,TempTankAvg.GetAvg(),TempBedAvg.GetAvg(),TempSumpAvg.GetAvg(),LvlSumpAvg.GetAvg()) 
				print ( "Commiting to Database")
				try:
					cursor.execute(query)
					conn.commit()
				except:
					try:
						print("Commit Failed")
						print("Attempting to re-connect")
						print("may take up to 30 secs")
						
						conn = mysql.connector.connect(
							user='PonicsMonitor',
							password='raspberry',
							host='xx.xx.xx.xx',
							database='aquaponics')
						cursor = conn.cursor()
						cursor.execute(query)
						conn.commit()
					except:
						print("Reconnect Failed")
						print("Contiue Monitoring")
						

			time.sleep(1)

	except KeyboardInterrupt:
		conn.close()
		sys.exit(0)

if __name__ == "__main__":
	main()
