import requests
import re
import json

# Estas son las direcciones donde el robot buscará los nuevos links
CANALES_A_BUSCAR = {
    "1- TVN": "https://www.tvn.cl/envivo/",
    "2- MEGA": "https://www.mega.cl/senal-en-vivo/",
    "3- CHV": "https://www.chilevision.cl/senal-online",
    "4- CANAL 13": "https://www.13.cl/en-vivo/"
}

def capturar_enlace(url_sitio):
    try:
        # Engañamos a la web para que crea que somos un navegador normal
        cabeceras = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        respuesta = requests.get(url_sitio, headers=cabeceras, timeout=15)
        
        # Buscamos el link largo que contiene ".m3u8" y los tokens
        encontrado = re.findall(r'(https?://[^\s"\']+\.m3u8\?[^"\']+)', respuesta.text)
        
        if encontrado:
            # Si hay varios, elegimos el que parece ser el oficial de video
            return encontrado[0].replace('\\/', '/')
    except:
        return None
    return None

# 1. Abrimos tu lista de canales
with open("canales.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

hay_cambios = False

# 2. El robot recorre tu lista y busca links nuevos
for canal in datos:
    nombre = canal.get("title")
    if nombre in CANALES_A_BUSCAR:
        link_nuevo = capturar_enlace(CANALES_A_BUSCAR[nombre])
        
        if link_nuevo and link_nuevo != canal["url"]:
            canal["url"] = link_nuevo
            hay_cambios = True
            print(f"Actualizado: {nombre}")

# 3. Solo si encontró algo nuevo, guarda el archivo
if hay_cambios:
    with open("canales.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("¡Éxito! Tu lista de canales ha sido actualizada.")
else:
    print("No se encontraron links nuevos en esta revisión.")
