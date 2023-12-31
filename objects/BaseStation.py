import random

import util
from objects import Params


class BaseStation:
    def __init__(self, id, bandwidth, power, x, y, frequency, maxCost, weights):
        self.id = id
        self.y = float(y)
        self.x = float(x)
        self.power = power
        self.bandwidth = bandwidth
        self.frequency = frequency
        self.weights = weights
        self.maxCost = maxCost
        self.fulfilmentrate = []
        self.overhead = []
        self.possible_cloud = True
        self.possible_edge = True
        print("BS is generated")

    def allocateResources(self, edgeComputeResources, cloudComputeResources, IoTnodes, scheme="ONLY_EDGE"):
        # This is the function you need to implement your decision approach
        # To give you some idea, three very simple decision logic are implemented: only-edge, only-cloud, and random
        n_nodes = len(IoTnodes)
        decision = []
        overhead_rate = []
        counter_fulfilled_budget = 0

        remainingEdgeCapacity = edgeComputeResources.CPU_cycles
        remainingCloudCapacity = cloudComputeResources.CPU_cycles

        if scheme == "ONLY_EDGE":
            for IoT in IoTnodes:

                # Calculating delay budget fulfillment rate
                total_budget_edge = Params.Edge_BS_delay + util.calculate_computationTime(IoT.CPU_needed,
                                                                                          Params.Edge_CPU_cycles)

                if (total_budget_edge <= IoT.delay_budget):
                    counter_fulfilled_budget += 1
                else:
                    overhead_rate.append(total_budget_edge/IoT.delay_budget)


                uplink_bandwidth = self.bandwidth / n_nodes  # equally allocate the uplink bandwidth among IoT devices
                run_on_edge = 1  # since this is EDGE allocation, set this to true
                run_on_cloud = 0
                compute_allocated = edgeComputeResources.CPU_cycles / n_nodes  # JUST allocate resources equally among IoT devices
                if compute_allocated > IoT.CPU_needed:  # if allocated resource is larger than needed, set allocation to what is needed
                    compute_allocated = IoT.CPU_needed


                resources_allocated = Allocation()
                resources_allocated.set_values(run_on_edge, run_on_cloud, uplink_bandwidth, compute_allocated)
                decision.append(resources_allocated)

        elif scheme == "ONLY_CLOUD":
            for IoT in IoTnodes:

                total_budget_cloud = Params.Cloud_BS_delay + util.calculate_computationTime(IoT.CPU_needed,
                                                                                            Params.Cloud_CPU_cycles)

                if (total_budget_cloud <= IoT.delay_budget):
                    counter_fulfilled_budget += 1
                else:
                    overhead_rate.append(total_budget_cloud / IoT.delay_budget)

                uplink_bandwidth = self.bandwidth / n_nodes
                run_on_edge = 0
                run_on_cloud = 1
                compute_allocated = cloudComputeResources.CPU_cycles / n_nodes
                if compute_allocated > IoT.CPU_needed:  # if allocated resource is larger than needed, set allocation to what is needed
                    compute_allocated = IoT.CPU_needed

                resources_allocated = Allocation()
                resources_allocated.set_values(run_on_edge, run_on_cloud, uplink_bandwidth, compute_allocated)
                decision.append(resources_allocated)

        elif scheme == "CUSTOM":
            for IoT in IoTnodes:

                # First step filter out unreasonable devices based on delay time

                total_cloud_time = IoT.data_generated/IoT.get_rate(self,self.bandwidth) + Params.Cloud_BS_delay + util.calculate_computationTime(IoT.CPU_needed,
                                                                                                                                                 Params.Cloud_CPU_cycles)

                if (total_cloud_time > IoT.delay_budget):

                    self.possible_cloud = False

                total_edge_time = IoT.data_generated/IoT.get_rate(self,self.bandwidth) + Params.Edge_BS_delay + util.calculate_computationTime(IoT.CPU_needed,
                                                                                                                                           Params.Edge_CPU_cycles)

                if(total_edge_time > IoT.delay_budget):

                    self.possible_edge = False

                    if(self.possible_cloud == False):
                        overhead_rate.append(total_edge_time / IoT.delay_budget)
                        print(
                            "IOT device " + IoT.id + " is dropped as it cannot fulfill the delay budget with an overhead of " + total_edge_time / IoT.delay_budget)

                        continue


                # Second step deciding on bandwidth allocation




                # Modifying the computation allocation to match the needed computation power

                if compute_allocated > IoT.CPU_needed:  # if allocated resource is larger than needed, set allocation to what is needed
                    compute_allocated = IoT.CPU_needed

                # Distribution of bandwidth
                ratioConstant = self.bandwidth/self.maxCost
                cost = IoT.get_cost(self.weights)
                uplink_bandwidth = ratioConstant * cost

                # uplink_bandwidth2 = self.bandwidth / n_nodes



                # Executing the resource allocation process

                resources_allocated = Allocation()
                resources_allocated.set_values(run_on_edge, run_on_cloud, uplink_bandwidth, compute_allocated)
                decision.append(resources_allocated)

                # Resetting all used variables

                self.possible_cloud = True

        else:
            for IoT in IoTnodes:
                uplink_bandwidth = self.bandwidth / n_nodes
                trow_a_dice = random.random()
                if trow_a_dice >= 0.5:
                    run_on_edge = 0
                    run_on_cloud = 1
                    compute_allocated = int(remainingCloudCapacity * trow_a_dice)

                    total_budget_cloud = Params.Cloud_BS_delay + util.calculate_computationTime(IoT.CPU_needed, Params.Cloud_CPU_cycles)
                    if (total_budget_cloud <= IoT.delay_budget):
                        counter_fulfilled_budget += 1
                    else:
                        overhead_rate.append(total_budget_cloud / IoT.delay_budget)


                    if compute_allocated > IoT.CPU_needed:  # if allocated resource is larger than needed, set allocation to what is needed
                        compute_allocated = IoT.CPU_needed
                    remainingCloudCapacity = remainingCloudCapacity - compute_allocated
                else:
                    run_on_edge = 1
                    run_on_cloud = 0
                    compute_allocated = int(remainingEdgeCapacity*trow_a_dice)

                    total_budget_edge = Params.Edge_BS_delay + util.calculate_computationTime(IoT.CPU_needed,Params.Edge_CPU_cycles)
                    if (total_budget_edge <= IoT.delay_budget):
                        counter_fulfilled_budget += 1
                    else:
                        overhead_rate.append(total_budget_edge / IoT.delay_budget)

                    if compute_allocated > IoT.CPU_needed:  # if allocated resource is larger than needed, set allocation to what is needed
                        compute_allocated = IoT.CPU_needed
                    remainingEdgeCapacity = remainingEdgeCapacity - compute_allocated


                resources_allocated = Allocation()
                resources_allocated.set_values(run_on_edge, run_on_cloud, uplink_bandwidth, compute_allocated)
                decision.append(resources_allocated)
        self.overhead.append(util.average(overhead_rate))
        self.fulfilmentrate.append(counter_fulfilled_budget/n_nodes)
        return decision

def check_if_feasible(self, allocation, edgeComputeCapacity, cloudComputeCapacity):
    sum_bw = 0
    sum_edge_compute = 0
    sum_cloud_compute = 0

    for a in allocation:
        sum_bw = sum_bw + a.uplink_bandwidth
        sum_edge_compute = sum_edge_compute + a.run_on_edge * a.compute_allocated
        sum_cloud_compute = sum_cloud_compute + (1 - a.run_on_edge) * a.compute_allocated

    utilization_uplink = 1.0 * sum_bw / self.bandwidth
    utilization_edge = 1.0 * sum_edge_compute / edgeComputeCapacity
    utilization_cloud = 1.0 * sum_cloud_compute / cloudComputeCapacity

    if utilization_uplink <= 1.0:
        if utilization_edge <= 1.0:
            if utilization_cloud <= 1.0:
                return True, utilization_uplink, utilization_edge, utilization_cloud
    return False, utilization_uplink, utilization_edge, utilization_cloud


class Allocation:
    def __init__(self):
        self.run_on_edge = - 0
        self.run_on_cloud = 0
        self.uplink_bandwidth = 0
        self.compute_allocated = 0

    def set_values(self, run_on_edge, run_on_cloud, uplink_bandwidth, compute_allocated):
        self.run_on_edge = run_on_edge
        self.run_on_cloud = run_on_cloud
        self.uplink_bandwidth = uplink_bandwidth
        self.compute_allocated = compute_allocated
