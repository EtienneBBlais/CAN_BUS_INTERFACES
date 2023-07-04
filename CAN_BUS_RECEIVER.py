import can

# Message identifiers
bms_id = [
    list(range(0x400, 0x40F)),
    list(range(0x410, 0x41F)),
    list(range(0x420, 0x42F)),
    list(range(0x430, 0x43F)),
    list(range(0x440, 0x44F)),
    list(range(0x450, 0x45F)),
    list(range(0x460, 0x46F))
]

# Cells correspondance
cells = {
    0 : list(range(0, 4)),
    1 : list(range(4, 8)),
    2 : list(range(8, 12)),
    3 : list(range(12, 16)),
    4 : list(range(16, 20)),
    5 : list(range(20, 24))
}

# Cell voltage
voltages = [([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24)]

def parse_message(bms, cells_id, data):
    data = list(data)
    voltage = [
        ((data[1] << 8) + data[0]),
        ((data[3] << 8) + data[2]),
        ((data[5] << 8) + data[4]),
        ((data[7] << 8) + data[6])
    ]
    cells_message = cells.get(cells_id)
    j = 0
    for i in cells_message:
        voltages[4][i] = voltage[j]
        j += 1
    print(voltages)

def receive_message(bus):
    message = bus.recv()  # Blocking receive
    if message is not None:
        bms = (message.arbitration_id & 0x0F0) >> 4
        cells_id = (message.arbitration_id) & 0x00F
        if ((cells_id < 6) and (bms in range(0, 7))):
            parse_message(bms, cells_id, message.data)



def main():
    # Use 'pcan' interface and appropriate channel
    bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000)
    while True:
        receive_message(bus)

def InitierCAN():
    # Use 'pcan' interface and appropriate channel
    bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000)
    while True:
        receive_message(bus)

def get_can_id(bms_index, cell_index):
    cell_id = cell_index % 4  # Get the id of the cell within the message
    msg_id = cell_index // 4  # Get the id of the message within the BMS
    can_id = bms_id[bms_index][msg_id]
    return can_id



if __name__ == "__main__":
    main()
