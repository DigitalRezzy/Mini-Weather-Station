import serial
import time

ser = serial.Serial('COM3', 9600)

time.sleep(2)

file = open("data.csv", "w")
file.write("temperature,humidity\n")

print("Logging data...")

while True:
    line = ser.readline().decode().strip()

    try:
        temp, hum = line.split(",")
        file.write(f"{temp},{hum}\n")
        file.flush()
        print(temp, hum)
    except:
        pass