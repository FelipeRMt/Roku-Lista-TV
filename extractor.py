import requests
import json
import re

# Enlaces directos a los servidores de video (saltando la página web)
CANALES_MEDIASTREAM = {
    "1- TVN": "https://mdstrm.com/live-stream-playlist/57a498c4d7b86d600e5461cb.m3u8",
    "2- MEGA": "https://mdstrm.com/live-stream-playlist/53d2c1a32640614e62a0e000.m3u8",
    "3- CHV": "https://mdstrm.com/live-stream-playlist/63ee47e1daeeb80a30d98ef4.m3u8"
}

def obtener_token_mediastream(url_base):
    try:
        # allow_redirects=True obliga al servidor a darnos la URL final con el token largo
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        respuesta = requests.get(url_base, headers=headers, allow_redirects=True, timeout=15)
        if respuesta.status_code == 200:
            return respuesta.url
    except:
        pass
    return None

def buscar_canal_13():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        respuesta = requests.get("https://www.13.cl/en-vivo/", headers=headers, timeout=15)
        match = re.search(r'(https?://origin\.dpsgo\.com/[^"\']+\.m3u8\?[^"\']+)', respuesta.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except:
        pass
    return None

# 1. Abrimos tu lista
with open("canales.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

hay_cambios = False

# 2. El robot procesa cada canal
for canal in datos:
    nombre = canal.get("title")
    url_nueva = None
    
    if nombre in CANALES_MEDIASTREAM:
        url_nueva = obtener_token_mediastream(CANALES_MEDIASTREAM[nombre])
    elif nombre == "4- CANAL 13":
        url_nueva = buscar_canal_13()
        
    if url_nueva and url_nueva != canal["url"]:
        canal["url"] = url_nueva
        hay_cambios = True
        print(f"Éxito: Link actualizado para {nombre}")

# 3. Guardar solo si hubo cambios
if hay_cambios:
    with open("canales.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("Finalizado: Se guardaron los cambios en canales.json")
else:
    print("Finalizado: Los links actuales siguen siendo válidos.")
