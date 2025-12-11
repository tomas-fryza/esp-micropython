# Based on
# https://github.com/bh1rio/micropython-si4703/tree/main

from machine import Pin, I2C
import time


def read_key(timeout=0.1):
    """Non-blocking read from stdin."""
    if select.select([sys.stdin], [], [], timeout)[0]:
        return sys.stdin.read(1)
    return None


def print_commands():
    print("Available commands:")
    print("  u : Seek up (higher frequency)")
    print("  d : Seek down (lower frequency)")
    print("  v : Volume up")
    print("  c : Volume down")
    print("  Ctrl+C : Quit and power down the radio")
    print("  h : Show this help message")
    print()


class Radio:
    REG_DEVICEID =       0x00
    REG_CHIPID =         0x01
    REG_POWERCFG =       0x02
    REG_CHANNEL =        0x03
    REG_SYSCONFIG1 =     0x04
    REG_SYSCONFIG2 =     0x05
    REG_SYSCONFIG3 =     0x06
    REG_TEST1 =          0x07
    REG_TEST2 =          0x08
    REG_BOOTCONFIG =     0x09
    REG_STATUSRSSI =     0x0A
    REG_READCHAN =       0x0B
    REG_RDSA =           0x0C
    REG_RDSB =           0x0D
    REG_RDSC =           0x0E
    REG_RDSD =           0x0F

    SI4703_SMUTE =          15
    SI4703_DMUTE =          14
    SI4703_SKMODE =         10
    SI4703_SEEKUP =         9
    SI4703_SEEK =           8
    SI4703_DISABLE =        6
    SI4703_ENABLE =         0

    SI4703_TUNE =           15

    SI4703_RDSIEN =         15
    SI4703_STCIEN =         14
    SI4703_RDS =            12
    SI4703_DE =             11
    SI4703_AGCD =           10
    SI4703_BLNDADJ =        6
    SI4703_GPIO3 =          4
    SI4703_GPIO2 =          2
    SI4703_GPIO1 =          0

    SI4703_SEEKTH =         8
    SI4703_SPACE1 =         5
    SI4703_SPACE0 =         4
    SI4703_VOLUME_MASK =    0x000F

    SI4703_SKSNR =          4
    SI4703_SKCNT =          0

    SI4703_AHIZEN =         14
    SI4703_XOSCEN =         15

    SI4703_RDSR =           15
    SI4703_STC =            14
    SI4703_SFBL =           13
    SI4703_AFCRL =          12
    SI4703_RDSS =           11
    SI4703_STEREO =         8

    SI4703_READCHAN_MASK =  0x03FF    

    SI4703_GROUPTYPE_OFFST = 11
    SI4703_TP_OFFST =       10
    SI4703_TA_OFFST =       4
    SI4703_MS_OFFST =       3
    SI4703_TYPE0_INDEX_MASK = 0x0003
    SI4703_TYPE2_INDEX_MASK = 0x000F

    SI4703_SEEK_DOWN =      0
    SI4703_SEEK_UP =        1
    
    def __init__(self, i2c, rstPin):
        self.i2c = i2c
        self.address = 0x10
        self.resetPin = rstPin
        
        self.registers = [0] * 16
        self.rds_ps = [0] * 8
        self.rds_rt = [0] * 64
    
    def ReadRegisters(self):
        i2cReadBytes = self.i2c.readfrom(self.address, 32)
        
        regIndex = 0x0A
        for i in range(16):
            self.registers[regIndex] = (i2cReadBytes[i*2] << 8) + i2cReadBytes[(i*2)+1]
            regIndex += 1
            if regIndex == 0x10:
                regIndex = 0
                
    def WriteRegisters(self):
        WriteBuffer = bytearray(12)

        for i in range(6):
            WriteBuffer[i*2], WriteBuffer[i*2+1] = divmod(self.registers[i+2], 0x100)
        
        self.i2c.writeto(self.address, WriteBuffer)

    def Init(self):
        self.resetPin.off()
        time.sleep_ms(100)
        self.resetPin.on()

        self.ReadRegisters()
        self.registers[self.REG_TEST1] |= (1 << self.SI4703_XOSCEN)
        self.WriteRegisters()
        time.sleep(0.5)

        self.ReadRegisters()
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_DMUTE)
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_ENABLE)
        self.registers[self.REG_SYSCONFIG1] |= (1 << self.SI4703_DE)
        self.registers[self.REG_SYSCONFIG2] |= (1 << self.SI4703_SPACE0)
        self.registers[self.REG_SYSCONFIG2] &= 0xFFF0
        self.registers[self.REG_SYSCONFIG2] |= 0x0001
        self.WriteRegisters()
        time.sleep(0.11)

    def ShutDown(self):
        self.ReadRegisters()
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_ENABLE)
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_DISABLE)
        self.WriteRegisters()
        
    def printInfo(self):
        self.ReadRegisters()
        pn, mfgid = divmod(self.registers[self.REG_DEVICEID], 0x1000)
        rev, other = divmod(self.registers[self.REG_CHIPID], 0b10000000000)
        dev, firmware = divmod(other, 0b1000000)
        if pn == 0x1 and mfgid == 0x242:
            print('Silicon Laboratories Si4700/01/02/03')
        print("Chip: ", end="")
        if dev == 0x9: print('Si4703')
        if dev == 0x8: print('Si4701')
        if dev == 0x1: print('Si4702')
        if dev == 0x0: print('Si4700')
        
        version = 'Ver.: '
        if rev == 0x2: version += 'B'
        if rev == 0x3: version += 'C'
        version += str(firmware)
        print(version)
        print()
        
    def SetChannel(self, freq_mhz):
        """
        freq_mhz: desired frequency in MHz, e.g., 88.3
        """
        # Convert MHz to channel number (register value)
        # 87.5 MHz base, 0.1 MHz = 100 kHz spacing
        channel_val = int(round((freq_mhz - 87.5) / 0.1)) & 0x03FF
        self.ReadRegisters()
        self.registers[self.REG_CHANNEL] &= 0xFE00  # Clear bits [9:0]
        self.registers[self.REG_CHANNEL] |= channel_val
        self.registers[self.REG_CHANNEL] |= (1 << self.SI4703_TUNE)
        self.WriteRegisters()

        # Wait for tuning complete
        while True:
            self.ReadRegisters()
            if (self.registers[self.REG_STATUSRSSI] & (1 << self.SI4703_STC)) != 0:
                break

        self.ReadRegisters()
        self.registers[self.REG_CHANNEL] &= ~(1 << self.SI4703_TUNE)
        self.WriteRegisters()

    def GetChannel(self):
        """
        Return tuned frequency in MHz as float
        """
        self.ReadRegisters()
        channel_val = self.registers[self.REG_READCHAN] & self.SI4703_READCHAN_MASK
        freq_mhz = 87.5 + channel_val * 0.1  # 100 kHz spacing
        return round(freq_mhz, 1)

    def SetVolume(self, volume):
        self.ReadRegisters()
        volume = max(0, min(volume, 15))
        self.registers[self.REG_SYSCONFIG2] &= 0xFFF0
        self.registers[self.REG_SYSCONFIG2] |= volume
        self.WriteRegisters()
        
    def SeekUp(self):
        self.Seek(self.SI4703_SEEK_UP)
        
    def SeekDown(self):
        self.Seek(self.SI4703_SEEK_DOWN)
    
    def Seek(self, seekDirection):
        self.ReadRegisters()
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_SKMODE)
        if seekDirection == self.SI4703_SEEK_DOWN:
            self.registers[self.REG_POWERCFG] &= ~(1 << self.SI4703_SEEKUP)
        else:
            self.registers[self.REG_POWERCFG] |= 1 << self.SI4703_SEEKUP
        self.registers[self.REG_POWERCFG] |= (1 << self.SI4703_SEEK)
        self.WriteRegisters()

        while True:
            self.ReadRegisters()
            if (self.registers[self.REG_STATUSRSSI] & (1 << self.SI4703_STC)) != 0:
                break
        self.ReadRegisters()
        self.registers[self.REG_POWERCFG] &= ~(1 << self.SI4703_SEEK)
        self.WriteRegisters()

    def GetStatus(self):
        """
        Reads basic status information from the Si4703 FM chip.

        Returns a dictionary:
            freq   : tuned frequency in MHz (float)
            rssi   : signal strength (0-255)
            stereo : True if stereo, False otherwise
            volume : current volume level (0-15)
        """
        self.ReadRegisters()
        regs = self.registers

        freq_mhz = ((regs[self.REG_READCHAN] & self.SI4703_READCHAN_MASK) * 0.1) + 87.5
        rssi = regs[self.REG_STATUSRSSI] & 0xFF
        stereo = bool((regs[self.REG_STATUSRSSI] >> self.SI4703_STEREO) & 1)
        volume = regs[self.REG_SYSCONFIG2] & self.SI4703_VOLUME_MASK

        return {
            "freq": round(freq_mhz, 1),
            "rssi": rssi,
            "stereo": stereo,
            "volume": volume
        }


if __name__ == "__main__":
    SDIO_PIN = 21
    SCL_PIN = 22
    RESET_PIN = 12

    i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDIO_PIN), freq=100_000)
    radio = Radio(i2c, Pin(RESET_PIN, Pin.OUT))

    radio.Init()
    radio.printInfo()

    radio.SetVolume(3)
    radio.SetChannel(88.3)

    print_commands()

    try:
        while True:
            status = radio.GetStatus()
            print(f"Freq: {status['freq']} MHz | RSSI: {status['rssi']} | Stereo: {status['stereo']} | Volume: {status['volume']}")

            cmd = input("Command: ").strip().lower()  # Waits for user input

            if cmd == 'u':
                radio.SeekUp()
                print("Seeked up →", radio.GetChannel(), "MHz")
            elif cmd == 'd':
                radio.SeekDown()
                print("Seeked down ←", radio.GetChannel(), "MHz")
            elif cmd == 'v':
                new_vol = min(current_volume + 1, 15)
                radio.SetVolume(new_vol)
                print("Volume increased →", radio.GetVolume())
            elif cmd == 'c':
                new_vol = max(current_volume - 1, 0)
                radio.SetVolume(new_vol)
                print("Volume decreased →", radio.GetVolume())
            elif cmd == 'h':
                print_commands()
            else:
                print("Unknown command.")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nShutting down...")
        radio.ShutDown()
        print("Radio powered down safely.")
