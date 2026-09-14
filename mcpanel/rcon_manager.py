from mcrcon import MCRcon
# yandere code quality :0

class ServerRCONConfig:
    def __init__(self, ip, port, command, password):
        self.ip = ip
        self.port = port
        self.command = command
        self.password = password

class ServerRCON:
    @staticmethod
    def sendCommand(config: ServerRCONConfig):
        try:
            with MCRcon(config.ip, config.password, config.port) as mcr:
                response = mcr.command(config.command)
                print(f"[SUCCESS] Command sent! Response: {response}")
                return response
        except Exception as e:
            print(f"[ERROR] RCON connection failed: {e}")
            raise