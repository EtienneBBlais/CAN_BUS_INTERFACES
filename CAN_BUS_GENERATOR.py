# Auteur: Étienne Bellerive-Blais
# Date de création: 2023-06-11
# Nom du fichier: CAN_BUS_GENERATOR.py
# Description:
#

import can
import time
import importationBMSLOG1
# Initialize bus
bus = can.interface.Bus(bustype='virtual', channel='vcan0')

# Messages identifiers for each device
message_identifiers = {
    "BMS1": list(range(0x410, 0x418)),
    "BMS2": list(range(0x420, 0x428)),
    "BMS3": list(range(0x430, 0x438)),
    "BMS4": list(range(0x440, 0x448)),
    "BMS5": list(range(0x450, 0x458))
}

# Signals for each message
signals = {
    "V00": 0,
    "V01": 1,
    "V02": 2,
    "V03": 3,
    "V04": 4,
    "V05": 5,
    "V06": 6,
    "V07": 7
}
# Your data as a string


# Convert your data to a list of integers
iterator = 0

while 1:
    start_time = time.perf_counter()
    if(iterator > 1000):
        iterator = 0

    for device, identifiers in message_identifiers.items():
        for identifier in identifiers:







                # Create message
            msg = can.Message(arbitration_id=identifier, data=importationBMSLOG1.data[iterator], is_extended_id=False)
            iterator += 1

            # Print message
            print(f"Sending message: {msg}")

            # Send message
            bus.send(msg)

    end_time = time.perf_counter()  # Get end time
    execution_time = end_time - start_time  # Calculate execution time

    if execution_time < 10:
        time.sleep(1 - execution_time)  # Sleep for the remaining time
