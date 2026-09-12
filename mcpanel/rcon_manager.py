from mcrcon import MCRcon
class ServerRCONConfig:
    def __init__(self,ip,port,command,password):
        self.ip = ip
        self.port = port
        self.command = command
        self.password = password
class ServerRCON:
    def sendCommand(config: ServerRCONConfig):
        mcr = MCRcon(config.ip,config.password,config.port)
        mcr.connect()
        mcr.command(config.command)
        print("[SUCCESS] command sended!")
        mcr.disconnect()
        