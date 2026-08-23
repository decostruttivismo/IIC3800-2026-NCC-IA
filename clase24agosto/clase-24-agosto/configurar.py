#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reescribe el usuario, el repositorio, la rama o la carpeta en el README y en todos
los cuadernos, y opcionalmente genera un código QR con el enlace de clase.

    python configurar.py --qr
    python configurar.py --repo OTRO-NOMBRE
    python configurar.py --carpeta clase-31-agosto --qr

Valores actuales: decostruttivismo / IIC3800-2026-NCC-IA / main / clase-24-agosto

El QR requiere `pip install qrcode[pil]`; si no está instalado, el script imprime la
URL para convertirla con cualquier generador web.

Aviso: GitHub sustituye por guiones los caracteres que no admite en el nombre de un
repositorio (espacios, «+», etc.). Usa aquí el nombre tal como quedó en GitHub.
"""
import argparse, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parent
EXTENSIONES = {".md", ".ipynb", ".py"}
EXCLUIR = {"configurar.py"}

ACTUAL = {"usuario": "decostruttivismo",
          "repo":    "IIC3800-2026-NCC-IA",
          "rama":    "main",
          "carpeta": "clase-24-agosto"}


def archivos():
    for p in RAIZ.rglob("*"):
        if p.is_file() and p.suffix in EXTENSIONES and p.name not in EXCLUIR:
            if ".git" not in p.parts and ".ipynb_checkpoints" not in p.parts:
                yield p


def enlace(v):
    return ("https://colab.research.google.com/github/%(usuario)s/%(repo)s"
            "/blob/%(rama)s/%(carpeta)s/notebooks/00_prueba.ipynb" % v)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ACTUAL:
        ap.add_argument("--" + k, default=None, help="actual: " + ACTUAL[k])
    ap.add_argument("--qr", action="store_true", help="generar docs/qr_colab.png")
    a = ap.parse_args()

    nuevo = dict(ACTUAL)
    for k in ACTUAL:
        if getattr(a, k):
            nuevo[k] = getattr(a, k)

    cambios = [(ACTUAL[k], nuevo[k]) for k in ACTUAL if ACTUAL[k] != nuevo[k]]
    if cambios:
        n = 0
        for p in archivos():
            t = p.read_text(encoding="utf-8")
            s = t
            for viejo, nuev in cambios:
                s = s.replace(viejo, nuev)
            if s != t:
                p.write_text(s, encoding="utf-8"); n += 1
                print("  actualizado:", p.relative_to(RAIZ))
        print("\n%d archivo(s) actualizado(s)." % n)
        print("Recuerda cambiar también el diccionario ACTUAL de este script.")
    else:
        print("Sin cambios de nombres.")

    print("\nEnlace para proyectar en clase:\n  %s" % enlace(nuevo))

    if a.qr:
        try:
            import qrcode
        except ImportError:
            print("\n(qrcode no está instalado: `pip install qrcode[pil]`, o usa un "
                  "generador web con la URL de arriba.)")
            return
        destino = RAIZ / "docs" / "qr_colab.png"
        destino.parent.mkdir(exist_ok=True)
        qrcode.make(enlace(nuevo)).save(destino)
        print("QR guardado en:", destino.relative_to(RAIZ))


if __name__ == "__main__":
    sys.exit(main())
