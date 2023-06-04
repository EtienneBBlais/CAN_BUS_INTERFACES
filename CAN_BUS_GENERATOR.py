import can
import time

# Initialize bus
bus = can.interface.Bus(bustype='virtual', channel='vcan0')

# Messages identifiers for each device
message_identifiers = {
    "BMS1": list(range(1040, 1046)),
    "BMS2": list(range(1056, 1062)),
    "BMS3": list(range(1072, 1078))
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

for device, identifiers in message_identifiers.items():
    for identifier in identifiers:
        # Initialize data array
        data = [0] * 8

        for signal, start_bit in signals.items():
            # Insert signal into data array
            raw_value = 1  # Raw signal value
            data[start_bit:start_bit+2] = [(raw_value >> 8) & 0xFF, raw_value & 0xFF]

        # Create message
        msg = can.Message(arbitration_id=identifier, data=data, is_extended_id=False)

        # Print message
        print(f"Sending message: {msg}")

        # Send message
        bus.send(msg)

        # Wait for one second
        time.sleep(1)
