import os
import requests

BASE_URL = "https://api.modrinth.com/v2"
USER_AGENT = "TwojaNazwaProjektu/1.0 (kontakt@twojadomena.com)"

HEADERS = {"User-Agent": USER_AGENT}


def search_plugins(query: str, version: str = None, loader: str = None, limit: int = 10):
    """Wyszukuje pliki/pluginy na Modrinth z opcjonalnym filtrowaniem

    po wersji oraz silniku (loaderze, np. paper, spigot, purpur).
    """
    url = f"{BASE_URL}/search"

    facets = [["project_type:plugin"]]

    if version:
        facets.append([f"versions:{version}"])

    if loader:
        facets.append([f"categories:{loader}"])

    params = {"query": query, "facets": str(facets).replace("'", '"'), "limit": limit}

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json().get("hits", [])

    response.raise_for_status()


def get_plugin_versions(project_id: str, version: str = None, loader: str = None):
    """Pobiera listę dostępnych wersji konkretnego projektu (pluginu),

    z możliwością przefiltrowania po wersji serwera i silniku.
    """
    url = f"{BASE_URL}/project/{project_id}/version"

    params = {}
    if loader:
        params["loaders"] = f'["{loader}"]'
    if version:
        params["game_versions"] = f'["{version}"]'

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()

    response.raise_for_status()


def download_plugin_version(version_data: dict, output_dir: str = "plugins"):
    """Pobiera plik `.jar` pluginu na podstawie danych konkretnej wersji

    zwróconych przez API.
    """
    os.makedirs(output_dir, exist_ok=True)

    files = version_data.get("files", [])
    if not files:
        raise ValueError("Ta wersja nie zawiera żadnych plików do pobrania.")

    # Wybieramy główny plik (często jest tylko jeden)
    primary_file = next((f for f in files if f.get("primary")), files[0])

    file_url = primary_file["url"]
    file_name = primary_file["filename"]
    save_path = os.path.join(output_dir, file_name)

    response = requests.get(file_url, headers=HEADERS, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path

    response.raise_for_status()


def download_plugin_by_name(
    query: str, version: str, loader: str, output_dir: str = "plugins"
):
    """Kompleksowa funkcja pomocnicza: wyszukuje plugin pasujący do kryteriów

    i automatycznie pobiera jego najnowszą pasującą wersję.
    """
    results = search_plugins(query=query, version=version, loader=loader, limit=1)

    if not results:
        print(f"Nie znaleziono pluginu '{query}' dla wersji {version} i silnika {loader}.")
        return None

    project_id = results[0]["project_id"]
    print(f"Znaleziono projekt: {results[0]['title']} (ID: {project_id})")

    versions = get_plugin_versions(project_id, version=version, loader=loader)

    if not versions:
        print("Brak kompatybilnych wersji dla podanych kryteriów.")
        return None

    # Pobieramy najnowszą wersję (pierwszą na liście z API)
    downloaded_path = download_plugin_version(versions[0], output_dir)
    print(f"Pobrano pomyślnie do: {downloaded_path}")
    return downloaded_path