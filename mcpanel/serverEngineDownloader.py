import os
import requests
# yandere code quality :0


def download_paper(version: str, output_dir: str = "."):
    """Pobiera najnowszy build silnika Paper dla wskazanej wersji Minecrafta."""
    base_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"

    # 1. Pobierz listę buildów
    resp = requests.get(base_url)
    if resp.status_code != 200:
        print(f"Nie znaleziono wersji Paper {version}")
        return None

    builds = resp.json().get("builds", [])
    if not builds:
        print(f"Brak dostępnych buildów dla Paper {version}")
        return None

    latest_build = builds[-1]
    file_name = f"paper-{version}-{latest_build}.jar"
    download_url = (
        f"{base_url}/builds/{latest_build}/downloads/{file_name}"
    )

    return _download_jar(download_url, output_dir, "server.jar")


def download_purpur(version: str, output_dir: str = "."):
    """Pobiera najnowszy build silnika Purpur dla wskazanej wersji Minecrafta."""
    base_url = f"https://api.purpurmc.org/v2/purpur/{version}"

    resp = requests.get(base_url)
    if resp.status_code != 200:
        print(f"Nie znaleziono wersji Purpur {version}")
        return None

    data = resp.json()
    latest_build = data.get("builds", {}).get("latest")
    if not latest_build:
        print(f"Brak buildów dla Purpur {version}")
        return None

    download_url = f"https://api.purpurmc.org/v2/purpur/{version}/{latest_build}/download"

    return _download_jar(download_url, output_dir, "server.jar")


def download_vanilla(version: str, output_dir: str = "."):
    """Pobiera czysty silnik Vanilla Minecraft z oficjalnego manifestu Mojang."""
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = requests.get(manifest_url).json()

    version_url = None
    for v in manifest["versions"]:
        if v["id"] == version:
            version_url = v["url"]
            break

    if not version_url:
        print(f"Nie znaleziono wersji Vanilla {version}")
        return None

    version_data = requests.get(version_url).json()
    server_download = (
        version_data.get("downloads", {}).get("server", {}).get("url")
    )

    if not server_download:
        print(f"Brak linku do pobrania serwera dla wersji {version}")
        return None

    return _download_jar(server_download, output_dir, "server.jar")


def _download_jar(url: str, output_dir: str, filename: str):
    """Funkcja pomocnicza do pobierania plików .jar ze streamowaniem."""
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, filename)

    print(f"Pobieranie silnika...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Zapisano pomyślnie jako: {save_path}")
        return save_path

    print(f"Błąd pobierania: HTTP {response.status_code}")
    return None