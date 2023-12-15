import numpy as np
import util as util

# to calculate the noise power
BOLTZMANN = 1.38e-23
TEMPERATURE = 283.15

## B BS properties
BS_bandwidth = 1e7  # Hz
BS_power = 20 # Wattsm
BS_location = [100, 100]
frequency = 3e9

IoT_power = 0.2 # read the BS properties from a file

BASE_CPU_cycles = 50000 # operations per sec also called processing capacity F
Cloud_CPU_cycles = BASE_CPU_cycles*10
Edge_CPU_cycles = BASE_CPU_cycles

Edge_BS_delay = 0
Cloud_BS_delay = 10 #s

n_IoT_devices = 10 # 5 # input_files/IoT_5_devices.txt
input_folder = "input_files"






