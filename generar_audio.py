#!/usr/bin/env python3
"""
Generador de audio neuronal para Allons-y ! (v2 — dos voces)
=============================================================
Genera MP3 con voces neuronales gratuitas de Microsoft (edge-tts):
  ♀ fr-FR-DeniseNeural  → archivos  {hash}.mp3
  ♂ fr-FR-HenriNeural   → archivos  {hash}_m.mp3

USO (en tu computadora, cada vez que haya contenido nuevo):
  1. pip install edge-tts          (solo la primera vez)
  2. python generar_audio.py
  3. git add . && git commit -m "audio" && git push

Los audios ya existentes se saltan automáticamente: solo genera los nuevos.
Otras voces masculinas/femeninas: edge-tts --list-voices | grep fr-FR
"""
import asyncio, json, os, re, sys

VOICES = {"f": "fr-FR-DeniseNeural", "m": "fr-FR-HenriNeural"}
RATE   = "-8%"   # un poco más lento que nativo, ideal para alumnos

def djb2(s: str) -> str:
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

    items = json.load(open("phrases.json", encoding="utf-8"))
    os.makedirs("audio", exist_ok=True)
    print(f"Generando {len(items)} audios…\n")
    nuevos = 0
    for i, it in enumerate(items, 1):
        text, v = it["t"], it.get("v", "f")
        fname = f"audio/{djb2(text)}{'_m' if v == 'm' else ''}.mp3"
        if os.path.exists(fname):
            continue
        tts = edge_tts.Communicate(text, VOICES[v], rate=RATE)
        await tts.save(fname)
        nuevos += 1
        print(f"[{i:3}/{len(items)}] {'♂' if v=='m' else '♀'} {fname}  ←  {text[:55]}")

    print(f"\n✓ Listo: {nuevos} audios nuevos generados (los demás ya existían).")
    print("  Sube la carpeta audio/ con git push.")

if __name__ == "__main__":
    asyncio.run(main())
