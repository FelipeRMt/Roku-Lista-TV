import requests
import re
import json

# Configuración de las webs oficiales
CANALES_CONFIG = {
    "TVN": "https://www.tvn.cl/envivo/",
    "Mega": "https://www.mega.cl/senal-en-vivo/",
    "CHV": "https://www.chilevision.cl/senal-online",
    "Canal 13": "https://www.13.cl/en-vivo/"
}

def buscar_m3u8(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        # Buscamos el patrón de un enlace de video streaming
        match = re.search(r'https?://[\w\.-]+/[\w\.-/]+.m3u8[^\s"\'<>]*', response.text)
        return match.group(0) if match else None
    except:
        return None

# 1. Cargar tu archivo actual
with open("canales.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Actualizar cada canal si se encuentra un link nuevo
for item in data:
    nombre = item.get("nombre") # Ajusta "nombre" según como se llame en tu JSON
    if nombre in CANALES_CONFIG:
        nuevo_link = buscar_m3u8(CANALES_CONFIG[nombre])
        if nuevo_link:
            item["url"] = nuevo_link # Ajusta "url" según tu JSON
            print(f"Actualizado {nombre}: {nuevo_link}")

# 3. Guardar los cambios
with open("canales.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
