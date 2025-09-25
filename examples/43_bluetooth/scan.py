import bluetooth
import time

devices = {}


def bt_irq(event, data):
    if event in (5, 6):
        print(".", end="")
    else:
        print("BLE event code:", event)

    if event == 5:  # _IRQ_SCAN_RESULT
        addr_type, addr, adv_type, rssi, adv_data = data
        addr_str = ':'.join('{:02x}'.format(b) for b in addr)

        if addr_str not in devices:
            devices[addr_str] = {
                'addr_type': addr_type,
                'adv_type': adv_type,
                'rssi': rssi,
                'adv_data': adv_data,
                'count': 1
            }
        else:
            # Update RSSI if stronger signal seen
            if rssi > devices[addr_str]['rssi']:
                devices[addr_str]['rssi'] = rssi
                devices[addr_str]['adv_data'] = adv_data
                devices[addr_str]['adv_type'] = adv_type
                devices[addr_str]['addr_type'] = addr_type
            # Increment count every time we see this device
            devices[addr_str]['count'] += 1

    elif event == 6:  # _IRQ_SCAN_DONE
        print(" Done")
        # Sort devices by RSSI (strongest first)
        sorted_devs = sorted(devices.items(), key=lambda item: item[1]['rssi'], reverse=True)

        if not sorted_devs:
            print("No devices found")
            return

        print(f"{'\n RSSI':>5} | {'Count':>5} | {'Address':<17} | {'Name':<10} | {'AdvType':<8} | {'AddrType'}")
        print("-" * 70)

        for addr_str, d in sorted_devs:
            try:
                name = bluetooth.decode_name(d['adv_data']) or "N/A"
            except:
                name = "N/A"

            print(f"{d['rssi']:>5} | {d['count']:>5} | {addr_str:<17} | {name:<10} | {d['adv_type']:<8} | {d['addr_type']}")


def start_scan(duration=2_000):
    ble = bluetooth.BLE()
    ble.active(True)
    ble.irq(bt_irq)
               # Duration, interval, window (in ms)
    ble.gap_scan(duration, 1_280, 1_280)

    print(f"Scanning for {duration/1000:.1f} seconds", end="")
    time.sleep(duration / 1000 + 1)

    # Turn off BLE after scan is done
    ble.active(False)


def print_legend():
    print("\nLegend:")
    print("  AdvType (Advertising Type):")
    print("    0 = Connectable undirected")
    print("    1 = Connectable directed")
    print("    2 = Scannable undirected")
    print("    3 = Non-connectable undirected")
    print("    4 = Scan response")
    print("\n  AddrType (Address Type):")
    print("    0 = Public address")
    print("    1 = Random address")
    print("\n  BLE Event Codes:")
    print("    1  = Central connected to this device (Peripheral mode)")
    print("    2  = Central disconnected")
    print("    3  = GATT write request (central wrote to a characteristic)")
    print("    5  = Scan result (advertising report found)")
    print("    6  = Scan complete")
    print("    7  = Connected to peripheral (Central mode)")
    print("    8  = Disconnected from peripheral")
    print("    9  = Service discovered")
    print("   10  = Characteristic discovered")
    print("   11  = Descriptor discovered")
    print("   12  = Characteristic read result")
    print("   14  = Characteristic write complete")
    print("   15  = Notification received")
    print("   16  = Indication received")

start_scan()
# print_legend()
