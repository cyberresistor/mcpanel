import os
from pathlib import Path
import subprocess
import requests

jdk_list = [
    "https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.tar.gz", # jdk 25
    "https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz", # jdk 21
    "https://download.oracle.com/java/17/archive/jdk-17.0.12_linux-x64_bin.tar.gz", # jdk 17
    "https://release-assets.githubusercontent.com/github-production-release-asset/372924428/860c06cc-30fd-4255-831a-1fefe733112f?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-09-14T14%3A12%3A32Z&rscd=attachment%3B+filename%3DOpenJDK8U-jdk_x64_linux_hotspot_8u504b01.tar.gz&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-09-14T13%3A12%3A15Z&ske=2026-09-14T14%3A12%3A32Z&sks=b&skv=2018-11-09&sig=OmCSObDyLjOoxAV4FB0l5Q03W7b7CcAjTa9IbqvWnJo%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc4OTM5NDM2OCwibmJmIjoxNzg5MzkyNTY4LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.2Hx5R6L0DzK05DZvwW3TPHzf2Fs-RAoRgmpA8oF1_3k&response-content-disposition=attachment%3B%20filename%3DOpenJDK8U-jdk_x64_linux_hotspot_8u504b01.tar.gz&response-content-type=application%2Foctet-stream" # temurin jdk 8
]

def download_file(url, output_path):
    print(f"[INFO] Pobieranie do {output_path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"[SUCCESS] Pobrano {output_path}")

def getJava(jdkVersion):
    mapping = {
        25: ("jdk25.tar.gz", 0),
        21: ("jdk21.tar.gz", 1),
        17: ("jdk17.tar.gz", 2),
        8: ("jdk8.tar.gz", 3),
        "1.8.0": ("jdk8.tar.gz", 3)
    }
    
    if jdkVersion in mapping:
        filename, index = mapping[jdkVersion]
        download_file(jdk_list[index], filename)
    else:
        raise ValueError(f"Nieznana wersja JDK: {jdkVersion}")

def unpackJDK():
    jdkNameOutputs = [
        "jdk25.tar.gz",
        "jdk21.tar.gz",
        "jdk17.tar.gz",
        "jdk8.tar.gz"
    ]
    
    target_archive = None
    for archive in jdkNameOutputs:
        if Path(archive).exists():
            target_archive = archive
            break
            
    if target_archive:
        print(f"[INFO] Rozpakowywanie {target_archive}...")
        subprocess.run(["tar", "xpvf", target_archive], check=True)
        print("[SUCCESS] Rozpakowano pomyślnie!")
    else:
        print("Java file doesnt exist... or you just need update it.")