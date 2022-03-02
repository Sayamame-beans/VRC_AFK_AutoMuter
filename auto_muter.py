import argparse
import threading
import time
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher

class AutoMuter:
    VERSION = "0.1.0"
    DEFAULT_OSC_TX_IP = "127.0.0.1"
    DEFAULT_OSC_TX_PORT = 9000
    DEFAULT_OSC_RX_IP = "127.0.0.1"
    DEFAULT_OSC_RX_PORT = 9001

    def __init__(self, tx_ip:str, tx_port:int, rx_ip:str, rx_port:int) -> None:
        self._event = threading.Event()
        self._event.set()

        self.tx_ip = tx_ip if tx_ip else self.DEFAULT_OSC_TX_IP
        self.tx_port = tx_port if tx_port else self.DEFAULT_OSC_TX_PORT
        self.rx_ip = rx_ip if rx_ip else self.DEFAULT_OSC_RX_IP
        self.rx_port = rx_port if rx_port else self.DEFAULT_OSC_RX_PORT
        self.last_afk = False
        self.last_muteself = False
        self.first_mute = True

        #OSC Client Initialization
        self.client = udp_client.SimpleUDPClient(self.tx_ip, self.tx_port)

        #OSC Server Initialization
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/avatar/parameters/AFK", self.update_afk)
        self.dispatcher.map("/avatar/parameters/MuteSelf", self.update_muteself)
        self.server = osc_server.BlockingOSCUDPServer((self.rx_ip, self.rx_port), self.dispatcher)

    def run(self) -> None:
        self.server.serve_forever()

    def update_afk(self, path: str, value: bool) -> None:
        self.last_afk = value
        if value:
            thread = threading.Thread(target=self.mute)
            thread.setDaemon(True)
            thread.start()

    def update_muteself(self, path: str, value: bool) -> None:
        self.last_muteself = value
        if(self.first_mute):
            if(self.last_afk and not value):
                self.update_afk("/avatar/parameters/AFK", True)
            self.first_mute = False

# Q: Why does time.sleep(1) exist?
# A: Because of the input lag of VRChat.
#    If you know the FPS value that basically never falls in your environment, you can reduce the wait time.
    def mute(self) -> None:
        if not self._event.is_set:
            self._event.wait()
        self._event.clear()
        if not self.last_muteself:
            self.client.send_message("/input/Voice", 0)
            time.sleep(1)
            self.client.send_message("/input/Voice", 1)
            time.sleep(1)
            self.client.send_message("/input/Voice", 0)
        self._event.set()

if __name__ == "__main__":
    print(f"VRC AFK AutoMuter v{AutoMuter.VERSION}")
    print("Created by Sayamame(https://github.com/Sayamame-beans)")

    parser = argparse.ArgumentParser(description="This is an OSC tool that automatically mutes when AFK in VRChat.")
    parser.add_argument("--tx_ip", type=str, help="Destination IP address. (Default: \"127.0.0.1\")")
    parser.add_argument("--tx_port", type=int, help="Destination Port. (Default: 9000)")
    parser.add_argument("--rx_ip", type=str, help="Source IP address. (Default: \"127.0.0.1\")")
    parser.add_argument("--rx_port", type=int, help="Source IP address. (Default: 9001)")

    args = parser.parse_args()
    if(not any((args.tx_ip, args.tx_port, args.rx_ip, args.rx_port))):
        print("Run with the default settings. (See \"-h\" option for available options.)")

    automuter = AutoMuter(args.tx_ip, args.tx_port, args.rx_ip, args.rx_port)
    print(f"Send to \"{automuter.tx_ip}:{automuter.tx_port}\", Receive at \"{automuter.rx_ip}:{automuter.rx_port}\"")
    try:
        automuter.run()
    except KeyboardInterrupt:
        print("Shutdown VRC AFK AutoMuter.")