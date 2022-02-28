import time
import RT_IB
import random
import datetime
from os.path import exists

## Config
# Prefix for datafile names
data_file_prefix = "data/data"

# Com port number (like 4 in COM4 on Windows, /dev/ttyACM4 on linux)
comport = 7

# Number of seconds between data records
record_data_every = 15

ib = RT_IB.Create()
ib.ComOpen(comport)

def get_turbine_wattage_le600(wind_speed_ms):
    # figures are from published power curve
    v = wind_speed_ms - 0.3
    if v < 3: return 0
    if v < 4: return 30
    if v < 5: return 60
    if v < 6: return 105
    if v < 7: return 160
    if v < 8: return 215
    if v < 9: return 300
    if v < 10: return 400
    if v < 11: return 500
    if v < 12: return 600
    if v < 13: return 650
    if v < 14: return 700
    if v < 15: return 725
    if v < 16: return 730
    if v < 18: return 750
    return 0

def get_turbine_wattage_airforce1(wind_speed_ms):
    if wind_speed_ms < 3.5: return 0 # cut in speed = 3.5m/s
    efficiency = 34.6
    blade_length = 0.9
    return get_turbine_wattage_generic(wind_speed_ms, efficiency, blade_length)

def get_turbine_wattage_generic(wind_speed_ms, efficiency, blade_length):
    # Constants
    pi = 3.14159         # pi is approx 3 
    air_density = 1.224 # kg/m3 - assumed typical default

    # Power = 0.5 * air_density * wind_speed_ms^3 * swept_area * efficiency%
    swept_area = pi * blade_length * blade_length  #area of circle = pi*r^2
    wind_power_avail = 0.5 * air_density * pow(wind_speed_ms, 3) * swept_area 
    wind_power_actual = wind_power_avail * (efficiency/100)
    return int(round(wind_power_actual, 0))

def getDataFileName():
    global fileNum
    # File num not yet set so find first unused filename
    if fileNum < 0:
        fileNum = 0
        while exists(f"{data_file_prefix}{fileNum}.csv"):
            fileNum += 1
        return f"{data_file_prefix}{fileNum}.csv"
    else:
        return f"{data_file_prefix}{fileNum}.csv"

fileNum = 0
samples = 0
sum_wind_speed_ms = 0
sum_wattage_le600 = 0
sum_wattage_airforce1 = 0

while True:
    AdcSample = ib.ADCSample10(0)

    # AdcSample is a 10-bit value 0..1023
    voltage = (AdcSample/1023) * 5

    # Voltage ranges from 0 (0m/s wind) to 5 (30m/s wind)
    wind_speed_ms = round(voltage * 6, 1)
    wind_speed_mph = round(wind_speed_ms * 2.24, 1)

    wattage_le600 = get_turbine_wattage_le600(wind_speed_ms)
    wattage_airforce1 = get_turbine_wattage_airforce1(wind_speed_ms)

    print(f"Wind speed: {wind_speed_ms} m/s {wind_speed_mph} mph {wattage_le600}w {wattage_airforce1}w")

    samples += 1
    sum_wind_speed_ms += wind_speed_ms
    sum_wattage_le600 += wattage_le600
    sum_wattage_airforce1 += wattage_airforce1

    if samples == record_data_every:
        timestamp = datetime.datetime.now()
        average_wind_speed_ms = round(sum_wind_speed_ms/samples, 1)
        average_wind_speed_mph = round(average_wind_speed_ms*2.24, 1)
        average_wattage_le600 = int(round(sum_wattage_le600/samples, 0))
        average_wattage_airforce1 = int(round(sum_wattage_airforce1/samples, 0))

        data_line = f"{timestamp},{average_wind_speed_ms},{average_wind_speed_mph},{average_wattage_le600},{average_wattage_airforce1}"

        f = open(getDataFileName(), "a")
        f.write("{data_line}\n")
        f.close()

        print(f"Wrote to {getDataFileName()}: {data_line}")

        samples = 0
        sum_wind_speed_ms = 0
        sum_wattage_le600 = 0
        sum_wattage_airforce1 = 0

    time.sleep(1)

#ib.ComClose()



    
