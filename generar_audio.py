#!/usr/bin/env python3
"""
Generador de audio neuronal para Allons-y !
============================================
Genera MP3 con voces neuronales gratuitas de Microsoft (edge-tts)
para todas las frases francesas de la plataforma.

USO (en tu computadora, una sola vez por cada lote de contenido):
  1. pip install edge-tts
  2. python generar_audio.py
  3. Sube la carpeta  audio/  junto a tu index.html al repo
     git add . && git commit -m "audio neuronal" && git push

Voces disponibles (cambia VOICE si prefieres otra):
  fr-FR-DeniseNeural   (mujer, muy natural — recomendada)
  fr-FR-VivienneMultilingualNeural (mujer, excelente)
  fr-FR-HenriNeural    (hombre)
  fr-FR-RemyMultilingualNeural (hombre, excelente)
Escucha demos:  edge-tts --list-voices | grep fr-FR
"""
import asyncio, json, os, re, sys

VOICE = "fr-FR-DeniseNeural"
RATE  = "-8%"          # un poco más lento que nativo, ideal para alumnos

def djb2(s: str) -> str:
    """Mismo hash que usa el index.html para nombrar los archivos."""
    s = re.sub(r"\s+", " ", s).strip()
    h = 5381
    for ch in s:
        h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    if h == 0: return "0"
    r = ""
    while h:
        r = d[h % 36] + r
        h //= 36
    return r

async def main():
    try:
        import edge_tts
    except ImportError:
        sys.exit("Falta edge-tts. Instala con:  pip install edge-tts")

    phrases = json.load(open("phrases.json", encoding="utf-8"))
    os.makedirs("audio", exist_ok=True)
    print(f"Generando {len(phrases)} audios con {VOICE}…\n")

    for i, p in enumerate(phrases, 1):
        fname = f"audio/{djb2(p)}.mp3"
        if os.path.exists(fname):
            print(f"[{i:3}/{len(phrases)}] ya existe → {fname}")
            continue
        tts = edge_tts.Communicate(p, VOICE, rate=RATE)
        await tts.save(fname)
        print(f"[{i:3}/{len(phrases)}] {fname}  ←  {p[:60]}")

    print("\n✓ Listo. Sube la carpeta audio/ a tu repositorio.")

if __name__ == "__main__":
    asyncio.run(main())
