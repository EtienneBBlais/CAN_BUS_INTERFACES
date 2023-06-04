import can

def receive_message(bus):
    message = bus.recv()  # Blocking receive
    if message is not None:
        print(f"Received message: {message}")

def main():
    # Use 'pcan' interface and appropriate channel
    bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000)
    while True:
        receive_message(bus)

if __name__ == "__main__":
    main()
