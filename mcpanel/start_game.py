import os
class ServerLauncherConfig:
    def __init__(self,jvmArgs,executableJar):
        self.jvmArgs = jvmArgs,
        self.executableJar = executableJar,
def startMinecraftServer(config: ServerLauncherConfig):
    print("Launching Your dream server :)")

    os.execvp("java",f"{config.jvmArgs}")
def accept_minecraft_eula(server_dir="."):
    eula_path = os.path.join(server_dir, "eula.txt")
    
    # Text required by Mojang to accept the EULA
    eula_content = (
        "#By changing the setting below to TRUE you are indicating your agreement to our EULA "
        "(https://aka.ms).\n"
        "eula=true\n"
    )
    
    try:
        # Write or overwrite the eula.txt file
        with open(eula_path, "w", encoding="utf-8") as file:
            file.write(eula_content)
        print(f"Successfully accepted Minecraft EULA in: {os.path.abspath(eula_path)}")
    except Exception as e:
        print(f"Error writing eula.txt: {e}")
