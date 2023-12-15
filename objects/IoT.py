import util


class IoT:
    def __init__(self, id: int, x: float, y: float, data_generated: float, delay_budget: float, CPU_needed: int, power=0.2):
        self.id = id
        self.x = x
        self.y = y
        self.data_generated = data_generated
        self.delay_budget = delay_budget
        self.CPU_needed = CPU_needed
        self.power = power # in watts

    def __str__(self):
        return "IoT[{}], data_generated: {}, x: {}, y: {}, delay_budget: {}, CPU_needed: {}"\
            .format(self.id, self.data_generated, self.x, self.y, self.delay_budget, self.CPU_needed)

    def get_rate(self, BS, bandwidth):
        distance = util.distance_2d(BS.x, BS.y, self.x, self.y)
        snr = util.snr(distance, bandwidth, self.power, BS.frequency)
        channel_rate = util.shannon_capacity(snr, bandwidth)
        return channel_rate

def read_from_IoT_file(fname): # return list of IoT devices
    # read the IoT properties from the file into list of IoT devices
    # format of the file: id    x   y   data_generated Mbps  delay_budget ms   CPU_needed Kcycles
    #
    IoT_devices =[]
    iot_file = open(fname, "r")
    iot_file.readline()  # skip the column names
    total_CPU_needed = 0
    with open(fname, 'r') as fp:
        fp.readline()
        for line in fp:
            #print(line)
            [id, x, y, data_generated, delay_budget, CPU_needed] = line.split()
            total_CPU_needed = total_CPU_needed + int(CPU_needed)
            IoT_devices.append(IoT(id, float(x), float(y), int(data_generated), int(delay_budget), int(CPU_needed)))

    print("%d IoT device information read from file:%s" % (int(id), fname))
    print("Total CPU needed: %d cycles" % total_CPU_needed)

    return IoT_devices



