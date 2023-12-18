import util
from objects import Params, BaseStation, IoT, ComputeNode
import numpy as np

# Read the parameters from Params.py  file for the Base Station
bandwidth = Params.BS_bandwidth
power = Params.BS_power
[x, y] = Params.BS_location
frequency = Params.frequency


# Generate the BS
BS = BaseStation.BaseStation(1, bandwidth, power, x, y, frequency)

# Generate IoT devices, read from input_files folder the IoT device properties
n_IoT_devices = Params.n_IoT_devices
IoT_devices = IoT.read_from_IoT_file(Params.input_folder + "/IoT_" + str(n_IoT_devices)+ "_devices.txt")

# Generate Edge and Cloud compute nodes according to the parameters in the Params.py file
edgeComputeNode = ComputeNode.ComputeNode("Edge", Params.Edge_CPU_cycles, 0)
cloudComputeNode = ComputeNode.ComputeNode("Cloud", Params.Cloud_CPU_cycles, Params.Cloud_BS_delay)



# Run your BS decision algorithm considering edge, cloud, and IoT properties
schemes = ["ONLY_EDGE", "ONLY_CLOUD", "RANDOM", "CUSTOM"] # NAME YOUR ALGORITHM AND ADD IT HERE

stats = np.zeros((4, len(schemes))) # 4 for 4 statistics
for a, allocation_scheme in enumerate(schemes):
    allocation = BS.allocateResources(edgeComputeNode, cloudComputeNode, IoT_devices, allocation_scheme)

    # Check if the algorithm's decision is a feasible one (resource limits are not violated)
    # Report the resource utilization: uplink bandwidth, edge and cloud usage
    is_feasible, utilization_uplink, utilization_edge, utilization_cloud = BS.check_if_feasible(allocation, edgeComputeNode.CPU_cycles, cloudComputeNode.CPU_cycles)
    if is_feasible:
        print("\nGreat! This is a feasible allocation of resources.\n")
    else:
        print("There seems to be more capacity allocated than the available capacity!")

    print("Utilization of Uplink:%.2f \nEdge-Utilization:%.2f \nCloud-Utilization:%.2f" %  (utilization_uplink, utilization_edge, utilization_cloud))
    stats[:, a] = [is_feasible, utilization_uplink, utilization_edge, utilization_cloud]


# plot statistics
# WHAT OTHER STATISTICS can you plot showing the goodness of your solution? You can add new statistics and plots here.
util.plot_bars(np.arange(len(schemes)), stats[1, :], "output_files/uplink_utilization", xlab="Allocation Schemes", ylab="Uplink Bandwidth Utilization", xlabels=schemes,
              labels=schemes)
util.plot_bars(np.arange(len(schemes)), stats[2, :],"output_files/edge_utilization", xlab="Allocation Schemes", ylab="Edge Compute Utilization", xlabels=schemes,
              labels=schemes)
util.plot_bars(np.arange(len(schemes)), stats[3, :], "output_files/cloud_utilization", xlab="Allocation Schemes", ylab="Cloud Compute Utilization", xlabels=schemes,
              labels=schemes)


util.plot_bars(np.arange(len(schemes)), BS.fulfilmentrate, "output_files/delay_budget_fulfilment_rate", xlab="Allocation Schemes", ylab="Delay budget fulfilment rate", xlabels=schemes,
              labels=schemes)

util.plot_bars(np.arange(len(schemes)), BS.overhead, "output_files/delay_overhead", xlab="Allocation Schemes", ylab="Delay overhead", xlabels=schemes,
              labels=schemes)