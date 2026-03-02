import requests
import re
import json

# URLs de las señales ONLINE actualizadas
CANALES_BUSQUEDA = {
    "1- TVN": "https://www.tvn.cl/envivo/",
    "2- MEGA": "https://www.mega.cl/senal-en-vivo/",
    "3- CHV": "https://www.chilevision.cl/senal-online",
    "4- CANAL 13": "https://www.13.cl/en-vivo/"
}

def buscar_m3u8(url_web):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(url_web, headers=headers, timeout=20)
        
        # 1. Buscador para Mediastream (CHV, TVN, Mega) y DPS (Canal 13)
        # Busca patrones .m3u8 seguidos de tokens larguísimos
        patrones = [
            r'(https?://mdstrm\.com/live-stream-playlist/[^"\']+\.m3u8\?[^"\']*)',
            r'(https?://origin\.dpsgo\.com/[^"\']+\.m3u8\?[^"\']*)',
            r'(https?://[\w\.-]+/[\w\.-/]+\.m3u8\?[^"\']*)'
        ]
        
        for patron in patrones:
            enlaces = re.findall(patron, response.text)
            if enlaces:
                # Nos quedamos con el más largo (el que tiene todos los tokens)
                link = max(enlaces, key=len)
                # Limpiar posibles barras escapadas del código fuente
                return link.replace('\\/', '/')
                
    except Exception as e:
        print(f"Error buscando en {url_web}: {e}")
    return None

# Cargar tu lista actual
with open("canales.json", "r", encoding="utf-8") as f:
    lista_canales = json.load(f)

cambios = False
for canal in lista_canales:
    title = canal.get("title")
    if title in CANALES_BUSQUEDA:
        print(f"Buscando link dinámico para: {title}...")
        nuevo_link = buscar_m3u8(CANALES_BUSQUEDA[title])
        
        if nuevo_link and nuevo_link != canal["url"]:
            canal["url"] = nuevo_link
            cambios = True
            print(f"-> ¡ÉXITO! Link actualizado para {title}")
        else:
            print(f"-> No hubo cambios o no se encontró link nuevo para {title}")

# Guardar si hubo actualizaciones
if cambios:
    with open("canales.json", "w", encoding="utf-8") as f:
        json.dump(lista_canales, f, indent=2, ensure_ascii=False)
    print("PROCESO TERMINADO: canales.json actualizado.")
else:
    print("PROCESO TERMINADO: No se requirieron cambios.")
