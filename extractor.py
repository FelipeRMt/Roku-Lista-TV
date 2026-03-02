import requests
import re
import json

# Configuración de búsqueda para cada canal oficial en Chile
CANALES_BUSQUEDA = {
    "1- TVN": "https://www.tvn.cl/envivo/",
    "2- MEGA": "https://www.mega.cl/senal-en-vivo/",
    "3- CHV": "https://www.chilevision.cl/senal-online",
    "4- CANAL 13": "https://www.13.cl/en-vivo/"
}

def buscar_m3u8(url_web):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        response = requests.get(url_web, headers=headers, timeout=15)
        # Buscamos el link .m3u8 que los canales ocultan en su código
        match = re.search(r'https?://[\w\.-]+/[\w\.-/]+.m3u8[^\s"\'<>]*', response.text)
        if match:
            return match.group(0)
    except:
        pass
    return None

# 1. Leer tu archivo canales.json actual
try:
    with open("canales.json", "r", encoding="utf-8") as f:
        lista_canales = json.load(f)
except Exception as e:
    print(f"Error leyendo canales.json: {e}")
    exit()

# 2. Revisar y actualizar cada canal
hubo_cambios = False
for canal in lista_canales:
    nombre_canal = canal.get("title")
    if nombre_canal in CANALES_BUSQUEDA:
        nuevo_link = buscar_m3u8(CANALES_BUSQUEDA[nombre_canal])
        if nuevo_link and nuevo_link != canal["url"]:
            print(f"-> Nuevo link para {nombre_canal}")
            canal["url"] = nuevo_link
            hubo_cambios = True

# 3. Guardar si encontramos algo nuevo
if hubo_cambios:
    with open("canales.json", "w", encoding="utf-8") as f:
        json.dump(lista_canales, f, indent=2, ensure_ascii=False)
    print("¡canales.json actualizado!")
else:
    print("No se encontraron links nuevos en esta hora.")
