import requests
import re
import json

# Configuración de búsqueda para cada canal
CANALES_BUSQUEDA = {
    "1- TVN": "https://www.tvn.cl/envivo/",
    "2- MEGA": "https://www.mega.cl/senal-en-vivo/",
    "3- CHV": "https://www.chilevision.cl/senal-online",
    "4- CANAL 13": "https://www.13.cl/en-vivo/"
}

def buscar_m3u8(url_web):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url_web, headers=headers, timeout=15)
        # Buscamos enlaces que terminen en .m3u8 dentro del código de la página
        match = re.search(r'https?://[\w\.-]+/[\w\.-/]+.m3u8[^\s"\'<>]*', response.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Error buscando en {url_web}: {e}")
    return None

# 1. Leer tu archivo canales.json
try:
    with open("canales.json", "r", encoding="utf-8") as f:
        lista_canales = json.load(f)
except Exception as e:
    print(f"No se pudo leer canales.json: {e}")
    exit()

# 2. Intentar actualizar cada uno de los 4 canales
cambio_realizado = False
for canal in lista_canales:
    nombre = canal.get("title")
    if nombre in CANALES_BUSQUEDA:
        nuevo_link = buscar_m3u8(CANALES_BUSQUEDA[nombre])
        if nuevo_link and nuevo_link != canal["url"]:
            print(f"Actualizando {nombre}...")
            canal["url"] = nuevo_link
            cambio_realizado = True

# 3. Guardar solo si hubo cambios
if cambio_realizado:
    with open("canales.json", "w", encoding="utf-8") as f:
        json.dump(lista_canales, f, indent=2, ensure_ascii=False)
    print("¡Archivo canales.json actualizado con éxito!")
else:
    print("No se encontraron links nuevos o no hubo cambios.")
